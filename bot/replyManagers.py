# -*- coding: utf-8 -*-
import aiogram
import logging
import random
import time
import auth

from aiogram import Bot, Dispatcher, executor, types


API_TOKEN = auth.token
bot = Bot(token=API_TOKEN)

async def giveReply(message, function):
    await bot.send_chat_action(message.chat.id, 'typing')
    time.sleep(random.randint(0, 1))
    return await message.reply(function)


async def giveAnswer(message, function):
    await bot.send_chat_action(message.chat.id, 'typing')
    time.sleep(random.randint(0, 1))
    return await message.answer(function)

async def current_block(message, current_block, state, questions):
    if message.text in current_block['possible']:
        if current_block['next'] != 0:
            last_block = current_block
            current_block = find_one_in_dict(questions, 'id', current_block['next'])
            return await state.update_data(current_block=current_block)
            return await state.update_data({f"{last_block['result']}" : message.text})
            return await message.reply(current_block['text'], reply_markup=keyboard(current_block['possible']), reply=False)
        else:
            last_block = current_block
            current_block = find_one_in_dict(questions, 'id', current_block['next'])
            return await state.update_data({f"{last_block['result']}" : message.text})
            return await message.reply(current_block['text'], reply=False)
            save(data)
            return await state.finish()
    else: 
        await message.reply('отвечай кнопками мудила')