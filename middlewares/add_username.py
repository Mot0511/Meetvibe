from sqlalchemy import update
from sqlalchemy.ext.asyncio import async_sessionmaker
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from typing import Dict, Any

from db.models import Profile

class AddUsername(BaseMiddleware):
    def __init__(self, session_maker: async_sessionmaker):
        self.session_maker = session_maker

    async def __call__(
        self,
        handler,
        event: TelegramObject,
        data: Dict[str, Any]
    ):
        async with self.session_maker() as session:
            
            query = update(Profile).where(Profile.user_id == event.message.from_user.id).values(
                username = event.message.from_user.username
            )
            await session.execute(query)
            await session.commit()

            return await handler(event, data)