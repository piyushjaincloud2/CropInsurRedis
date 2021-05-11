from gearsclient import GearsRemoteBuilder as GearsBuilder
from gearsclient import execute
import redis
import cv2
import base64

conn = redis.Redis(host='localhost', port=6379)

with open("1.png", "rb") as image_file:
    encodedimage = base64.b64encode(image_file.read()).decode('utf8')

img0 = cv2.imread("2.jpg")
_, data = cv2.imencode('.jpg', img0)
storedimg = data.tobytes()

print(storedimg)

MAX_IMAGES = 50
conn.execute_command('xadd', 'airsimrunner',  'MAXLEN', '~', str(MAX_IMAGES), '*', 'image', storedimg)