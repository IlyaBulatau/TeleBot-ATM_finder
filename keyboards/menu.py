from aiogram.types import BotCommand

async def menu(bot):
    commands = [
        BotCommand(command='/start', description='Начни сначала'),
        BotCommand(command='/bank', description='Выбери банк'),
    ]
    
    await bot.set_my_commands(commands)