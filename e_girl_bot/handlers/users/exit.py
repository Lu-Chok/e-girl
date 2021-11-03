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

@dp.message_handler(commands=['start', 'help'], state="*")
async def help(message: types.Message, state: FSMContext):
    await message.reply(f'''Помощь с <a href="https://telegra.ph/Moya-nasha-vajfu-01-08">командами </a>''', reply=False, parse_mode="HTML")

    
