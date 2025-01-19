from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.enums.parse_mode import ParseMode
from app.ai.aigentext import generate
from app.utils.allowed_users import ALLOWED_IDS


rt = Router()



@rt.message(CommandStart(), F.func(lambda msg: msg if msg.from_user.id in ALLOWED_IDS else None))
async def cmd_start(msg: Message):
    await msg.delete()
    await msg.answer(
        '👋 Привет друг, я ИИ, созданный разработчиком [𒆜ʏʊքɨ 𒆜](https://github.com/yupi-devv/).'
        '\n\nЯ использую открытые модели ИИ с [Hugging Face](https://huggingface.co/) и [Mistral AI](https://mistral.ai/) для генерации текста.'
        '\n\nНекоторые из этих моделей используют данные запросов для собственного дообучения.'
        '\n\nЗдесь используется поиск в интернете с помощью [DuckDuckGo Search](https://pypi.org/project/duckduckgo-search/), это реализация RAG.'
        '\n\nТакже я умею генерировать картинки, читать голосовые сообщения, отвечать голосовыми, сокращать текст с ссылок и с обычного ввода, рассматривать фотографии и PDF документы.',
        parse_mode=ParseMode.MARKDOWN
    )
