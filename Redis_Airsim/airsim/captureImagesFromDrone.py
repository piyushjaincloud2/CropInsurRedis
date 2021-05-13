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

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--level', help='Game Level', type=int, default=1)
    args = parser.parse_args()

    client = airsim.VehicleClient()
    client.confirmConnection()

    CaptureImageService.setCameraPose(client)
    
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
    
    count=1

    while(client.isApiControlEnabled()):
        iteration = input[:]
        imagename = str(count) + '.jpg'
        img_rgb = CaptureImageService.getRealTimeImage(client,count)
        CaptureImageService.addToStream(conn,img_rgb,iteration,imagename,MAX_IMAGES)
        time.sleep(2)
        print(count)
        count += 1