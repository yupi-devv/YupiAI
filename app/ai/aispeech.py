from gradio_client import Client
from loguru import logger
from duckduckgo_search import AsyncDDGS


async def speech_russian(text):
    try:
        client = Client("VoiceCloning-be/text-to-speech")
        result = client.predict(
                text=text,
                voice="ru-RU-DmitryNeural - ru-RU (Male)",
                rate=0,
                pitch=0,
                api_name="/predict"
        )
        if result is not None:
            return str(result[0])
    except Exception as ex:
        logger.error(f'Ошибка при генерации русского аудио:\n{ex}')


async def speech_english(text):
    try:
        client = Client("VoiceCloning-be/text-to-speech")
        result = client.predict(
                text=text,
                voice="en-US-ChristopherNeural - en-US (Male)",
                rate=0,
                pitch=0,
                api_name="/predict"
        )
        if result is not None:
            return str(result[0])
    except Exception as ex:
        logger.error(f'Ошибка при генерации английского аудио:\n{ex}')


async def ai_speech(text):
    try:
        ee = await AsyncDDGS().atranslate(text, to="en")
        lang = str(ee[0]["detected_language"])
        match lang:
            case 'ru':
                result = await speech_russian(text)
            case 'en':
                result = await speech_english(text)
        if result is not None:
            return result
        else:
            raise Exception
    except Exception as ex:
        logger.error(f'Ошибка:\n{ex}')

