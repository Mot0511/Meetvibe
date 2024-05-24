from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_allow_kb(user_id):
    kb_allow = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='✅', callback_data=f'allow_{user_id}'),
            InlineKeyboardButton(text='❌', callback_data=f'reject'),
        ]
    ])

    return kb_allow

def get_link(text, link):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=text, url=link),
        ]
    ])
    return kb