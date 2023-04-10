from aiogram.types import BotCommand

async def menu(bot):
    commands = [
        BotCommand(command='/start', description='Начни сначала'),
        BotCommand(command='/place', description='Населенный пункт'),
        BotCommand(command='/cancel', description='Отмена')
    ]
    
    await bot.set_my_commands(commands)