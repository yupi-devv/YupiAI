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



BASE_URL = "ссылка для вашего тунеля трафика"
WEBHOOK_PATH = "/webhook"


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
    uvicorn.run(app, host="0.0.0.0", port="порт, тот же, что и в вашем тунеле.")