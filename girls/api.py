import requests
import json

def get_girls():
    url = "https://api.waifulabs.com/generate"
    payload=json.dumps({
        "step":0
        })
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

    response = requests.request("POST", url, headers=headers, data=payload)
    buffer = json.loads(response.text)
    return list(map(lambda x : x['image'], buffer['newGirls']))