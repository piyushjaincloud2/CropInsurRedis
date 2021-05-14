import redis
import numpy as np
conn = redis.Redis(host='localhost', port=6379)

# try:
#     res1 = conn.execute_command('xinfo','GROUPS','inspection')
# except:


try:
    res1 = conn.execute_command('xgroup','CREATE','inspection','InspectionGroup','$','MKSTREAM')
    print(res1)
except:
    print("Consumer Group already  exist")


res = conn.execute_command('xreadgroup','GROUP', 'InspectionGroup','InspectionConsumer','Block', 30000,'STREAMS', 'inspection','>')

currentStream = res[0][1][0]
print(currentStream)

# def convert(data):
#     if isinstance(data, bytes):  return data.decode('ascii')
#     if isinstance(data, dict):   return dict(map(convert, data.items()))
#     if isinstance(data, tuple):  return map(convert, data)
#     return data

# tuple1 = res[0][1][0]
# map1 = convert(tuple1)
# list1 = list(map1)

# print(list1[0])
# res = conn.execute_command('xack','inspection','test',list1[0])
# print(res)
# detectedProbability = np.array([]) 
# print(type(detectedProbability))