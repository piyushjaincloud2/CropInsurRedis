import airsim
import time
import os
import numpy as np
import cv2
import redis
from flyService import FlyService

conn = redis.Redis(host='localhost', port=6379)
MAX_IMAGES = 50

def main():

    client = airsim.VehicleClient()
    client.confirmConnection()
    count=1

    FlyService.setCameraPose(client)

    input = []
    input.append(['weather','Sunny'])
    input.append(['windSpeed',5])

    while(client.isApiControlEnabled()):
        iteration = input[:]
        imagename = str(count) + '.jpg'
        img_rgb = FlyService.getRealTimeImage(client,count)
        FlyService.addToStream(conn,img_rgb,iteration,imagename,MAX_IMAGES)
        time.sleep(2)
        print(count)
        count += 1

if __name__ == '__main__':
    main()