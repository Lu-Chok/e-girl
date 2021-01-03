from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from loader import dp

from functions import keyboard
from functions import removeKeyboard

mainMenuButtons = keyboard([
    "Моя вайфу"
    ]
)

async def mainMenu(message, text='Главное меню'):
    await message.reply(text, reply_markup=mainMenuButtons, reply=False)

@dp.message_handler(text="Моя вайфу", state="*")
async def exit(message: types.Message, state: FSMContext):
    from .router import my_girl
    await my_girl(message, state)

@dp.message_handler(text=["Моя баба", "моя баба"], state="*")
async def exit(message: types.Message, state: FSMContext):
    from .router import my_girl
    await my_girl(message, state)
