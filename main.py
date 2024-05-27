import asyncio

from sqlalchemy import update
from config import DEV, ISDEV, TOKEN
from db.models import Profile
from filters.isRegistered import isRegistered
from middlewares.add_username import AddUsername
from middlewares.db import DatabaseSession
from aiogram import F, Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from handlers.profile import register_router
from handlers.search import search_router
from handlers.stats import stats_router
from db.engine import create_db, session_maker
from kbds import reply
from aiogram.fsm.context import FSMContext
# from middlewares.get_album import AlbumMiddleware
from utils.search import set_is_demo

# Bot and dispatcher initialization

bot = Bot(token=(DEV if ISDEV=='TRUE' else TOKEN))
dp = Dispatcher()

# Start handler
@dp.message(CommandStart(), isRegistered(session_maker()))
async def start(mess: types.Message, state: FSMContext):
    print(mess.from_user.url)
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
async def demo(mess, session):
   obj = Profile(
       user_id = 1634061373,
       name = 'Пидор',
       age = 14,
       gender = 'Мужской',
       city = 'Киров',
       school = 25,
       hobbies = '["\u0448\u0430\u0445\u043c\u0430\u0442\u044b", "\u0433\u0438\u0442\u0430\u0440\u0430", "\u0445\u0437", "\u043a\u043e\u043d\u0435\u0447\u043d\u043e", "\u0441\u0430\u043c\u043e\u043a\u0430\u0442"]',
       description = 'Я тупой,но прикольный(наверное)',
       photo = 'AgACAgIAAxkBAAJB8mZTeBw6e_tAX2__KlHuAvFQp1hWAAI42DEbG0CYShU7e-BJ9mrGAQADAgADeQADNQQ',
       username = 'Gitler1109',
       location = ''

   )
   obj2 = Profile(
       user_id = 6243330468,
       name = 'Vlad',
       age = 14,
       gender = 'Мужской',
       city = 'Киров',
       location = '[58.596025, 49.602337]',
       school = 25,
       hobbies = '["\u043a\u0430\u0442\u0430\u044e\u0441\u044c \u043d\u0430 \u043f\u0438\u0442\u0435"]',
       description = '',
       photo = 'AgACAgIAAxkBAAI7n2ZQf8ziUgLOCSEdiRkLh_PuEvQgAAIC3DEbZdyJSgE8t1prFHeFAQADAgADeQADNQQ ',
       username = 'Abobys228853'
   )

   session.add(obj)
   session.add(obj2)
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

    # Including middlewares
    dp.update.middleware(DatabaseSession(session_maker=session_maker))  # for sessions
    dp.update.middleware(AddUsername(session_maker=session_maker))  # for adding usernames
    # dp.update.middleware(AlbumMiddleware())  # for getting albums

    # Startng bot
    await dp.start_polling(bot)
    
# Running app
asyncio.run(main())