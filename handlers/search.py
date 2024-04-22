from aiogram import Router, F, types


search_router = Router()

@search_router.message(F.text == 'Начать поиск')
async def search(mess: types.Message):
    pass