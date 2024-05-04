import asyncio
from config import TOKEN
from filters.isRegistered import isRegistered
from middlewares.db import DatabaseSession
from aiogram import F, Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from handlers.profile import register_router
from handlers.search import search_router
from db.engine import create_db, session_maker
from kbds import reply
from utils.search import set_is_demo

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart(), isRegistered(session_maker()))
async def start(mess: types.Message):
    set_is_demo(False)
    await mess.answer(text='Привет! Meetvibe - это бот для знакомств по интересам', reply_markup=reply.kb_menu)

@dp.message((F.text == 'Главное меню') | (F.text == 'Выйти'))
async def main_menu(mess: types.Message):
    await mess.answer(text='Главное меню:', reply_markup=reply.kb_menu)

@dp.message(Command('demo'))
async def demo(mess: types.Message):
    set_is_demo(True)
    await mess.answer(text='Демо режим включен', reply_markup=reply.kb_menu)

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