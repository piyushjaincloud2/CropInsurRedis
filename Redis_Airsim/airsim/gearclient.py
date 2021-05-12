from gearsclient import GearsRemoteBuilder as GearsBuilder
from gearsclient import execute
import redis
import cv2

conn = redis.Redis(host='localhost', port=6379)

MAX_IMAGES = 50

imagename = "2.jpg"
img0 = cv2.imread("2.jpg")
_, data = cv2.imencode('.jpg', img0)
storedimg = data.tobytes()  
msg = {
    'imagename': imagename,
    'image': storedimg
}

conn.execute_command('xadd', 'airsimrunner',  'MAXLEN', '~', str(MAX_IMAGES), '*','imagename', msg['imagename'], 'image', msg['image'])