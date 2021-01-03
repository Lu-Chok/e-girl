from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

def keyboard(input):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for name in input:
        keyboard.add(name)
    return keyboard


def removeKeyboard():
    keyboard = types.ReplyKeyboardRemove()
    return keyboard