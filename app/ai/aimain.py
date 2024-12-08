from duckduckgo_search import AsyncDDGS
from loguru import logger
import asyncio

async def getfunc(text):
    try:
        query = f"""You have to understand this user request | {text} | and depending on what he wants, you have to send, if he wants to generate an image, then you have to answer me [_gen_image_] , if you read the link and extract the content of the web page, then you have to answer me [_scrape_url_, and the link from which he wants to extract the content] , if he wants to shorten the text that is in the request, then you have to answer me [_scrape_input_] , if the user wants to find some new information or asks to send him a link or wants you to find information on the Internet, then I get [_search_in_inet_] in response, if neither one nor the other, then you have to answer me [_gen_text_] , you have no right to answer anything else, if neither one nor the other, answer only"""
        result = await AsyncDDGS().achat(keywords=query, model='gpt-4o-mini')
        if result is not None:
            return result
    except Exception as ex:
        logger.error(f'Ошибка:\n{ex}')

#print(asyncio.run(getfunc('Создай картинку медведей с пивом')))