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
# Categories of different sections in the images
Labels = ["cultivatedLand","damageArea","highQualityCrop","inFertileLand","lowQualityCrop","other"]
# container name on the Azure blob storag
ContainerName = 'droneimages'

# add boxes to image to show box corner around the areas categorized by the AI model
def add_boxes_to_images(img, predictions,classes,blob):
    try:
        for idx,pred in enumerate(predictions):
            x = int(pred[0] * 600)
            y = int(pred[1] * 600)

            width = int(pred[2] * 600)
            height = int(pred[3] * 600)
            shape = [(x, y), (width, height)]

            font = ImageFont.truetype(r'/data/fonts/ariblk.ttf', 20)
            text = Labels[classes[idx]] + "( " + str(detectedProbability[idx]*100) + " )"
            
            ImageDraw.Draw(img).rectangle(shape, outline ="red") 
            ImageDraw.Draw(img).text((x, y), text, fill ="red", align ="left",font=font)
        saveImageToAzure(img,blob)    
    except:
        xlog('add_boxes_to_images: error:', sys.exc_info()[0])

# saving the image to Azure blob storage
def saveImageToAzure(img,blob):
    try:
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()
        blob.upload_blob(img_byte_arr)
    except:
        xlog('saveImageToAzure: error:', sys.exc_info()[0])

# get public url of the image stored at Azure
def getBlobUrl(imagename,connectionString):
    try:
        container_client = ContainerClient.from_connection_string(conn_str=connectionString, container_name="droneimages")
        blob_client = container_client.get_blob_client(imagename) 
        return blob_client.url
    except:
        xlog('getBlobUrl: error:', sys.exc_info()[0])

# get connection string of the Azure blob from the secret file on the container
def getSecret(secretName):
    try:
        with open('/run/secrets/'+ secretName) as f:
            secret = f.readline()
        return secret
    except:
        xlog('getSecret: error:', sys.exc_info())
        
# get predictions of the different categories in the images from the model trained using Custom Vision at RedisAI 
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
                connectionString = getSecret("azure_blob_secret")
                blob = BlobClient.from_connection_string(conn_str=connectionString, container_name=ContainerName, blob_name=imagename)
                add_boxes_to_images(image,detectedBoxes,detectedClasses,blob)
                bloburl = getBlobUrl(imagename,connectionString)
            
            weatherCondition = x['value']['weather']
            windSpeed = x['value']['windSpeed']
            isDone = x['value']['isDone']
            return detectedProbability,detectedClasses,bloburl,weatherCondition,windSpeed,isDone
        except:
            xlog('Predict_image: error:', sys.exc_info())

# store the modelled results returned by the Redis AI to the Redis Stream
def addToStream(x):
    try:
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

# store the exception logs in the Redis Log Stream
def xlog(*args):
    redisgears.executeCommand('xadd', 'log', '*', 'text', ' '.join(map(str, args)))

# Registeration of the stream with the Redis Gears
GearsBuilder('StreamReader').\
    map(predictImage).\
    foreach(addToStream).\
    register('inspectiondata')