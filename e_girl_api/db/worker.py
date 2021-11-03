import pymongo
import datetime as dt
from bson import *


def createOne(data, collection):
    data['__createdAt'] = dt.datetime.now()
    collection.insert_one(data)
    return data

def find(data, collection):
    found = []
    res = collection.find(data)
    for document in res:
        found.append(document)
    return found


def findOne(data, collection):
    r = collection.find_one(data)
    return collection.find_one(data)


def update(data, update, collection):
    return collection.find_one_and_update(data, {'$set':  update}, return_document=True)


def deleteOne(data, collection):
    return collection.find_one_and_delete(data)