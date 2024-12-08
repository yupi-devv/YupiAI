from gradio_client import Client, handle_file
from loguru import logger


async def transcribe_audio(path_to_file):
    try:
        client = Client("hf-audio/whisper-large-v3-turbo")
        result = client.predict(
                inputs=handle_file(path_to_file),
                task="transcribe",
                api_name="/predict"
        )
        return result
    except Exception as ex:
        logger.error(f'Ошибка при транскрибации текста:\n{ex}')
