# from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware
from aiogram.dispatcher.middlewares import BaseMiddleware
from pprint import pprint

from aiogram import types
from typing import Optional
import requests
import os
import json

API_HOSTNAME = os.environ['API_HOSTNAME']

def sync(user: types.User):
    a = user.as_json()
    headers = { 'Content-Type': 'application/json'}
    response = requests.request("POST", f"{API_HOSTNAME}/v1/user", headers=headers, data=a.encode('utf-8')).json()
    return response


class UserMiddleware(BaseMiddleware):
    async def setup_language(self, data: dict, user: types.User, message: types.Message ,chat: Optional[types.Chat] = None):
        dbUser = sync(user)
        # print(user)

        data["dbUser"] = dbUser
    async def on_pre_process_message(self, message: types.Message, data: dict):
        await self.setup_language(data, message.from_user, message, message.chat)
