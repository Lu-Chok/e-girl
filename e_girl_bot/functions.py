from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from dataclasses import dataclass

import requests
import base64
import io
import os

from PIL import Image

HOSTNAME = os.environ['API_HOSTNAME']

def keyboard(input):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for name in input:
        keyboard.add(name)
    return keyboard


def removeKeyboard():
    keyboard = types.ReplyKeyboardRemove()
    return keyboard


def decode_img(image):
    return io.BytesIO(base64.b64decode(image))

def pretty(s, l=10):
    l += 2
    s = str(s)
    d = ' '
    diff = l - len(s)
    s += d * diff
    return s

def bar(num, l=10):
    d = '-'
    e = '▄'
    bar = f"[{e * num}{d * (l - num)}]"
    return bar

@dataclass
class WaifuActions:
    def feed(owner : str):
        waifu = requests.get(f"{HOSTNAME}/v1/waifu/feed?user={owner}").json()
        return waifu

    def pet(owner : str):
        waifu = requests.get(f"{HOSTNAME}/v1/waifu/pet?user={owner}").json()
        return waifu

    def satisfy(owner : str):
        waifu = requests.get(f"{HOSTNAME}/v1/waifu/satisfy?user={owner}").json()
        return waifu

    def drop(owner : str):
        waifu = requests.get(f"{HOSTNAME}/v1/waifu/drop?user={owner}").json()
        return waifu

    def get_waifu(owner : str):
        waifu = requests.get(f"{HOSTNAME}/v1/waifu?user={owner}").json()
        image =decode_img( waifu.get("image", None))
        waifu['_image'] = image
        return waifu
    
    def name(owner, name):
        response = requests.get(f"{HOSTNAME}/v1/waifu/name?user={owner}&name={name}").json()
        return response