from datetime import datetime
import os, random

import requests
import json
from io import StringIO
import base64
from PIL import Image
from io import BytesIO

import time 

from dataclasses import dataclass

from ..db.worker import createOne
from ..db.worker import findOne
from ..db.worker import update
from ..db.worker import deleteOne

from ..db.mongo_collections import waifu_images
from bson import ObjectId

from .api import get_girls

from logs import logger

from ..config import DEFAULT_HEALTH, DEFAULT_SYMPATHY, DEFAULT_MOOD, DEFAULT_NAME

@dataclass
class WaifuVending:
    def store_girls():
        logger.info(f"Starting girls saving")
        for girl in get_girls():
            createOne({'image' : girl, "born" : int(time.time())}, waifu_images)

    def ensure_girls():
        query = {
            "owner_id" : {
                "$exists": False
                }
            }

        waifu = findOne(query, waifu_images)
        try:
            img = waifu['image']
        except TypeError:
            WaifuVending.store_girls()


    def get_waifu(owner: str):
        WaifuVending.ensure_girls()
        empty_waifu = {"owner_id" : {"$exists": False}}
        try:
            user_waifu = {"owner_id" : owner}
            waifu = findOne(user_waifu, waifu_images)
            img = waifu['image']
            own_waifu = waifu
            return own_waifu
        except TypeError:
            WaifuVending.ensure_girls()
            empty_waifu = {"owner_id" : {"$exists": False}}
            waifu = findOne(empty_waifu, waifu_images)
            own_waifu = update({"_id" : ObjectId(waifu['_id'])}, {
                "owner_id" : owner,
                "name" : DEFAULT_NAME,
                "health" : DEFAULT_HEALTH,
                "sympathy" : DEFAULT_SYMPATHY,
                "mood" : DEFAULT_MOOD,
                "_name_last_update" : datetime.now(),
                "_health_last_update" : datetime.now(),
                "_sympathy_last_update" : datetime.now(),
                "_mood_last_update" : datetime.now()
                }, waifu_images)
            return own_waifu


    def get_waifu_by_chat_id(owner: str):
        user_waifu = {"owner_id" : owner}
        return findOne(user_waifu, waifu_images)


    def change_waifu_photo(owner: str, b64_image):
        own_waifu = update({"owner_id" : owner}, {"image" : b64_image}, waifu_images)

    def update_waifu_fields(owner: str, patch):
        own_waifu = update({"owner_id" : owner}, patch, waifu_images)

    def refresh_waifu(owner: str):
        WaifuVending.ensure_girls()
        waifu = findOne({"owner_id" : owner}, waifu_images)
        deleteOne({"_id" : ObjectId(waifu['_id'])}, waifu_images)