import pymongo
from ..config import DB_STRING

cursor = pymongo.MongoClient(DB_STRING)
db = cursor.waifus

user = db['users']
starts = db['starts']
waifus = db['waifus']
waifu_images = db['waifu_images']