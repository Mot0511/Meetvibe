import json
from sqlalchemy import and_, select, func
from db.orm_query import get_user, get_users
from schemas.Profile import Profile
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import Profile
from aiogram.fsm.context import FSMContext

from utils.get_distance import get_distance
from utils.get_hobbies_prop import get_hobbies_prop


async def search(id: int, gender: str, session: AsyncSession):
    userdata = await get_user(session, id)
    age = userdata.age
    city = userdata.city

    query = select(Profile).order_by(func.random()).where( and_(Profile.gender == gender, Profile.age >= (age - 2), Profile.age <= (age + 2), Profile.city == city, Profile.user_id != id))
    users = await get_users(session, query)

    users = add_distances(userdata, users)
    users = add_hobbies_props(userdata, users)

    users_my_school = sort([user for user in users if user.school == userdata.school])
    users_other_school = sort([user for user in users if not user.school == userdata.school])
    
    users_my_school.extend(users_other_school)

    return users_my_school

def sort(users):
    N = len(users)

    for i in range(N-1):
        for j in range(N-1-i):
            if users[j].hobbies_prop < users[j+1].hobbies_prop:
                users[j], users[j+1] = users[j+1], users[j]

    return users

def add_hobbies_props(userdata, users):
    hobbies1 = set(json.loads(userdata.hobbies))
    
    res = []
    for user in users:
        hobbies2 = set(json.loads(user.hobbies))
        prop = get_hobbies_prop(hobbies1, hobbies2)
        user.hobbies_prop = prop
        res.append(user)
    
    return res

def add_distances(userdata, users):
    res = []
    for user in users:
        if userdata.location and user.location:
            location1 = json.loads(userdata.location)
            location2 = json.loads(user.location)
            distance = get_distance(location1, location2)
            user.distance = distance
        else:
            user.distance = 12000000
        
        res.append(user)
    
    return res

# ["\u0444\u0443\u0442\u0431\u043e\u043b", "\u0441\u043f\u043e\u0440\u0442"]