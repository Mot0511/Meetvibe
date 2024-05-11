from schemas.Profile import Profile
import json

def get_info(user: Profile, show_username: bool = False):

    hobbies_str = ''
    for hobby in json.loads(user.hobbies):
        hobbies_str += hobby + ', '

    return f'\
<b>{user.name}{(f' (@{user.username})' if show_username and user.username else '')}</b>, <b>{int(user.age)} лет</b>, <b>{user.city}</b>{f", 📍<b>{user.distance} м</b>" if user.distance != 12000000 else "" }\n\
{( user.school and f"<b>Школа: {user.school}</b>")}\n\
<b>Интересы: {hobbies_str}</b>\n\
{(user.description and user.description)}'