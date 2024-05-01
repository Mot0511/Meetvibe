from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from typing import Tuple

def get_keyboard(
    *btns,
    placeholder: str = None,
    sizes: Tuple[int] = (2,),
):
    keyboard = ReplyKeyboardBuilder()
    for btn in btns:
        keyboard.add(KeyboardButton(text=btn))

    return keyboard.adjust(*sizes).as_markup(resize_keyboard=True, input_field_placeholder=placeholder)


kb_location = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='Отправить свою геопозицию', request_location=True),
    ]
], resize_keyboard=True)

kb_menu = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='Начать поиск'),
        KeyboardButton(text='Моя анкета'),
    ]
], resize_keyboard=True)

kb_skip = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='Пропустить'),
    ]
], resize_keyboard=True)

kb_gender = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='Мужской'),
        KeyboardButton(text='Женский'),
    ]
], resize_keyboard=True)

kb_select = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='✅'),
        KeyboardButton(text='❌'),
    ],
    [
        KeyboardButton(text='Выйти')
    ]
], resize_keyboard=True)

remove = ReplyKeyboardRemove()