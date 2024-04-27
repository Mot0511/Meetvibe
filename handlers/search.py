import json
from aiogram import Router, F, types
from utils.search import search
from aiogram.enums.parse_mode import ParseMode
from kbds import reply
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

search_router = Router()

@search_router.message(F.text == 'Начать поиск')
async def start_search(mess: types.Message):
    await mess.answer(text='Выбери пол', reply_markup=reply.kb_gender)
    
@search_router.message((F.text == 'Мужской') | (F.text == 'Женский'))
async def start_search(mess: types.Message, session: AsyncSession):
    users = await search(mess.from_user.id, mess.text, session)

    for user in users:
        hobbies_str = ''
        print(user.hobbies)
        for hobby in json.loads(user.hobbies):
            hobbies_str += hobby + ', '

        await mess.answer_photo(photo=user.photo, caption=f'\
<b>{user.name}</b>, <b>{int(user.age)} лет</b>, <b>{user.city}</b>{f', 📍<b>{user.distance} м</b>' if user.distance != 12000000 else '' }\n\
{( user.school and f'<b>Школа: {int(user.school)}</b>\n')}\
<b>Схожесть интересов: {user.hobbies_prop} %</b>\n\
<b>Интересы: {hobbies_str}</b>\n\
{(user.description and user.description)}', parse_mode=ParseMode.HTML)

# , reply_markup=reply.get_keyboard('✅', '❌')