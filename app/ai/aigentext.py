from mistralai import Mistral
from decouple import config
from loguru import logger
from app.utils.bbs import encode_image
import json
from decouple import config



MISTRALTOKEN = config('MISTRALTOK') # получение токена mistral из .env файла



async def generate(content, usr_id, additional_messages=None):
    try:
        if additional_messages is None:
            additional_messages = []
        with open(f'users_histories/{usr_id}.json', 'r') as file:
            data = json.load(file)
        data_list = list(data)
        messages = [i for i in data_list] + additional_messages
        messages.append({'role': 'user', 'content': content})
        s = Mistral(
            api_key=MISTRALTOKEN,
        )
        res = await s.agents.complete_async(
            messages=messages,
            agent_id=config('AGENTID')
        )
        if res is not None:
            return res.choices[0].message.content
    except Exception as ex:
        logger.error(f'Ошибка при генерации текста:\n{ex}')


async def gen_from_image(text, image_path):
    try:
        # Initialize the Mistral client
        base64_image = encode_image(image_path)

        client = Mistral(api_key=MISTRALTOKEN)

        # Define the messages for the chat
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": text
                    },
                    {
                        "type": "image_url",
                        "image_url": f"data:image/jpeg;base64,{base64_image}" 
                    }
                ]
            }
        ]

        # Get the chat response
        chat_response = client.chat.complete(
            model='pixtral-12b-2409',
            messages=messages
        )
        if chat_response is not None:
            return chat_response.choices[0].message.content
    except Exception as ex:
        logger.error(f'Ошибка:\n{ex}')


#print(asyncio.run(generate('как на python сделать функцию хеширования sha_1')))