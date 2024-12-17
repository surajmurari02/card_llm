import json
import requests
import cv2
import time
from ast import literal_eval

img = cv2.imread("img/3.jpg")
server_url = "http://4.240.46.255:11434"
_, encoded_image = cv2.imencode('.jpg', img)
image_bytes = encoded_image.tobytes()
files = {'image': ('image.jpg', image_bytes, 'image/jpeg')}
text = {"query": "I am providing business cards, What I want is to get json output of some keys like name, Company name, Mob. Number, e-mail id, address,. I want it all to be in a json output in a structured manner"}
response = requests.post(server_url, files=files, data=text, timeout=30).json()
st = time.perf_counter()
print("RES", response)
op = time.perf_counter() - st
print(op)
# val = literal_eval(response.strip())
print(response.strip())










# curl http://localhost:11434/api/chat -d '{
#   "model": "llama3.2-vision",
#   "messages": [
#     {
#       "role": "user",
#       "content": "what is in this image?",
#       "images": ["<base64-encoded image data>"]
#     }
#   ]
# }'
