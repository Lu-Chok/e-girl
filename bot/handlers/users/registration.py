from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from loader import dp
from pprint import pprint

from blockHandler import block

from scenarios.registration import scenario

from functions import keyboard
from functions import removeKeyboard

def find_one_in_dict(d, key, value):
    return list(x for x in d if key in x.keys() and x[key] == value)[0]


class Init(StatesGroup):
    register_form = State()

current_block = find_one_in_dict(scenario, 'id', 1)

@dp.message_handler(commands=["registration", "start"], state="*")
async def reg_step_1(message: types.Message, state: FSMContext):
    await state.update_data(current_block=current_block)
    await message.reply(current_block['text'], reply_markup=keyboard(current_block['possible']), reply=False)
    await Init.register_form.set()


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=Init.register_form)
async def reg_handler(message: types.Message, state: FSMContext):
    await block(message, state, scenario)