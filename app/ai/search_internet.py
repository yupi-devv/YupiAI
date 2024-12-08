import asyncio
from duckduckgo_search import AsyncDDGS
import random
from loguru import logger


def check_el(ll: list, href):
    if len(ll) != 0:
        for i in ll:
            if i["href"] == href:
                return False
            else:
                return True
    else:
        return True


async def ddg(text=None):
    try:
        ready = []
        
        try:
            text_res = await AsyncDDGS().atext(text, region='ru-ru')
            for i in text_res:
                d = None
                if i["href"] is not None:
                    d = {"href": i["href"]}
                    if (i["title"] is not None) and (i["body"] is not None):
                        d = {"href": i["href"], "description": i["title"]+"\n-------\n"+i["body"]}
                    elif i["title"] is not None:
                        d = {"href": i["href"], "description": i["title"]}
                    elif i["body"] is not None:
                        d = {'href': i["href"], "description": i["body"]}
                if d is not None:
                    ready.append(d)
        except:
            logger.warning('Не найдены текста')
        try:
            news_res = await AsyncDDGS().anews(keywords=text, region='ru-ru', safesearch='off')
            for i in news_res:
                d = None
                if (i["url"] is not None) and check_el(ready, i["url"]):
                    d = {"href": i["url"]}
                    if (i["title"] is not None) and (i["body"] is not None):
                        d = {"href": i["url"], "description": i["title"]+"\n-------\n"+i["body"]}
                    elif i["title"] is not None:
                        d = {"href": i["url"], "description": i["title"]}
                    elif i["body"] is not None:
                        d = {'href': i["url"], "description": i["body"]}
                if d is not None:
                    ready.append(d)
        except:
            logger.warning('Не найдены новости')
        try:
            images_res = await AsyncDDGS().aimages(text, region='ru-ru', safesearch='off')
            for i in images_res:
                d = None
                
                if (i["image"] is not None) and (check_el(ready, i["image"]) is True):
                    d = {"href": i["image"]}
                    if i["title"] is not None:
                        d = {"href": i["url"], "description": i["title"]}
                if d is not None:
                    ready.append(d)
        except:
            logger.warning('Не найдены фото')
        try:
            videos_res = await AsyncDDGS().avideos(text, region='ru-ru', safesearch='off', timelimit='y')
            for i in videos_res:
                d = None
                if (i["content"] is not None) and check_el(ready, i["content"]):
                    d = {"href": i["content"]}
                    if i["description"] is not None:
                        d = {"href": i["content"], "description": i["description"]}
                if d is not None:
                    ready.append(d)
        except:
            logger.warning('Не найдены видео')
        try:
            pdf_res = await AsyncDDGS().atext(text + ':pdf', region='ru-ru', safesearch='off', timelimit='y', max_results=10)
            for i in pdf_res:
                d = None
                if i["href"] is not None:
                    d = {"href": i["href"]}
                    if (i["title"] is not None) and (i["body"] is not None):
                        d = {"href": i["href"], "description": i["title"]+"\n-------\n"+i["body"]}
                    elif i["title"] is not None:
                        d = {"href": i["href"], "description": i["title"]}
                    elif i["body"] is not None:
                        d = {'href': i["href"], "description": i["body"]}
                if d is not None:
                    ready.append(d)
        except:
            logger.warning('Не найдены пдфки')
        readys = tuple(ready[:random.randint(5, 10)])
        if len(readys) == 0:
            logger.error('Ресуры не найдены')
        return readys
    except Exception as ex:
        logger.error(f'Ошибка:\n{ex}')
