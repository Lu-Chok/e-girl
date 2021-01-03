from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from loader import dp
from pprint import pprint
import re

from handlers.users.exit import mainMenu

# async def sendQuestion(block, message):
#     if 'possible' in current_block.keys():
#         return await message.reply(current_block['text'], reply_markup=keyboard(current_block['possible']), reply=False)
#     else:
#         return await message.reply(current_block['text'], reply=False)


def keyboard(input):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for name in input:
        keyboard.add(name)
    return keyboard


def removeKeyboard():
    keyboard = types.ReplyKeyboardRemove()
    return keyboard


def find_in_dict(d, key, value):
    return list(x for x in d if key in x.keys() and x[key] == value)


def find_one_in_dict(d, key, value):
    return list(x for x in d if key in x.keys() and x[key] == value)[0]


async def save(state):
    data = await state.get_data()
    del data['current_block']
    pprint(data)

async def sendMsg(message, current_block):
    if len(current_block['possible']) == 0:
        return await message.reply(current_block['text'], reply=False)
    else:
        return await message.reply(current_block['text'], reply_markup=keyboard(current_block['possible']), reply=False)

def getRegex(current_block):
    regex = ''
    if 'regex' in current_block.keys():
        regex = current_block['regex']
    else:
        if len(current_block['possible']) == 0:
            regex = '.*'
        else:
            regex += '|'.join(current_block['possible'])
    return regex


def getByeText(current_block):
    if 'bye_text' in current_block.keys():
        return current_block['bye_text']
    else:
        return 'отвечай кнопками'

async def block(message, state, questions):
    data = await state.get_data()
    current_block = data['current_block']
    print(current_block)
    
    print(getRegex(current_block))
    if bool(re.match(getRegex(current_block), message.text)):
        next_block = find_one_in_dict(questions, 'id', current_block['next'])
        
        if(next_block['id'] == 0):
            await save(state)
            await mainMenu(message, next_block['text'])
            return await state.finish()
        else:
            last_block = current_block
            await state.update_data(current_block=next_block)
            return await sendMsg(message, next_block)
    else:
        await message.reply(getByeText(current_block))
        return
        # if len(current_block['possible'])== 0:
        #     return await message.reply(current_block['text'], reply_markup=keyboard(current_block['possible']), reply=False)

    # if current_block['type'] == "question":
    #     if message.text in current_block['possible']:
    #         # handle last block
    #         if current_block['next'] != 0:
    #             last_block = current_block
    #             current_block = find_one_in_dict(questions, 'id', current_block['next'])
    #             await state.update_data(current_block=current_block)
    #             await state.update_data({f"{last_block['result']}" : message.text})
    #             return await message.reply(current_block['text'], reply_markup=keyboard(current_block['possible']), reply=False)
    #         else:
    #             last_block = current_block
    #             current_block = find_one_in_dict(questions, 'id', current_block['next'])
    #             await state.update_data({f"{last_block['result']}" : message.text})
    #             # await message.reply(current_block['text'], reply=False)
    #             await save(state)
    #             await mainMenu(message, current_block['text'])
    #             return await state.finish()
    #     else:
    #         if (len(current_block['possible']) == 0):
    #             last_block = current_block
    #             current_block = find_one_in_dict(questions, 'id', current_block['next'])
    #             if (current_block['id'] == 0):
    #                 # await state.update_data(current_block=current_block)
    #                 await state.update_data({f"{last_block['result']}" : message.text})
    #                 await save(state)
    #                 await mainMenu(message, current_block['text'])
    #                 return await state.finish()
    #             else:
    #                 await state.update_data(current_block=current_block)
    #                 await state.update_data({f"{last_block['result']}" : message.text})
    #                 return await message.reply(current_block['text'], reply_markup=keyboard(current_block['possible']), reply=False)
    #         else:
    #             await message.reply('отвечай кнопками')
    #             return

    # elif current_block['type'] == "routingQuestion":
    #     current_block['possible_str'] = []
    #     for i in current_block['possible']:
    #         current_block['possible_str'].append(i['text'])

    #     if message.text in current_block['possible_str']:
    #         last_block = current_block
    #         current_block['next'] = find_one_in_dict(current_block['possible'], 'text', message.text)['next']
    #         current_block = find_one_in_dict(questions, 'id', current_block['next'])
    #         await message.reply(current_block['text'], reply_markup=keyboard(current_block['possible']), reply=False)
    #         await state.update_data({f"{last_block['result']}" : message.text})
    #         return await state.update_data(current_block=current_block)
    #     else: 
    #         await message.reply('отвечай кнопками')
    #         return

# async def block(message, state, questions):
#     data = await state.get_data()
#     current_block = data['current_block']
#     if current_block['type'] == "question":
#         if message.text in current_block['possible']:
#             # handle last block
#             if current_block['next'] != 0:
#                 last_block = current_block
#                 current_block = find_one_in_dict(questions, 'id', current_block['next'])
#                 await state.update_data(current_block=current_block)
#                 await state.update_data({f"{last_block['result']}" : message.text})
#                 return await message.reply(current_block['text'], reply_markup=keyboard(current_block['possible']), reply=False)
#             else:
#                 last_block = current_block
#                 current_block = find_one_in_dict(questions, 'id', current_block['next'])
#                 await state.update_data({f"{last_block['result']}" : message.text})
#                 # await message.reply(current_block['text'], reply=False)
#                 await save(state)
#                 await mainMenu(message, current_block['text'])
#                 return await state.finish()
#         else: 
#             if (len(current_block['possible']) == 0):
#                 last_block = current_block
#                 current_block = find_one_in_dict(questions, 'id', current_block['next'])
#                 if (current_block['id'] == 0):
#                     # await state.update_data(current_block=current_block)
#                     await state.update_data({f"{last_block['result']}" : message.text})
#                     await save(state)
#                     await mainMenu(message, current_block['text'])
#                     return await state.finish()
#                 else:
#                     await state.update_data(current_block=current_block)
#                     await state.update_data({f"{last_block['result']}" : message.text})
#                     return await message.reply(current_block['text'], reply_markup=keyboard(current_block['possible']), reply=False)
#             else:
#                 await message.reply('отвечай кнопками')
#                 return

#     elif current_block['type'] == "routingQuestion":
#         current_block['possible_str'] = []
#         for i in current_block['possible']:
#             current_block['possible_str'].append(i['text'])

#         if message.text in current_block['possible_str']:
#             last_block = current_block
#             current_block['next'] = find_one_in_dict(current_block['possible'], 'text', message.text)['next']
#             current_block = find_one_in_dict(questions, 'id', current_block['next'])
#             await message.reply(current_block['text'], reply_markup=keyboard(current_block['possible']), reply=False)
#             await state.update_data({f"{last_block['result']}" : message.text})
#             return await state.update_data(current_block=current_block)
#         else: 
#             await message.reply('отвечай кнопками')
#             return