import pymongo

def createOne(data, collection):
    collection.insert_one(data)
    return data

def find(data, collection):
    found = []
    res = collection.find(data)
    for document in res:
        found.append(document)
    return found


def findOne(data, collection):
    return collection.find_one(data)


def update(data, update, collection):
    return collection.find_one_and_update(data, {'$set':  update}, return_document=True)


def deleteOne(data, collection):
    return collection.find_one_and_delete(data)