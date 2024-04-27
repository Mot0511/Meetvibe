from sqlalchemy import select, update
from db.models import Profile
from sqlalchemy.ext.asyncio import AsyncSession

async def add_user(session: AsyncSession, data):
    obj = Profile(
        user_id = data['user_id'],
        name = data['name'],
        age = data['age'],
        gender = data['gender'],
        city = data['city'],
        location = data['location'],
        school = data['school'],
        hobbies = data['hobbies'],
        photo = data['photo'],
        description = data['description'],
    )
    session.add(obj)
    await session.commit()

async def edit_user(session: AsyncSession, data):
    query = update(Profile).where(Profile.user_id == data['user_id']).values(
        user_id = data['user_id'],
        name = data['name'],
        age = data['age'],
        gender = data['gender'],
        city = data['city'],
        location = data['location'],
        school = data['school'],
        hobbies = data['hobbies'],
        photo = data['photo'],
        description = data['description'],
    )
    await session.execute(query)
    await session.commit()

async def get_user(session: AsyncSession, user_id):
    query = select(Profile).where(user_id == user_id)
    data = await session.execute(query)
    print(data)
    return data.scalar()

async def get_users(session: AsyncSession, query):
    data = await session.execute(query)
    return data.scalars().all()

async def get_all_ids(session: AsyncSession):
    query = select(Profile.user_id)
    data = await session.execute(query)
    return data.scalars().all()