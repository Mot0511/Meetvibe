from dotenv import find_dotenv, load_dotenv

from db.orm_query import get_all_ids
from filters.isRegistered import isRegistered
from middlewares.db import DatabaseSession
from utils.get_city import get_city
load_dotenv(find_dotenv())
import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from handlers.profile import register_router
from handlers.search import search_router
from db.engine import create_db, drop_db, session_maker
from aiogram.enums.parse_mode import ParseMode
from kbds import reply
from aiogram import F

bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher()

@dp.message(CommandStart(), isRegistered(session_maker()))
async def start(mess: types.Message):
    await mess.answer(text='Привет! Meetvibe - это бот для знакомств по интересам', reply_markup=reply.kb_menu)

@dp.message(F.text == 'Главное меню')
async def main_menu(mess: types.Message):
    await mess.answer(text='Главное меню:', reply_markup=reply.kb_menu)

dp.include_router(register_router)
dp.include_router(search_router)

async def on_startup():
    # await drop_db()
    await create_db()

async def on_shutdown():
    print('Bot is down')

async def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    dp.update.middleware(DatabaseSession(session_maker=session_maker))

    await dp.start_polling(bot)
    

asyncio.run(main())