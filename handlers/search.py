import json
import random
from config import DEV, ISDEV, TOKEN
from aiogram import Bot, Router, F, types
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from kbds import reply, inline
from sqlalchemy.ext.asyncio import AsyncSession
from db.orm_query import get_user
from utils.get_distance import get_distance
from utils.get_info import get_info
from utils.search import search

bot = Bot(token=(DEV if ISDEV=='TRUE' else TOKEN))
search_router = Router()

class QueueState(StatesGroup):
    users = State()
    current_user = State()
    num = State()

# Search handlers
@search_router.message(F.text == 'Начать поиск')
async def start_search(mess: types.Message):
    await mess.answer(text='Выбери пол', reply_markup=reply.kb_gender)
    
@search_router.message((F.text == 'Мужской') | (F.text == 'Женский'))
async def start_search(mess: types.Message, session: AsyncSession, state: FSMContext):
    users = await search(mess.from_user.id, mess.text, session)  # getting users
    
    if not users:
        await mess.answer(text='Нет подходящих пользователей, можешь попробовать изменить критерии поиска', reply_markup=reply.kb_menu)

    await state.update_data(users=users, num=0)

    # Showing person
    await show_person(users[0], mess, state)

# Handler of allowing person
@search_router.message(F.text == '✅')
async def allow(mess: types.Message, state: FSMContext, session: AsyncSession):
    queue_data = await state.get_data()
    current_user = queue_data['current_user']
    user = await get_user(session, mess.from_user.id)
    user.distance = get_distance(json.loads(user.location), json.loads(current_user.location)) if current_user.location else 12000000

    await bot.send_message(current_user.user_id, text='<b>Ты кому-то понравился(ась)</b>:', parse_mode=ParseMode.HTML)
    await bot.send_photo(current_user.user_id, photo=user.photo, caption=get_info(user), parse_mode=ParseMode.HTML, reply_markup=inline.get_allow_kb(mess.from_user.id))
    # await send_request({
    #     'to_id': 1086904500,
    #     'from_id': mess.from_user.id,
    # }, session)
    await next(mess, state)

# Handler of rejecting person
@search_router.message((F.text == '❌') | (F.text == 'Дальше'))
async def next(mess: types.Message, state: FSMContext):
    queue_state = await state.get_data()

    users = queue_state['users']
    num = queue_state['num']

    if num == len(users) - 1:
        await mess.answer(text='Ты просмотрел всех доступных пользователей, можешь начать поиск заново', reply_markup=reply.kb_menu)
        state.clear()
        return

    num += 1
    await state.update_data(num=num)
    await show_person(users[num], mess, state)

# Callback handler of allowing person
@search_router.callback_query(F.data.startswith('allow_'))
async def callback_allow(callback: types.CallbackQuery, session: AsyncSession):
    # Getting info
    user_id1 = callback.data.split('_')[1]
    user_id2 = callback.from_user.id
    user1 = await get_user(session, user_id=user_id1)
    user2 = await get_user(session, user_id=user_id2)

    
    # Message of pair for first person
    await callback.message.answer(text=f'\
<b>Пара создана:</b>\n\
{user1.name} - @{(user1.username if user1.username else user1.user_id)}\n\
{user2.name} - @{(user2.username if user2.username else user2.user_id)}', parse_mode='html')
    

    # Message of pair for second person
    await bot.send_message(user_id1, text=f'\
<b>Пара создана:</b>\n\
{user2.name} - @{(user2.username if user2.username else user2.user_id)}\n\
{user1.name} - @{(user1.username if user1.username else user1.user_id)}', parse_mode='html')

    await callback.answer()

# Callback handler of rejecting person
@search_router.callback_query(F.data == 'reject')
async def callback_reject(callback: types.CallbackQuery):
    await callback.message.delete()

# Function for showing person
async def show_person(user, mess: types.Message, state: FSMContext):
    # if random.randint(0, 15) == 1:
    #     ad_id = 'AgACAgIAAxkBAAIz92ZQJlqvg-rOkcyf1X7rFM01E9IKAAIQ3jEbssSJSh5UNasHK7JkAQADAgADeAADNQQ'
    #     ad_id_demo = 'AgACAgIAAxkBAAIUM2ZQLp8fJQQdcI3BzAZ3lZHHOL1yAAIQ3jEbssSJSn9fZcCs-lhHAQADAgADeAADNQQ'
    #     await mess.answer_photo(photo=ad_id, caption='Подпишись, пожалуйста, на ТЛШ', reply_markup=inline.get_link('Перейти в канал', 'https://t.me/tls2543'))
    #     return
    
    await state.update_data(current_user=user)
    await mess.answer_photo(photo=user.photo, caption=get_info(user), parse_mode=ParseMode.HTML, reply_markup=reply.kb_select)
