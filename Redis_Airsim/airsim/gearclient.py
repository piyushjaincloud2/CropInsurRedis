from gearsclient import GearsRemoteBuilder as GearsBuilder
from gearsclient import execute
import redis
import cv2
import pandas as pd

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




input = []


input.append(['CultivaltedLand',5])
input.append(['Infertiland',5])
input.append(['CultivaltedLand',8])
print(input)

df = pd.DataFrame(input)
result = df.groupby(0)[1].mean()
print(type(result))
print(result)

for (columnName, columnData) in result.iteritems():
   input.append([columnName,columnData])


print(input)
# for name,group in result:
#    print(name)
#    for subgroup in group:
#        print(subgroup)

#conn.execute_command('xadd', 'airsimrunner',  'MAXLEN', '~', str(MAX_IMAGES), '*','imagename', msg['imagename'], 'image', msg['image'])