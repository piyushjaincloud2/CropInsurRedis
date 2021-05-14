from PIL import Image,ImageFont,ImageDraw
import re
import base64
import io
import cv2
import numpy as np
import redisAI
import redisgears
import os
from azure.storage.blob import BlobClient
from azure.storage.blob import ContainerClient
import pandas as pd


MAX_IMAGES = 50
Labels = ["cultivatedLand","inFertileLand","other","highQualityCrop","lowQualityCrop","damageArea"]
Connection_String = 'DefaultEndpointsProtocol=https;AccountName=droneredissg;AccountKey=hJx8SCf/fYN0zpOJvoAdfLv+JHwDDNO0ZScseOZI4xATYOuU4mI2I4LPbCy/qerO4jrw2zf1AgIC1diDQuayWw==;EndpointSuffix=core.windows.net'
ContainerName = 'droneimages'


def add_boxes_to_images(img, predictions,classes,blob):
    try:
        for idx,pred in enumerate(predictions):
            x = int(pred[0] * 600)
            y = int(pred[1] * 600)

            width = int(pred[2] * 600)
            height = int(pred[3] * 600)
            shape = [(x, y), (width, height)]

            redisgears.executeCommand('xadd', 'env', '*', 'text', os.environ['FontPath'])
            font = ImageFont.truetype(r'/data/fonts/ariblk.ttf', 20)
            text = Labels[classes[idx]]
            
            ImageDraw.Draw(img).rectangle(shape, outline ="red") 
            ImageDraw.Draw(img).text((x, y), text, fill ="red", align ="left",font=font)
        saveImageToAzure(img,blob)    
    except:
        xlog('add_boxes_to_images: error:', sys.exc_info()[0])

def saveImageToAzure(img,blob):
    try:
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()
        blob.upload_blob(img_byte_arr)
    except:
        xlog('saveImageToAzure: error:', sys.exc_info()[0])

def getBlobUrl(imagename):
    try:
        container_client = ContainerClient.from_connection_string(conn_str=Connection_String, container_name="droneimages")
        blob_client = container_client.get_blob_client(imagename) 
        return blob_client.url
    except:
        xlog('getBlobUrl: error:', sys.exc_info()[0])

def getSecret(secretName):
    try:
        with open('/run/secrets/'+ secretName) as f:
            line = f.readline()
            redisgears.executeCommand('xadd', 'secret', '*', 'text', line)
    except:
        xlog('getSecret: error:', sys.exc_info()[0])

def predictImage(x):
        try:
            detectedProbability = np.array([]) 
            detectedClasses = np.array([])
            bloburl = ''
            if x['value']['image']:
                image_data = io.BytesIO(x['value']['image'])
                image = Image.open(image_data)
                numpy_img = np.array(image)
                resize_img = cv2.resize(numpy_img, (320, 320), interpolation=cv2.INTER_LINEAR)
                inputs = np.array(resize_img, dtype=np.float32)[np.newaxis, :, :, :]
                img_ba = bytearray(inputs.tobytes())
                v1 = redisAI.createTensorFromBlob('FLOAT', [1, 320, 320, 3], img_ba)

                graphRunner = redisAI.createModelRunner('customvisionmodel')
                redisAI.modelRunnerAddInput(graphRunner, 'image_tensor', v1)
                redisAI.modelRunnerAddOutput(graphRunner, 'detected_boxes')
                redisAI.modelRunnerAddOutput(graphRunner, 'detected_scores')
                redisAI.modelRunnerAddOutput(graphRunner, 'detected_classes')

                res = redisAI.modelRunnerRun(graphRunner)

                res1 = redisAI.tensorToFlatList(res[0])
                res2 = redisAI.tensorToFlatList(res[1])
                res3 = redisAI.tensorToFlatList(res[2])

                redisgears.executeCommand('xadd', 'result1', '*', 'text', res1)
                redisgears.executeCommand('xadd', 'result2', '*', 'text', res2)
                redisgears.executeCommand('xadd', 'result3', '*', 'text', res3)
            
                deleteLowProbResult = []
                for idx,prediction in enumerate(res2):
                    if(prediction < 0.5):
                        deleteLowProbResult.append(idx)

                array_2d_rowcount = int(len(res1)/4)
                arr_2d = np.reshape(res1, (array_2d_rowcount, 4))

                detectedBoxes = np.delete(arr_2d, deleteLowProbResult, axis=0)
                detectedProbability =  np.delete(res2, deleteLowProbResult)
                detectedClasses = np.delete(res3, deleteLowProbResult)
                
                imagename = x['value']['imagename']
                getSecret("azure_blob_secret")
                blob = BlobClient.from_connection_string(conn_str=Connection_String, container_name=ContainerName, blob_name=imagename)
                add_boxes_to_images(image,detectedBoxes,detectedClasses,blob)
                bloburl = getBlobUrl(imagename)
            
            weatherCondition = x['value']['weather']
            windSpeed = x['value']['windSpeed']
            isDone = x['value']['isDone']
            return detectedProbability,detectedClasses,bloburl,weatherCondition,windSpeed,isDone
        except:
            xlog('Predict_image: error:', sys.exc_info()[0])

def addToStream(x):
    try:
        redisgears.executeCommand('xadd', 'result15', '*', 'text', type(x[0]))
        redisgears.executeCommand('xadd', 'result16', '*', 'text', type(x[1]))
        detectedProbabilities =  x[0].tolist()
        detectedClasses = x[1].tolist()
        bloburl = x[2]
        weatherCondition = x[3]
        windSpeed = x[4]
        isDone = x[5]
        
        result = []
        streamResult = []

        for idx,prediction in enumerate(detectedClasses):
            result.append([Labels[prediction],detectedProbabilities[idx] * 100])

        for idx,label in enumerate(Labels):
            if not idx in detectedClasses:
                result.append([label,0])
        
        df = pd.DataFrame(result)
        result = df.groupby(0)[1].mean()

        for (columnName, columnData) in result.iteritems():
            streamResult.append([columnName,columnData])

        streamResult.append(['fileName',bloburl])
        streamResult.append(['isDone',isDone])
        streamResult.append(['weather',weatherCondition])
        streamResult.append(['windSpeed',windSpeed])
        redisgears.executeCommand('xadd', 'predictions', '*',*sum(streamResult, []))
    except:
        xlog('addToStream: error:', sys.exc_info())

def xlog(*args):
    redisgears.executeCommand('xadd', 'log', '*', 'text', ' '.join(map(str, args)))

GearsBuilder('StreamReader').\
    map(predictImage).\
    foreach(addToStream).\
    register('inspectiondata')