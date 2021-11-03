import logging
import os

from aiogram import Bot, Dispatcher, types

from middlewares.user_middleware import UserMiddleware

# from aiogram.contrib.fsm_storage.mongo import MongoStorage

bot = Bot(token=os.environ['BOT_TOKEN'], parse_mode=types.ParseMode.MARKDOWN_V2)

from aiogram.contrib.fsm_storage.memory import MemoryStorage
storage = MemoryStorage()
# from aiogram.contrib.fsm_storage.mongo import MongoStorage
# storage = MongoStorage(host='localhost', port=27017, username=os.environ['DB_USERNAME'], password=os.environ['DB_PASSWORD'] db_name='userstates')

dp = Dispatcher(bot, storage=storage)

dp.middleware.setup(UserMiddleware())

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO,
                    )
