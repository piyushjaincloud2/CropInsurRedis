import airsim
from datetime import datetime
import time
import os
import numpy as np
import cv2
from azure.storage.blob.aio import BlobClient
import shutil
import asyncio
from azure.cosmosdb.table.tableservice import TableService
from azure.cosmosdb.table.models import Entity
from operator import itemgetter
import errno, stat
from customvisionservice import CustomVisionService
from azure.cosmosdb.table.tablebatch import TableBatch
import uuid

# Get the latest inspectionID
def GetLatestInspectionData(table_service):
    results = table_service.query_entities('Inspections',filter=None, select='RowKey,Timestamp,PartitionKey,inspectionId')
    lastestInspection = sorted(results, key=itemgetter('Timestamp'),reverse=True)
    return lastestInspection

# Set camera position to take ground pictures
def SetCameraPose(client):
    camera_pose = airsim.Pose(airsim.Vector3r(0, 0, 0), airsim.to_quaternion(-1.5708, 0, 0))
    client.simSetCameraPose(1, camera_pose);

# Set root level permission to store media items
def handleRemoveReadonly(func, path, exc):
  excvalue = exc[1]
  if func in (os.rmdir, os.remove) and excvalue.errno == errno.EACCES:
      os.chmod(path, stat.S_IRWXU| stat.S_IRWXG| stat.S_IRWXO)
      func(path)
  else:
      raise

def main():
    account_name = "hawathon";
    account_key = "T4q6iO9UkmR/3gjNOLbDZEQsZZvglTMbKpaC5yp+ERp+eV79Fg4xoHajrT8i11MTIlijweaFmk93c/s3RsnnIA=="
    table_service = TableService(account_name=account_name, account_key=account_key)
    connection_string = "DefaultEndpointsProtocol=https;AccountName={};AccountKey={};EndpointSuffix=core.windows.net".format(account_name,account_key)
    client = airsim.VehicleClient()
    client.confirmConnection()
    temp_dir = os.path.join(os.getcwd(), "airsim_drone")
    boximages_temp_dir = os.path.join(os.getcwd(), "airsim_drone_boxedimages")
    isdir = os.path.isdir(temp_dir)
    isboximagedir = os.path.isdir(boximages_temp_dir)

    # clear previous run folders
    if isdir:
        shutil.rmtree(temp_dir,ignore_errors=False, onerror=handleRemoveReadonly)
        shutil.rmtree(boximages_temp_dir,ignore_errors=False, onerror=handleRemoveReadonly)

    # create folders to store media and boxed images
    try:
        os.chmod(os.getcwd(), stat.S_IRWXU| stat.S_IRWXG| stat.S_IRWXO)
        os.makedirs(temp_dir)
        os.makedirs(boximages_temp_dir)
    except OSError:
        if not os.path.isdir(temp_dir):
            raise

    count=1
    lastestInspection  = GetLatestInspectionData(table_service)
    inspectionID = lastestInspection[0].inspectionId

    loop = asyncio.get_event_loop()
    tasks = []

    SetCameraPose(client)

    # loop until drone simulator is running
    while(client.isApiControlEnabled()):
        filepath = os.path.join(temp_dir, str(count))
        filename = inspectionID + '_' + str(count) + '.png'
        simImages = client.simGetImages([airsim.ImageRequest("1", airsim.ImageType.Scene, False, False)])
        simImage = simImages[0]
        img1d = np.fromstring(simImage.image_data_uint8, dtype=np.uint8) 
        img_rgb = img1d.reshape(simImage.height, simImage.width, 3)
        cv2.imwrite(os.path.normpath(filepath + '.png'), img_rgb)
        task = asyncio.gather(CustomVisionService.ClassifyImage(account_name,account_key,os.path.normpath(filepath + '.png'),inspectionID,connection_string,filepath,filename,"Sunny", 5)) #send image to custom vision for object detection
        tasks.append(task)
        time.sleep(2)
        count += 1

    loop.run_until_complete(asyncio.wait(tasks))
    predictionObject = {}
    predictionObject['inspectionId'] = inspectionID
    predictionObject['RowKey'] = str(uuid.uuid4())
    predictionObject['PartitionKey'] = str(uuid.uuid4())
    predictionObject['isDone'] = True
    predictionObject['Weather'] = 'Rain'
    predictionObject['WindSpeed'] = 5

    table_service.insert_entity('Field', predictionObject)

if __name__ == '__main__':
    main()


