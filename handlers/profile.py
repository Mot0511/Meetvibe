import json
from atexit import register
from aiogram import Router, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, Command
from aiogram import types
from db.orm_query import add_user, edit_user, get_user
from kbds import reply
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.enums.parse_mode import ParseMode

from utils.get_city import get_city

register_router = Router()

@register_router.message(F.text == 'Моя анкета')
async def profile(mess: types.Message, session: AsyncSession):
    profile = await get_user(session, mess.from_user.id)

    hobbies_str = ''
    print(profile.hobbies)
    for hobby in json.loads(profile.hobbies):
        hobbies_str += hobby + ', '

    await mess.answer_photo(photo=profile.photo, caption=f'\
<b>{profile.name}</b>, <b>{int(profile.age)} лет</b>, <b>{profile.city}</b>\n\
{( profile.school and f'<b>Школа: {int(profile.school)}</b>\n')}\
<b>Интересы: {hobbies_str}</b>\n\
{(profile.description and profile.description)}', parse_mode=ParseMode.HTML, reply_markup=reply.get_keyboard('Изменить анкету', 'Главное меню'))

class Profile(StatesGroup):
    user_id = State()
    name = State()
    age = State()
    gender = State()
    city = State()
    location = State()
    school = State()
    hobbies = State()
    photo = State()
    description = State()

    isEditing = State()

@register_router.message(Command('reset'))
async def name(mess: types.Message, state: FSMContext):
    await state.clear()
    await mess.answer(text='Состояние сброшено')

@register_router.message(CommandStart())
async def start(mess: types.Message, state: FSMContext):
    await mess.answer(text='Привет! Meetvibe - это бот для знакомств по интересам', reply_markup=reply.kb_menu)

    await mess.answer(text='Я вижу, что ты здесь впервые. Давай создадим анкету')
    await mess.answer(text='Как тебя зовут?', reply_markup=reply.remove)
    await state.set_state(Profile.name)

@register_router.message(StateFilter(None), F.text == 'Изменить анкету')
async def name(mess: types.Message, state: FSMContext):
    await state.update_data(isEditing=True)

    await mess.answer(text='Как тебя зовут?')
    await state.set_state(Profile.name)

@register_router.message(Profile.name, F.text)
async def name(mess: types.Message, state: FSMContext):
    await state.update_data(name=mess.text)

    await mess.answer(text='Сколько тебе лет?')
    await state.set_state(Profile.age)

@register_router.message(Profile.age, F.text)
async def age(mess: types.Message, state: FSMContext):
    await state.update_data(age=mess.text)

    await mess.answer(text='Какой у тебя пол', reply_markup=reply.kb_gender)
    await state.set_state(Profile.gender)

@register_router.message(Profile.gender, F.text)
async def gender(mess: types.Message, state: FSMContext):
    await state.update_data(gender=mess.text)

    await mess.answer(text='В каком городе ты живешь?', reply_markup=reply.kb_location)
    await mess.answer(text='Ты можешь отправить свою геопозицию для подбора людей ближе к тебе')
    await state.set_state(Profile.city)

@register_router.message(Profile.city, F.text)
async def city(mess: types.Message, state: FSMContext):
    await state.update_data(city=mess.text)
    await state.update_data(location='')

    await mess.answer(text='В какой школе ты учишься? (номер школы или аббревитаруа)\nЭто можно указать для более точного поиска.', reply_markup=reply.kb_skip)
    await state.set_state(Profile.school)

@register_router.message(Profile.city, F.location)
async def location(mess: types.Message, state: FSMContext):
    await state.update_data(location=str([mess.location.latitude, mess.location.longitude]))
    city = get_city(str(mess.location.latitude), str(mess.location.longitude))
    await state.update_data(city=city)

    await mess.answer(text='В какой школе ты учишься? (номер школы или аббревитаруа)\nЭто можно указать для более точного поиска', reply_markup=reply.kb_skip)
    await state.set_state(Profile.school)

@register_router.message(Profile.school, F.text)
async def school(mess: types.Message, state: FSMContext):
    if not mess.text == 'Пропустить':
        await state.update_data(school=int(mess.text))
    else:
        await state.update_data(school='')

    await mess.answer(text='Какие у тебя увлечения? (перечисли через запятую)', reply_markup=reply.remove)
    await state.set_state(Profile.hobbies)


@register_router.message(Profile.hobbies, F.text)
async def hobbies(mess: types.Message, state: FSMContext):
    hobbies = mess.text.split(', ')
    await state.update_data(hobbies=json.dumps(hobbies))

    await mess.answer(text='Можешь еще написать описание себя', reply_markup=reply.kb_skip)
    await state.set_state(Profile.description)

@register_router.message(Profile.description, F.text)
async def hobbies(mess: types.Message, state: FSMContext):
    if not mess.text == 'Пропустить':
        await state.update_data(description=mess.text)
    else:
        await state.update_data(description='')

    await mess.answer(text='Отправь свое фото', reply_markup=reply.remove)
    await state.set_state(Profile.photo)
    

@register_router.message(Profile.photo, F.photo)
async def photo(mess: types.Message, state: FSMContext, session: AsyncSession):
    await state.update_data(photo=mess.photo[-1].file_id)

    await state.update_data(user_id=mess.from_user.id)
    data = await state.get_data()

    if (data['isEditing'] == True):
        await edit_user(session, data)
        await mess.answer(text='Анкета изменена', reply_markup=reply.kb_menu)
    else:
        await add_user(session, data)
        await mess.answer(text='Анкета создана', reply_markup=reply.kb_menu)
    
    await state.clear()