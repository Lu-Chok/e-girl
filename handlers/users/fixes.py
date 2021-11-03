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

from girls.girls_vending_machine import get_random_girl
mainMenuButtons = types.ReplyKeyboardRemove()

def fix(user, meessage):
    try:
        name = findOne({'chat_id' : user}, user_collection)['name']
    except KeyError:
        update({'chat_id' : user},
            {
                "name" : 'Вайфу',
                "health" : 10,
                "love" : "Безгранична" 
            }, user_collection)

