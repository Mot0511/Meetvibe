import asyncio
from profile import Profile

from sqlalchemy import update
from config import TOKEN
from filters.isRegistered import isRegistered
from middlewares.db import DatabaseSession
from aiogram import F, Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from handlers.profile import register_router
from handlers.search import search_router
from handlers.stats import stats_router
from db.engine import create_db, session_maker
from kbds import reply
from aiogram.fsm.context import FSMContext
from utils.search import set_is_demo

# Bot and dispatcher initialization
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Start handler
@dp.message(CommandStart(), isRegistered(session_maker()))
async def start(mess: types.Message, state: FSMContext):
    set_is_demo(False)
    await state.clear()
    await mess.answer(text='Привет! Meetvibe - это бот для знакомств по интересам', reply_markup=reply.kb_menu)

# Menu handler
@dp.message((F.text == 'Главное меню') | (F.text == 'Выйти'))
async def main_menu(mess: types.Message, state: FSMContext):
    await state.clear()
    await mess.answer(text='Главное меню:', reply_markup=reply.kb_menu)

# Demo mode handler
@dp.message(Command('demo'))
async def demo(mess: types.Message, state: FSMContext):
    await state.clear()
    set_is_demo(True)
    await mess.answer(text='Демо режим включен', reply_markup=reply.kb_menu)

@dp.message(Command('fix'))
async def fix(mess, session):
    query1 = update(Profile).where(Profile.user_id == 1194825216).values(
        gender = 'Женский'
    )
    query2 = update(Profile).where(Profile.user_id == 1351119439).values(
        city = 'Киров'
    )
    query3 = update(Profile).where(Profile.user_id == 945631080).values(
        city = 'Киров'
    )
    await session.execute(query1)
    await session.execute(query2)
    await session.execute(query3)
    await session.commit()

    await mess.answer(text='Fixed')


# Including routers
dp.include_router(stats_router)
dp.include_router(register_router)
dp.include_router(search_router)

# Creating bd tables on startup
async def on_startup():
    # await drop_db()
    await create_db()

# Logging about shutdown
async def on_shutdown():
    print('Bot is down')

async def main():
    # Registering startup and shutdown functions
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    # Including middleware for session
    dp.update.middleware(DatabaseSession(session_maker=session_maker))

    # Startng bot
    await dp.start_polling(bot)
    
# Running app
asyncio.run(main())