from io import StringIO
import json
import base64
from PIL import Image
from io import BytesIO

girls = json.loads(open('out.json').read())
girl = girls['newGirls'][5]['image']

im = Image.open(BytesIO(base64.b64decode(girl)))
im.save('image.png', 'PNG')