from loader import bot, storage
from start import dir_check_make

from db.worker import *
from db.mongo_collections import starts

import time

async def on_shutdown(dp):
    await bot.close()
    await storage.close()

# dir_check_make('used')

print(createOne({'start' : int(time.time())}, starts))

if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp
    
    executor.start_polling(dp, on_shutdown=on_shutdown)
