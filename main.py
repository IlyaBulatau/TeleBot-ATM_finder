import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import load_config_token
from handlers import handlers
from keyboards import menu

async def main():
    bot = Bot(token=load_config_token())
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    dp.include_router(handlers.router)

    dp.startup.register(menu.menu)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())