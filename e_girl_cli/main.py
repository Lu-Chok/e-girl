import requests
import base64
import io

import climage

import numpy as np

from PIL import Image
from colorthief import ColorThief

SEPARATOR = "=" * 40

def decode_img(image):
    return io.BytesIO(base64.b64decode(image))

def pretty(s, l=10):
    l += 2
    s = str(s)
    d = ' '
    diff = l - len(s)
    s += d * diff
    return s

def bar(num, l=10):
    d = '-'
    e = '▄'
    bar = f"[{e * num}{d * (l - num)}]"
    return bar

def feed(owner):
    waifu = requests.get(f"http://127.0.0.1/v1/waifu/feed?user={owner}").json()
    return waifu

def pet(owner):
    waifu = requests.get(f"http://127.0.0.1/v1/waifu/pet?user={owner}").json()
    return waifu

def satisfy(owner):
    waifu = requests.get(f"http://127.0.0.1/v1/waifu/satisfy?user={owner}").json()
    return waifu

def drop(owner):
    waifu = requests.get(f"http://127.0.0.1/v1/waifu/drop?user={owner}").json()
    return waifu

def _get_screen(owner):
    waifu = requests.get(f"http://127.0.0.1/v1/waifu?user={owner}").json()
    image =decode_img( waifu.get("image", None))

    preview = climage.convert(image, is_unicode=True, is_256color=True, width=40)
    
    climage.to_file(image, 'test.png', is_unicode=True, is_256color=True, width=40)

            
    l_name = pretty(waifu.get("name", "?"), 23)

    l_health = bar(waifu.get("health", 0), 10)
    l_sympathy = bar(waifu.get("sympathy", 0), 10)
    l_mood = bar(waifu.get("mood", 0), 10)

    l_owner = pretty(waifu.get("owner", "?"), 23)

    name_tag = f"""
.-=-._.-=(+)=-._.-(=*=)-._.-=(+)=-._.-=-.
|                                       |
|   Name:      { l_name                }|
|                                       |
|   Health:    { l_health }             |
|   Sympathy:  {l_sympathy}             |
|   Mood:      {  l_mood  }             |
|                                       |
|   Owner:     { l_owner               }|
|_______________________________________|
|  Feed  | |  Pet  |  |  18+  | |  Drop |
|    F   | |   P   |  |   S   | |   D   |
|‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾|
'-=-'‾'-=(+)=-'‾'-(=*=)-'‾'-=(+)=-'‾'-=-'
"""
    checksum = ''.join((l_name,l_health,l_sympathy,l_mood,l_owner))
    # preview = SEPARATOR + '\n' + preview + name_tag + SEPARATOR
    preview = preview + name_tag
    return preview, checksum