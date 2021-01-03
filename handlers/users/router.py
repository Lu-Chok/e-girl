from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
 
# from aiogram.types import FSInputFile

from loader import dp

from functions import keyboard
from functions import removeKeyboard

mainMenuButtons = keyboard([
    "Моя вайфу"
    ]
)

def get_caption(user):
    caption = []
    caption.append('📝 *Имя:* Вайфу\n')
    caption.append('❤️ *Здоровье:* 10/10')
    caption.append('💖 *Любовь:* Безгранична')
    return '\n'.join(caption)

from girls.girls_vending_machine import get_random_girl

async def my_girl(message: types.Message, state: FSMContext):
    own_girl = get_random_girl(message.from_user.id)
    girl_path = own_girl['path']
    with open(girl_path,'rb') as photo:
        await message.answer_photo(photo=photo, caption=get_caption(message.from_user.id), parse_mode="Markdown", reply_markup=mainMenuButtons)