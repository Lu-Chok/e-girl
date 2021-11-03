from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from loader import dp
import re

# from db.worker import createOne
# from db.worker import findOne
# from db.worker import update
# from db.mongo_collections import user as user_collection

from functions import WaifuActions, pretty, bar

# from db.roles import get_role

import base64
from io import BytesIO
from PIL import Image

mainMenuButtons = types.ReplyKeyboardRemove()

def get_caption(user):
    waifu = WaifuActions.get_waifu(user['id'])
    caption = []
    caption.append('```')
    caption.append(f"Имя:         {waifu['name']}")
    caption.append(f"Здоровье:    {bar(waifu['health'] * 2,   20)}")
    caption.append(f"Настроение:  {bar(waifu['mood'] * 2,     20)}")
    caption.append(f"Симпатия:    {bar(waifu['sympathy'] * 2, 20)}")
    if user['id'] == waifu['owner']:
        caption.append(f"Хозяин:      {user['first_name']}")
    caption.append('```')

    return '\n'.join(caption)


@dp.message_handler(regexp='[Мм]оя\s(баба|вайфу|девка)', state="*")
async def my_girl(message: types.Message, state: FSMContext, dbUser: dict):
    waifu = WaifuActions.get_waifu(dbUser['id'])
    waifu_photo = BytesIO()
    waifu_photo.name = 'image.jpeg'
    with Image.open(BytesIO(base64.b64decode(waifu['image']))) as im:
        im.thumbnail(size=(40, 40), resample=Image.NONE)
        im_resized = im.resize((400, 400), Image.NONE)
        im_resized.save(waifu_photo, 'JPEG')
    waifu_photo.seek(0)
    
    with waifu_photo as photo:
        await message.answer_photo(photo=photo, 
        caption=get_caption(dbUser), 
        parse_mode="Markdown", 
        reply_markup=mainMenuButtons
    )



@dp.message_handler(regexp='(по)?[Гг]ладить\s(бабу|Бабу|вайфу|Вайфу|девка|Девку)', state="*")
async def pet_own(message: types.Message, state: FSMContext, dbUser: dict):
    WaifuActions.pet(dbUser['id'])
    await message.reply(f"{message.from_user.first_name} погладил(а) свою {message.text.split('ладить ')[1]}", reply=False, parse_mode="HTML") 


@dp.message_handler(regexp='([Чч]покнуть\s(бабу|Бабу|вайфу|Вайфу|девка|Девку)).*', state="*")
async def chpok_own(message: types.Message, state: FSMContext, dbUser: dict):
    WaifuActions.satisfy(dbUser['id'])
    await message.reply(f"{message.from_user.first_name} чпокнул(а) {message.text.split('покнуть ')[1]}", reply=False, parse_mode="HTML")


@dp.message_handler(regexp='([Пп]окормить\s(бабу|Бабу|вайфу|Вайфу|девка|Девку)).*', state="*")
async def chpok_own(message: types.Message, state: FSMContext, dbUser: dict):
    WaifuActions.feed(dbUser['id'])
    await message.reply(f"{message.from_user.first_name} покормил(а) {message.text.split('кормить ')[1]}", reply=False, parse_mode="HTML")


@dp.message_handler(regexp='[Дд]ать\s.*\sимя\s(.{1,64}$)', state="*")
async def give_name(message: types.Message, state: FSMContext, dbUser: dict):
    name = message.text.split('имя ')[1]
    WaifuActions.name(dbUser['id'], name)
    await message.reply(f"{message.from_user.first_name} дал(а) свое вайфу имя {name}", reply=False, parse_mode="HTML")

@dp.message_handler(regexp='[Оо]бновить\s(бабу|Бабу|вайфу|Вайфу|девка|Девку)', state="*")
async def refresh(message: types.Message, state: FSMContext, dbUser: dict):
    WaifuActions.drop(dbUser['id'])
    await message.reply(f"{message.from_user.first_name} нашел себе девочку помоложе", reply=False, parse_mode="HTML")

@dp.message_handler(regexp='[Бб]росить\s(бабу|Бабу|вайфу|Вайфу|девка|Девку)', state="*")
async def refresh(message: types.Message, state: FSMContext, dbUser: dict):
    WaifuActions.drop(dbUser['id'])
    await message.reply(f"{message.from_user.first_name} бросил свою старую вайфу", reply=False, parse_mode="HTML")




@dp.message_handler(regexp='([Чч]покнуть\s).*', state="*")
async def chpok(message: types.Message, state: FSMContext, dbUser: dict):
    await message.reply(f"{message.from_user.first_name} чпокнул(а) {message.text.split('покнуть ')[1]}", reply=False, parse_mode="HTML")


@dp.message_handler(regexp='[Т|т]искать', state="*")
async def squeeze(message: types.Message, state: FSMContext, dbUser: dict):
    await message.reply(f"{message.from_user.first_name} затискал(а) {re.sub(r'[Т|т]искать', '', message.text)}", reply=False, parse_mode="HTML")


@dp.message_handler(regexp='[Дд]ать\s.*\sпо\s(.*)', state="*")
async def punch(message: types.Message, state: FSMContext, dbUser: dict):
    await message.reply(f"{message.from_user.first_name} дал(а) своей вайфу по {message.text.split('по ')[1]}", reply=False, parse_mode="HTML")


@dp.message_handler(regexp='[Гг]ладить\s.*\sпо\s(.*)', state="*")
async def pet_on(message: types.Message, state: FSMContext, dbUser: dict):
    await message.reply(f"{message.from_user.first_name} погладил(а) свою вайфу по {message.text.split('по ')[1]}", reply=False, parse_mode="HTML")


@dp.message_handler(regexp='(по)?[Гг]ладить\s', state="*")
async def pet(message: types.Message, state: FSMContext, dbUser: dict):
    await message.reply(f"{message.from_user.first_name} погладил(а) {message.text.split('ладить ')[1]}", reply=False, parse_mode="HTML") 


@dp.message_handler(regexp='[Оо]тшлепать', state="*")
async def spank(message: types.Message, state: FSMContext):
    await message.reply(f"{message.from_user.first_name} отшлепал(а) свою вайфу", reply=False, parse_mode="HTML")




# # @dp.message_handler(regexp='роль', state="*")
# # async def give_name(message: types.Message, state: FSMContext):
# #     role = get_role(message)
# #     if get_role(message) == 'vip':
# #     print(role)
# #     await message.reply(f"{role}", reply=False, parse_mode="HTML")


# @dp.message_handler(content_types=['photo'], state="*")
# async def my_girl(message: types.Message, state: FSMContext):
#     if message.caption.lower() == 'сменить вайфу':
#         if get_role(message) == 'vip' or get_role(message) != '' :
#             waifu_photo = BytesIO()
#             waifu_photo.name = 'image.jpeg'
#             await message.photo[-1].download(waifu_photo)
#             waifu_photo.seek(0)
#             with waifu_photo as image_file:
#                 data = base64.b64encode(image_file.read()).decode('utf-8')
#                 change_waifu_photo(message, data)
#                 await message.answer('Фото вайфу успешно изменено!', parse_mode='HTML', reply=False)
#         else:
#             await message.answer('У вас недостаточно прав', parse_mode='HTML', reply=False)
