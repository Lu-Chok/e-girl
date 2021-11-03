from fastapi import Depends, APIRouter, HTTPException, Request

from ..config import VERSION

from . import schemas

from .crud import Waifu

import json
import datetime

from .waifu import WaifuTemplate, UserSync

router = APIRouter(prefix="/v1")


@router.post("/user")
def save_user(user: schemas.webhookSchema, request: Request):
    data = request._json
    data['id'] = str(data['id'])
    return UserSync.sync(data)


@router.get("/waifu")
def get_waifu(user: str):
    """
    Health Check
    """
    w = WaifuTemplate(user)
    w.load_waifu()
    return w.get_waifu()

@router.get("/waifu/name")
def name_waifu(user: str, name: str, request: Request):
    w = WaifuTemplate(user)
    return {"status" : "ok"} if w.name_waifu(name) else {"status" : "error"}


@router.get("/waifu/feed")
def feed_waifu(user: str):
    """
    Feed Waifu
    """
    w = WaifuTemplate(user)
    res = {"status" : "ok"} if w.feed_waifu() else {"status" : "error"}
    return res

@router.get("/waifu/pet")
def pet_waifu(user: str):
    """
    Pet Waifu
    """
    w = WaifuTemplate(user)
    res = {"status" : "ok"} if w.pet_waifu() else {"status" : "error"}
    return res


@router.get("/waifu/satisfy")
def satisfy_waifu(user: str):
    """
    Satisfy Waifu
    """
    w = WaifuTemplate(user)
    res = {"status" : "ok"} if w.sex_waifu() else {"status" : "error"}

@router.get("/waifu/drop")
def feed_waifu(user: str):
    """
    Drop Waifu
    """
    w = WaifuTemplate(user)
    res = {"status" : "ok"} if w.drop() else {"status" : "error"}
    return res


@router.get("/")
def alive():
    """
    Health Check
    """
    return {"alive":"I'm alive!"}


@router.get("/version")
def version():
    return {"version": VERSION}

