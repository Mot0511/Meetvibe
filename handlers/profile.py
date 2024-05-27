import json
from aiogram import Bot, Router, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, Command
from aiogram import types
from aiogram.enums.parse_mode import ParseMode
from config import DEV, ISDEV, TOKEN
from db.orm_query import add_user, edit_user, get_user
from kbds import reply
from sqlalchemy.ext.asyncio import AsyncSession
from utils.get_city import get_city
from utils.get_info import get_info

bot = Bot(token=(DEV if ISDEV=='TRUE' else TOKEN))
register_router = Router()

# My profile handler
@register_router.message(F.text == 'Моя анкета')
async def profile(mess: types.Message, session: AsyncSession):
    profile = await get_user(session, mess.from_user.id)
    profile.distance = 12000000

    await mess.answer_photo(photo=profile.photo, caption=get_info(profile), parse_mode=ParseMode.HTML, reply_markup=reply.get_keyboard('Изменить анкету', 'Главное меню'))

# State for user data
class Profile(StatesGroup):
    user_id = State()
    username = State()
    name = State()
    age = State()
    gender = State()
    city = State()
    location = State()
    school = State()
    hobbies = State()
    photo = State()
    description = State()
    isEditing = State(state=False)

# Reset state
@register_router.message(Command('reset'))
async def name(mess: types.Message, state: FSMContext):
    await state.clear()
    await mess.answer(text='Состояние сброшено')

# Start handler for unregistered user
@register_router.message(CommandStart())
async def start(mess: types.Message, state: FSMContext):
    await mess.answer(text='Привет! Meetvibe - это бот для знакомств по интересам', reply_markup=reply.kb_menu)

    await mess.answer(text='Я вижу, что ты здесь впервые. Давай создадим анкету')
    await mess.answer(text='Как тебя зовут?', reply_markup=reply.remove)
    await state.update_data(isEditing=False)
    await state.set_state(Profile.name)

# Handlers for getting user data
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
    await state.update_data(gender=mess.text.capitalize())

    await mess.answer(text='В каком городе ты живешь?', reply_markup=reply.kb_location)
    await mess.answer(text='Ты можешь отправить свою геопозицию для подбора людей ближе к тебе')
    await state.set_state(Profile.city)

@register_router.message(Profile.city, F.text)
async def city(mess: types.Message, state: FSMContext):
    await state.update_data(city=mess.text.capitalize())
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
        await state.update_data(school=(mess.text if mess.text.isdigit() else mess.text.upper()))
    else:
        await state.update_data(school='')

    await mess.answer(text='Какие у тебя увлечения? (перечисли через запятую)\n<i>Например: шахматы, велосипед, музыка</i>', reply_markup=reply.remove, parse_mode=ParseMode.HTML)
    await state.set_state(Profile.hobbies)


@register_router.message(Profile.hobbies, F.text)
async def hobbies(mess: types.Message, state: FSMContext):
    hobbies = mess.text.split(', ')
    hobbies = [hobby.lower() for hobby in hobbies]
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

@register_router.message(Profile.photo, F.media_group_id)
async def photo(mess: types.Message):
    await mess.answer('Пока можно загружать только одно фото')

@register_router.message(Profile.photo, F.photo)
async def photo(mess: types.Message, state: FSMContext, session: AsyncSession):
    await state.update_data(photo=mess.photo[-1].file_id)

    await state.update_data(user_id=mess.from_user.id)
    await state.update_data(username=mess.from_user.username)
    data = await state.get_data()

    if (data['isEditing'] == True):
        await edit_user(session, data)
        await mess.answer(text='Анкета изменена', reply_markup=reply.kb_menu)
    else:
        await add_user(session, data)
        await mess.answer(text='Анкета создана', reply_markup=reply.kb_menu)
    
    await state.clear()

    # Showing new person to admin (me)
    user = await get_user(session, data['user_id'])
    user.distance = 12000000
    await bot.send_message(chat_id=1086904500, text='<b>Новый пользователь:</b>', parse_mode=ParseMode.HTML)
    await bot.send_photo(chat_id=1086904500, photo=user.photo, caption=get_info(user), parse_mode=ParseMode.HTML)