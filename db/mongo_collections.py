import pymongo
from .auth import mainToken

cursor = pymongo.MongoClient(mainToken)
db = cursor.users

user = db['users']
starts = db['starts']
waifus = db['waifus']