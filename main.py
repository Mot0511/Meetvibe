from dotenv import find_dotenv, load_dotenv

from middlewares.db import DatabaseSession
from utils.get_city import get_city
load_dotenv(find_dotenv())
import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from handlers.register import register_router
from db.engine import create_db, session_maker

bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher()

dp.include_router(register_router)

async def on_startup():
    await create_db()

async def on_shutdown():
    print('Bot is down')

async def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    dp.update.middleware(DatabaseSession(session_maker=session_maker))

    await dp.start_polling(bot)
    

asyncio.run(main())