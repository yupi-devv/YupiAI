from decouple import config
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message


LOGLEVEL = config('LOGLEVEL') # уровень логирования

TOKEN = config('BOTTOKEN') # получение токена бота из .env файла

bot = Bot(token=TOKEN)





