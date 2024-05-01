from filters.isRegistered import isRegistered
from middlewares.db import DatabaseSession
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from handlers.profile import register_router
from handlers.search import search_router
from db.engine import create_db, session_maker
from kbds import reply
from aiogram import F
from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart(), isRegistered(session_maker()))
async def start(mess: types.Message):
    await mess.answer(text='Привет! Meetvibe - это бот для знакомств по интересам', reply_markup=reply.kb_menu)

@dp.message((F.text == 'Главное меню') | (F.text == 'Выйти'))
async def main_menu(mess: types.Message):
    await mess.answer(text='Главное меню:', reply_markup=reply.kb_menu)


dp.include_router(register_router)
dp.include_router(search_router)

async def send_photo(user_id, photo, caption):
    await bot.send_photo(user_id, photo=photo, caption=caption)

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