import asyncio
from app.utils.logger import InterceptHandler
from app.handlers import routers
from app.utils.default_commands import setup_default_commands
import logging
from btconf import LOGLEVEL, bot
from loguru import logger
from aiogram import Dispatcher
import os



async def main():
    dirs = os.listdir(os.getcwd())
    if 'users_audios' not in dirs or 'users_histories' not in dirs or 'users_images' not in dirs:
        os.mkdir('users_audios')
        os.mkdir('users_histories')
        os.mkdir('users_images')
    logging.basicConfig(
        handlers=[InterceptHandler()],
        level=logging.getLevelName(LOGLEVEL)
    )
    dp = Dispatcher()
    try:
        for i in routers:
            dp.include_router(i)
        logger.info('Роутеры зарегались успешно!')
    except:
        logger.error('Роутеры не зарегались!')
    
    await setup_default_commands(bot)
    await bot.delete_webhook()
    await dp.start_polling(bot)
    

if __name__ == '__main__':
    asyncio.run(main())