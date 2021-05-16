import airsim
import time
import os
import numpy as np
import cv2
import redis
import argparse
from captureImageService import CaptureImageService

conn = redis.Redis(host='localhost', port=6379)
MAX_IMAGES = 50

def convertToMap(data):
    if isinstance(data, bytes):  return data.decode('ascii')
    if isinstance(data, dict):   return dict(map(convertToMap, data.items()))
    if isinstance(data, tuple):  return map(convertToMap, data)
    return data

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--level', help='Game Level', type=int, default=1)
    args = parser.parse_args()

    # set the weather conditions for different game levels
    gameLevel = args.level
    print(gameLevel)
    input = []
    if gameLevel == 3:    
        print('Level 3')
        input.append(['weather','Sunny'])
        input.append(['windSpeed',25])
    elif gameLevel == 2:
        print('Level 2')
        input.append(['weather','Sunny'])
        input.append(['windSpeed',5])
    else:
       print('Level 1')
       input.append(['weather','Rain'])
       input.append(['windSpeed',5])

    # creating the consumer group if it does not exist to read the data from the stream
    try:
        conn.execute_command('xgroup','CREATE','inspection','InspectionGroup','$','MKSTREAM')
    except:
        print("Consumer Group already  exist")
   
    # waiting to receive input the redis stream and once the signal is received drone starts flying and stores real time images to Redis Stream in form of bytes.  
    try:
        client = airsim.VehicleClient()
        client.confirmConnection()
        while True:
            res = conn.execute_command('xreadgroup','GROUP', 'InspectionGroup','InspectionConsumer','Block', 10000,'STREAMS', 'inspection','>')
            if res:
                print("Signal received from stream")
                    
                count=1
                currentStream = res[0][1][0]
                currentStreamMap = convertToMap(currentStream)
                currentStreamMapList = list(currentStreamMap)
                streamID = currentStreamMapList[0]
                inspectionId = currentStreamMapList[1]['inspectionId']
                print("Inspection ID is " + inspectionId )
                print("Stream ID is " + streamID )

                CaptureImageService.setCameraPose(client)

                client.confirmConnection()
                client.enableApiControl(True)
                client.armDisarm(True)

                print("Drone is ready to fly now")

                if client.isApiControlEnabled():
                    res = conn.execute_command('xack','inspection','InspectionGroup',streamID)
                    print("Stream Acknowledged " + str(res))

                while(client.isApiControlEnabled()):
                    iteration = input[:]
                    imagename = inspectionId + "_" + str(count) + '.jpg'
                    img_rgb = CaptureImageService.getRealTimeImage(client,count)
                    CaptureImageService.addToStream(conn,img_rgb,iteration,imagename,MAX_IMAGES)
                    time.sleep(2)
                    print(count)
                    count += 1

                lastRow = input[:]
                lastRow.append(['isDone','1'])
                lastRow.append(['imagename',''])
                lastRow.append(['image',''])
                print("Saving Final Row")
                conn.execute_command('xadd', 'inspectiondata',  'MAXLEN', '~', str(MAX_IMAGES), '*', *sum(lastRow,[]))
            else:
                print("Yet no input from stream")
    except:
        print("Airsim is not yet ready")
    