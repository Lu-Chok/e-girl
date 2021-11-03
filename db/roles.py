import pymongo

from db.worker import createOne
from db.worker import findOne
from db.worker import update
from db.worker import deleteOne

from db.mongo_collections import user as user_collection
from bson import ObjectId


def get_role(message):
    user = findOne({'chat_id' : message.from_user.id}, user_collection)
    try:
        return user['role']
    except KeyError:
        return 'default'