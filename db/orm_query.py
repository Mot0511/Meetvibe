from db.models import Profile
from sqlalchemy.ext.asyncio import AsyncSession

async def add_user(session: AsyncSession, data):
    obj = Profile(
        **data
    )
    session.add(obj)
    await session.commit()