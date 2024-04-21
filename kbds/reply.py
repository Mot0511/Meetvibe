from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def get_keyboard(
    *btns,
    placeholder: str = None,
    sizes: tuple[int] = (2,),
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

remove = ReplyKeyboardRemove()