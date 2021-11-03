import os, random

import requests
import json
from io import StringIO
import base64
from PIL import Image
from io import BytesIO

import time 

from db.worker import createOne
from db.worker import findOne
from db.worker import update
from db.worker import deleteOne

from db.mongo_collections import waifus
from bson import ObjectId

from .api import get_girls

def store_girls():
    for girl in get_girls():
        createOne({'image' : girl, "born" : int(time.time())}, waifus)

def ensure_girls():
    query = {
        "owner_id" : {
            "$exists": False
            }
        }

    waifu = findOne(query, waifus)
    try:
        img = waifu['image']
    except TypeError:
        store_girls()

def get_waifu(message):
    ensure_girls()
    empty_waifu = {"owner_id" : {"$exists": False}}
    try:
        user_waifu = {"owner_id" : message.from_user.id}
        waifu = findOne(user_waifu, waifus)
        img = waifu['image']
        own_waifu = waifu
        return own_waifu
    except TypeError:
        ensure_girls()
        empty_waifu = {"owner_id" : {"$exists": False}}
        waifu = findOne(empty_waifu, waifus)
        own_waifu = update({"_id" : ObjectId(waifu['_id'])}, {"owner_id" : message.from_user.id}, waifus)
        return own_waifu

def get_waifu_by_chat_id(chat_id):
    user_waifu = {"owner_id" : chat_id}
    return findOne(user_waifu, waifus)

def change_waifu_photo(message, b64_image):
    own_waifu = update({"owner_id" : message.from_user.id}, {"image" : b64_image}, waifus)

def refresh_waifu(message):
    ensure_girls()
    empty_waifu = {"owner_id" : {"$exists": False}}
    waifu = findOne(empty_waifu, waifus)
    own_waifu = update({"owner_id" : message.from_user.id}, {"image" : waifu['image']}, waifus)
    deleteOne({"_id" : ObjectId(waifu['_id'])}, waifus)