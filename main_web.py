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




BASE_URL = "https://<твой статический ip сервера>:<443, 80, 88, 8443 -- один из этих портов, смотря какой настроите | или ссылка если вы настроили отдельно доменное имя для бота>"
WEBHOOK_PATH = "/webhook"
ssl_cert = 'путь до твоего cert.pem'
ssl_key = 'путь до твоего key.pem'
# как создать кастомные сертификаты для вашего сервера можно посмотреть здесь https://core.telegram.org/bots/self-signed

dp = Dispatcher()


async def lifespan(app: FastAPI):
    try:
        for i in routers:
            dp.include_router(i)
        logger.info('Роутеры зарегались успешно!')
    except:
        logger.error('Роутеры не зарегались!')
    await setup_default_commands(bot)
    url_webhook = BASE_URL + WEBHOOK_PATH
    await bot.set_webhook(url=url_webhook,
                          allowed_updates=dp.resolve_used_update_types(),
                          drop_pending_updates=True,
                          certificate=types.FSInputFile(ssl_cert)
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
    uvicorn.run(app, host="0.0.0.0", port="443, 80, 88, 8443 -- один из этих портов, смотря какой настроите, указывать в int", ssl_keyfile=ssl_key, ssl_certfile=ssl_cert)