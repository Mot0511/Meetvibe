import json
from typing import List
from db.orm_query import get_user, get_users
from db.models import Profile
from sqlalchemy import and_, or_, select, func  
from sqlalchemy.ext.asyncio import AsyncSession
from utils.get_distance import get_distance
from utils.get_hobbies_prop import get_hobbies_prop

# State and function for demo mode
isDemo = False
def set_is_demo(mode):
    global isDemo
    isDemo = mode

# Main search code
async def search(id: int, gender: str, session: AsyncSession):
    global isDemo
    # Getting info about user
    userdata = await get_user(session, id)
    age = userdata.age
    city = userdata.city

    # Building query for seacrhing
    query = select(Profile).order_by(func.random()).where( and_(Profile.gender == gender, Profile.age >= (age - 2), Profile.age <= (age + 2), Profile.city == city, Profile.user_id != id))
    if isDemo:
        query = query.where(or_(Profile.user_id == 1, Profile.user_id == 1275580390))  # for demo mode
    else:
        query = query.where(and_(Profile.user_id != 1))  # for normal mode
# , Profile.user_id != 1275580390
    # Getting users
    users = await get_users(session, query)

    # Adding distances and hobbies props for users
    users = add_distances(userdata, users)
    users = add_hobbies_props(userdata, users)

    # Sorting users
    users_my_school = sort([user for user in users if user.school == userdata.school])
    users_other_school = sort([user for user in users if not user.school == userdata.school])
    
    users_my_school.extend(users_other_school)

    return users_my_school

# Function for sorting
def sort(users):
    N = len(users)

    for i in range(N-1):
        for j in range(N-1-i):
            if users[j].hobbies_prop < users[j+1].hobbies_prop:
                users[j], users[j+1] = users[j+1], users[j]

    return users

# Function for adding hobbies props
def add_hobbies_props(userdata, users):
    hobbies1 = set(json.loads(userdata.hobbies))
    
    res = []
    for user in users:
        hobbies2 = set(json.loads(user.hobbies))
        prop = get_hobbies_prop(hobbies1, hobbies2)
        user.hobbies_prop = prop
        res.append(user)
    
    return res

# Function for adding distances
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