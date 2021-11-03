from datetime import datetime, timedelta

from ..db.worker import findOne, createOne, update

from ..db.mongo_collections import user as user_collection

from ..config import DEFAULT_NAME, DEFAULT_HEALTH, DEFAULT_SYMPATHY, DEFAULT_MOOD

from ..image_provider.girls_vending_machine import WaifuVending


class UserSync:
    def sync(user) -> dict:
        found = findOne({'id' : user['id']}, user_collection)
        
        if found == None:
            found = createOne(user, user_collection)
            print('created new user')
        else:
            found = update({'id' : user['id']}, user, user_collection)
        return {
            "first_name" : found['first_name'],
            "username" : found['username'],
            "id" : found['id']
        }
        # findOne({"chat"},user_collection)
        


class WaifuTemplate:
    def __init__(self, owner, name=DEFAULT_NAME, health=DEFAULT_HEALTH, sympathy=DEFAULT_SYMPATHY, mood=DEFAULT_MOOD) -> None:
        self.owner = owner

    def drop(self):
        WaifuVending.refresh_waifu(self.owner)
        return True

    def __update(self, patch):
        return WaifuVending.update_waifu_fields(self.owner, patch)

        
    def __recount_stats(self):
        HEALTH_UPDATE_RATE = 1200
        SYMPATHY_UPDATE_RATE = 600
        MOOD_UPDATE_RATE = 600

        now = datetime.now()
        patch = {}

        health_update = (now - self._health_last_update).total_seconds() > HEALTH_UPDATE_RATE
        sympathy_update = (now - self._health_last_update).total_seconds() > SYMPATHY_UPDATE_RATE
        mood_update = (now - self._mood_last_update).total_seconds() > MOOD_UPDATE_RATE

        if health_update == True:
            diff = int((now - self._health_last_update).total_seconds() // HEALTH_UPDATE_RATE)
            self.health = self.health - diff if self.health - diff > 0 else 0
            self._health_last_update = datetime.now()
            patch['health'] = self.health
            patch['_health_last_update'] = self._health_last_update

        if sympathy_update == True:
            diff = int((now - self._sympathy_last_update).total_seconds() // SYMPATHY_UPDATE_RATE)
            self.sympathy = self.sympathy - diff if self.sympathy - diff > 0 else 0
            self._sympathy_last_update = datetime.now()
            patch['sympathy'] = self.sympathy
            patch['_sympathy_last_update'] = self._sympathy_last_update
        
        if mood_update == True:
            diff = int((now - self._mood_last_update).total_seconds() // MOOD_UPDATE_RATE)
            self.mood = self.mood - diff if self.mood - diff > 0 else 0
            self._mood_last_update = datetime.now()
            patch['mood'] = self.mood
            patch['_mood_last_update'] = self._mood_last_update

        self.__update(patch)

    def load_waifu(self):
        loaded_waifu = WaifuVending.get_waifu(self.owner)
        self.name = loaded_waifu.get("name")
        self.health = loaded_waifu.get("health")
        self.sympathy = loaded_waifu.get("sympathy")
        self.mood = loaded_waifu.get("mood")
        self.image = loaded_waifu.get("image", None)
        
        self._health_last_update = loaded_waifu.get("_health_last_update", None)
        self._mood_last_update = loaded_waifu.get("_mood_last_update", None)
        self._sympathy_last_update = loaded_waifu.get("_sympathy_last_update", None)

        self.__recount_stats()


    def feed_waifu(self, mod=1):
        self.load_waifu()

        self.health = self.health + mod if self.health + mod <= DEFAULT_HEALTH else DEFAULT_HEALTH
        self._health_last_update = datetime.now()

        self.__update({"health" : self.health, "_health_last_update" : self._health_last_update})
        return True
    
    
    def pet_waifu(self, mod=1):
        self.load_waifu()

        self.sympathy = self.sympathy + mod if self.sympathy + mod <= DEFAULT_SYMPATHY else DEFAULT_SYMPATHY
        self._sympathy_last_update = datetime.now()

        self.__update({"sympathy" : self.sympathy, "_sympathy_last_update" : self._sympathy_last_update})
        return True


    def sex_waifu(self, mod=1):
        self.load_waifu()

        self.mood = self.mood + mod if self.mood + mod <= DEFAULT_MOOD else DEFAULT_MOOD
        self._mood_last_update = datetime.now()

        self.__update({"mood" : self.mood, "_mood_last_update" : self._mood_last_update})
        return True
    
    def name_waifu(self, name):
        self.load_waifu()
        
        self.name = name

        self.__update({"name" : self.name})
        return True


    def get_waifu(self) -> dict:
        return {p:v for p, v in self.__dict__.items() if p[:1] != '_'}
