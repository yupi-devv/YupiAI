from loguru import logger
from duckduckgo_search import AsyncDDGS

async def translate_prompt(text):
    try:
        tt = await AsyncDDGS().atranslate(text, to="en")
        text = str(tt[0]["translated"])
        return text
    except Exception as ex:
        logger.error(f'Ошибка при переводе:\n{ex}')

