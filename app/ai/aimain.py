from duckduckgo_search import AsyncDDGS
from loguru import logger
import asyncio


async def getfunc(text):
    try:
        query = (
            f"Please analyze the user's request: |{text}|. Based on their needs, respond with one of the following options:"
            f"\n\nIf they want to generate an image, respond with: [_gen_image_]."
            f"\nIf they want to scrape content from a URL, respond with: [_scrape_url_, URL]."
            f"\nIf they want to shorten text within the input, respond with: [_scrape_input_, TEXT_INPUT]."
            f"\nIf they are looking for new information or asking for links, respond with: [_search_in_inet_]."
            f"\nOtherwise, respond with: [_gen_text_]."
        )

        logger.info(f"Sending query: {query}")

        result = await AsyncDDGS().achat(keywords=query, model='gpt-4o-mini')
        logger.info(f"Received result: {result}")

        if result:
            if any(keyword in result for keyword in
                   ['[_gen_text_]', '[_scrape_url_,', '[_scrape_input_,', '[_search_in_inet_]', '[_gen_image_]']):
                return result
            else:
                logger.warning(f"Unexpected result: {result}. Falling back to [_gen_text_]")
                return '[_gen_text_]'
        else:
            logger.warning("Received empty result. Falling back to [_gen_text_]")
            return '[_gen_text_]'
    except Exception as ex:
        logger.error(f'Error: {ex}')
        return '[_gen_text_]'

#print(asyncio.run(getfunc('Создай картинку медведей с пивом')))