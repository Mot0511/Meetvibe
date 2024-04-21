from aiogram import Router, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart
from aiogram import types
from db.orm_query import add_user
from kbds import reply
from sqlalchemy.ext.asyncio import AsyncSession

from utils.get_city import get_city

register_router = Router()

class Profile(StatesGroup):
    name = State()
    age = State()
    gender = State()
    city = State()
    location = State()
    school = State()
    hobbies = State()

@register_router.message(CommandStart())
async def start(mess: types.Message, state: FSMContext):
    await mess.answer(text='Привет! Meetvibe - это бот для знакомств по интересам', reply_markup=reply.remove)

    await mess.answer(text='Я вижу, что ты здесь впервые. Давай создадим анкету')
    await mess.answer(text='Как тебя зовут?')
    await state.set_state(Profile.name)

@register_router.message(Profile.name, F.text)
async def start(mess: types.Message, state: FSMContext):
    await state.update_data(name=mess.text)

    await mess.answer(text='Сколько тебе лет?')
    await state.set_state(Profile.age)

@register_router.message(Profile.age, F.text)
async def start(mess: types.Message, state: FSMContext):
    await state.update_data(age=mess.text)

    await mess.answer(text='Какой у тебя пол', reply_markup=reply.get_keyboard('Мужской', 'Женский'))
    await state.set_state(Profile.gender)

@register_router.message(Profile.gender, F.text)
async def start(mess: types.Message, state: FSMContext):
    await state.update_data(gender=mess.text)

    await mess.answer(text='В каком городе вы живете?', reply_markup=reply.kb_location)
    await mess.answer(text='Ты можешь отправить свою геопозицию для подбора людей ближе к тебе')
    await state.set_state(Profile.city)

@register_router.message(Profile.city, F.text)
async def start(mess: types.Message, state: FSMContext):
    await state.update_data(city=mess.text)
    await state.update_data(location='')

    await mess.answer(text='В какой школе ты учишься? (номер школы)', reply_markup=reply.remove)
    await state.set_state(Profile.school)

@register_router.message(Profile.city, F.location)
async def start(mess: types.Message, state: FSMContext):
    await state.update_data(location=str(dict(mess.location)))
    city = get_city(str(mess.location.latitude), str(mess.location.longitude))
    await state.update_data(city=city)

    await mess.answer(text='В какой школе ты учишься? (номер школы)')
    await state.set_state(Profile.school)

@register_router.message(Profile.school, F.text)
async def start(mess: types.Message, state: FSMContext):
    await state.update_data(school=int(mess.text))

    await mess.answer(text='Какие у тебя увлечения? (перечисли через запятую)')
    await state.set_state(Profile.hobbies)

@register_router.message(Profile.hobbies, F.text)
async def start(mess: types.Message, state: FSMContext, session: AsyncSession):
    hobbies = mess.text.split(', ')
    await state.update_data(hobbies=str(hobbies))

    data = await state.get_data()
    await add_user(session, data)

    await mess.answer(text='Анкета создана', reply_markup=reply.remove)
    await state.clear()