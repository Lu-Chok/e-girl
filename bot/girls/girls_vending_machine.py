import os, random

# def get_own_waifu(user):

import requests
import json
from io import StringIO
import base64
from PIL import Image
from io import BytesIO

def get_girls():
    url = "https://api.waifulabs.com/generate"
    payload="{\"step\":0}"
    headers = {
    'sec-ch-ua': '"Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87"',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,uk;q=0.6',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    'sec-fetch-site': 'same-site',
    'sec-fetch-dest': 'empty',
    'sec-ch-ua-mobile': '?0',
    'referer': 'https://waifulabs.com/',
    'origin': 'https://waifulabs.com',
    'content-type': 'application/json'
    }

    girlcounter = 0
    buffer = json.loads(open('temp/1.json').read())
    for girl in buffer['newGirls']:
        im = Image.open(BytesIO(base64.b64decode(girl['image'])))
        girlcounter += 1
        im.save(f"./images/{girlcounter}.png", 'PNG')
    return 'success'

def get_random_girl(user):
    rfile = ''
    for root, dirs, files in os.walk('./used'):
        if f"{user}_1.png" in files:
            return {"status" : 200, "text" : "девка найдена", "file" : f"./used/{user}_1.png", "path" : os.path.abspath(f"./used/{user}_1.png")}

    n=0
    random.seed();
    for root, dirs, files in os.walk('./images'):
        files.remove('.DS_Store')
        if len(files) == 0:
            get_girls()
            print("девки кончились")
            return get_random_girl(user)
            # return {"status" : 400, "error" : "девки кончились"}
        for name in files:
            n=n+1
            # print(files)
            if random.uniform(0, n) < 1: rfile=os.path.join(root, name)
            
    print(rfile)
    os.rename(rfile, f"./used/{user}_1.png")
    return {"status" : 200, "text" : "создана новая девка", "file" : f"./used/{user}_1.png", "path" : os.path.abspath(f"./used/{user}_1.png")}

print(get_random_girl(random.randint(0,160)))