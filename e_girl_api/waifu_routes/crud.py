from typing import Union
from ..config import *

from ..db.worker import *

from dataclasses import dataclass

@dataclass
class Waifu:
    def create_waifu(user: Union[str, int]):
        return {"user" : user}

# from ..db.mongo_collections import analytics

# def create_analytics(analytic):
    # res = createOne(dict(analytic), analytics)
    # return res