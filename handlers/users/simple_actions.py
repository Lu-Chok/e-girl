from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from loader import dp
import re

from db.worker import createOne
from db.worker import findOne
from db.worker import update
from db.mongo_collections import user as user_collection

from functions import keyboard
from functions import removeKeyboard

from girls.girls_vending_machine_2_0 import get_waifu
from girls.girls_vending_machine_2_0 import change_waifu_photo
from girls.girls_vending_machine_2_0 import refresh_waifu
from girls.girls_vending_machine_2_0 import get_waifu_by_chat_id

from db.roles import get_role

import base64
from io import BytesIO
from PIL import Image

mainMenuButtons = types.ReplyKeyboardRemove()

def get_caption(user, message):
    waifu = findOne({'chat_id' : user}, user_collection)
    if waifu == None:
        waifu = createOne({
            'chat_id' : user,
            'owner' : message.from_user.first_name,
            'name' : "Вайфу",
            "health" : 10,
            "love" : "Безгранична"
        }, user_collection)

    try:
        name = waifu['name']
    except KeyError:
        name = 'Вайфу'
        update({'chat_id' : user}, {"name" : name}, user_collection)

    try:
        health = waifu['health']
    except KeyError:
        health = 10
        update({'chat_id' : user}, {"health" : health}, user_collection)

    try:
        love = waifu['love']
    except KeyError:
        love = 'Безгранична'
        update({'chat_id' : user}, {"love" : love}, user_collection)
    
    try:
        owner = waifu['owner']
        owner_username = waifu['owner_username']
        if owner == message.from_user.first_name and owner_username == message.from_user.username:
            pass
        else:
            raise KeyError('KeyError')
    except KeyError:
        owner = message.from_user.first_name
        update({'chat_id' : user}, {"owner" : message.from_user.first_name, "owner_username" : message.from_user.username}, user_collection)

    caption = []
    caption.append(f'📝 *Имя:* {name}\n')
    caption.append(f'❤️ *Здоровье:* {health}/10')
    caption.append(f'💖 *Любовь:* {love}\n')
    caption.append(f'🏚 *Хозяин:* {owner}')

    return '\n'.join(caption)

def get_caption_chat_id(chat_id):
    waifu = findOne({'chat_id' : chat_id}, user_collection)
    
    caption = []
    caption.append(f"📝 *Имя:* {waifu['name']}\n")
    caption.append(f"❤️ *Здоровье:* {waifu['health']}/10")
    caption.append(f"💖 *Любовь:* {waifu['love']}\n")
    caption.append(f"🏚 *Хозяин:* {waifu['owner']}")

    return '\n'.join(caption)


@dp.message_handler(regexp='[Мм]оя\s(баба|вайфу|девка)', state="*")
async def my_girl(message: types.Message, state: FSMContext):
    waifu = get_waifu(message)
    waifu_photo = BytesIO()
    waifu_photo.name = 'image.jpeg'
    Image.open(BytesIO(base64.b64decode(waifu['image']))).save(waifu_photo, 'JPEG')
    waifu_photo.seek(0)
    with waifu_photo as photo:
        await message.answer_photo(photo=photo, 
        caption=get_caption(message.from_user.id, message), 
        parse_mode="Markdown", 
        reply_markup=mainMenuButtons
    )



@dp.message_handler(regexp='([Чч]покнуть\s).*', state="*")
async def chpok(message: types.Message, state: FSMContext):
    await message.reply(f"{message.from_user.first_name} чпокнул(а) {message.text.split('покнуть ')[1]}", reply=False, parse_mode="HTML")


@dp.message_handler(regexp='([Бб]аба|[Вв]айфу|[Дд]евка)\s@.*', state="*")
async def my_girl(message: types.Message, state: FSMContext):
    find_username = message.text.split('@')[1]
    
    found = findOne({"owner_username" : find_username}, user_collection)
    print(found)
    caption = get_caption_chat_id(found['chat_id'])
    waifu = get_waifu_by_chat_id(found['chat_id'])
    waifu_photo = BytesIO()
    waifu_photo.name = 'image.jpeg'
    Image.open(BytesIO(base64.b64decode(waifu['image']))).save(waifu_photo, 'JPEG')
    waifu_photo.seek(0)
    with waifu_photo as photo:
        await message.answer_photo(photo=photo, 
        caption=caption, 
        parse_mode="Markdown", 
        reply_markup=mainMenuButtons
    )


@dp.message_handler(content_types=['photo'], state="*")
async def my_girl(message: types.Message, state: FSMContext):
    if message.caption.lower() == 'сменить вайфу':
        if get_role(message) == 'vip' or get_role(message) != '' :
            waifu_photo = BytesIO()
            waifu_photo.name = 'image.jpeg'
            await message.photo[-1].download(waifu_photo)
            waifu_photo.seek(0)
            with waifu_photo as image_file:
                data = base64.b64encode(image_file.read()).decode('utf-8')
                change_waifu_photo(message, data)
                await message.answer('Фото вайфу успешно изменено!', parse_mode='HTML', reply=False)
        else:
            await message.answer('У вас недостаточно прав', parse_mode='HTML', reply=False)

@dp.message_handler(regexp='[Т|т]искать', state="*")
async def squeeze(message: types.Message, state: FSMContext):
    await message.reply(f"{message.from_user.first_name} затискал(а) {re.sub(r'[Т|т]искать', '', message.text)}", reply=False, parse_mode="HTML")


@dp.message_handler(regexp='[Дд]ать\s.*\sпо\s(.*)', state="*")
async def punch(message: types.Message, state: FSMContext):
    await message.reply(f"{message.from_user.first_name} дал(а) своей вайфу по {message.text.split('по ')[1]}", reply=False, parse_mode="HTML")


@dp.message_handler(regexp='[Гг]ладить\s.*\sпо\s(.*)', state="*")
async def pet_on(message: types.Message, state: FSMContext):
    await message.reply(f"{message.from_user.first_name} погладил(а) свою вайфу по {message.text.split('по ')[1]}", reply=False, parse_mode="HTML")


@dp.message_handler(regexp='[Гг]ладить', state="*")
async def pet(message: types.Message, state: FSMContext):
    await message.reply(f"{message.from_user.first_name} погладил(а) {message.text.split('ладить ')[1]}", reply=False, parse_mode="HTML") 


@dp.message_handler(regexp='[Оо]тшлепать', state="*")
async def spank(message: types.Message, state: FSMContext):
    await message.reply(f"{message.from_user.first_name} отшлепал(а) свою вайфу", reply=False, parse_mode="HTML")


@dp.message_handler(regexp='[Дд]ать\s.*\sимя\s(.{1,64}$)', state="*")
async def give_name(message: types.Message, state: FSMContext):
    name = message.text.split('имя ')[1]
    update({'chat_id' : message.from_user.id},{"name" : name}, user_collection)
    await message.reply(f"{message.from_user.first_name} дал(а) свое вайфу имя {name}", reply=False, parse_mode="HTML")


@dp.message_handler(regexp='[Оо]бновить вайфу', state="*")
async def refresh(message: types.Message, state: FSMContext):
    refresh_waifu(message)
    await message.reply(f"{message.from_user.first_name} используя душу другой вайфу обновил образ своей девочки", reply=False, parse_mode="HTML")


# @dp.message_handler(regexp='роль', state="*")
# async def give_name(message: types.Message, state: FSMContext):
#     role = get_role(message)
#     if get_role(message) == 'vip':
#     print(role)
#     await message.reply(f"{role}", reply=False, parse_mode="HTML")
