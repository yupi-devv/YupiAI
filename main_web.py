from fastapi import FastAPI, Request
from aiogram import Dispatcher, types
from fastapi.requests import Request
import uvicorn
from app.utils.logger import InterceptHandler
from app.handlers import routers
from app.utils.default_commands import setup_default_commands
import logging
from btconf import LOGLEVEL, bot
from loguru import logger
from decouple import config
import os




BASE_URL = config("BASEURL")
WEBHOOK_PATH = config("WEBHOOKPATH")
ssl_cert = config("SSLCERT")
ssl_key = config("SSLKEY")
# как создать кастомные сертификаты для вашего сервера можно посмотреть здесь https://core.telegram.org/bots/self-signed

dp = Dispatcher()


async def lifespan(app: FastAPI):
    dirs = os.listdir(os.getcwd())
    if 'users_audios' not in dirs or 'users_histories' not in dirs or 'users_images' not in dirs:
        os.mkdir('users_audios')
        os.mkdir('users_histories')
        os.mkdir('users_images')
    try:
        for i in routers:
            dp.include_router(i)
        logger.info('Роутеры зарегались успешно!')
    except:
        logger.error('Роутеры не зарегались!')
    await setup_default_commands(bot)
    url_webhook = BASE_URL + WEBHOOK_PATH
    if ssl_cert is not None or ssl_key != '':
        await bot.set_webhook(url=url_webhook,
                              allowed_updates=dp.resolve_used_update_types(),
                              drop_pending_updates=True,
                              certificate=types.FSInputFile(ssl_cert)
                              )
    else:
        await bot.set_webhook(url=url_webhook,
                              allowed_updates=dp.resolve_used_update_types(),
                              drop_pending_updates=True,
                              )
    yield
    await bot.delete_webhook()

app = FastAPI(lifespan=lifespan)


# Обработчик вебхука
@app.post(WEBHOOK_PATH)
async def webhook(request: Request):
    update = types.Update.model_validate(await request.json(), context={"bot": bot})
    await dp.feed_update(bot, update)



# Запуск бота
if __name__ == "__main__":
    HOST = config("HOST")
    PORT = config("PORT")
    logging.basicConfig(
        handlers=[InterceptHandler()],
        level=logging.getLevelName(LOGLEVEL)
    )
    if ssl_cert is not None or ssl_cert != '':
        if ssl_key is not None or ssl_key != '':
            uvicorn.run(app, host=HOST, port=PORT, ssl_keyfile=ssl_key, ssl_certfile=ssl_cert)
    else:
        uvicorn.run(app, host=HOST, port=PORT)
