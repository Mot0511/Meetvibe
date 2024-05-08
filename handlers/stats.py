from aiogram import Router
from aiogram.filters import Command
from aiogram import types
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.enums.parse_mode import ParseMode
from db.orm_query import get_users_count
from aiogram.fsm.context import FSMContext

stats_router = Router()

@stats_router.message(Command('stats'))
async def get_stats(mess: types.Message, session: AsyncSession, state: FSMContext):
    await state.clear()
    users_count = await get_users_count(session)
    await mess.answer(text=f'<b>Статистика:</b>\n\n\
Количество сторонних пользователей: {users_count - 10}', parse_mode=ParseMode.HTML)