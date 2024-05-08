from aiogram.filters import Filter
from aiogram import types
from sqlalchemy.ext.asyncio import AsyncSession
from db.orm_query import get_all_ids

# Filter for define: user is registered or not
class isRegistered(Filter):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def __call__(self, mess: types.Message):
        user_ids = await get_all_ids(session=self.session)
        return mess.from_user.id in user_ids