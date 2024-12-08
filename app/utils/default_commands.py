from aiogram import types

async def setup_default_commands(bot):
    await bot.set_my_commands(
        commands=[
            types.BotCommand(command="start", description="▶️ Начало работы с ботом"),
            types.BotCommand(command="clear_history", description="🗑 Очистить историю сообщений с ботом")
        ]
    )