from io import StringIO
import json
import base64
from PIL import Image
from io import BytesIO

girls = []
girlcounter = 0

for i in range(0,10):
    buffer = json.loads(open(f"{i+1}.json").read())
    for girl in buffer['newGirls']:
        # print(girl['image'])
        # girls.append(girl['image'])
        im = Image.open(BytesIO(base64.b64decode(girl['image'])))
        girlcounter += 1
        im.save(f"./images/{girlcounter}.png", 'PNG')

# print(girls)
    # girls = json.loads(open('out.json').read())
    # girl = girls['newGirls'][5]['image']