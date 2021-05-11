from PIL import Image,ImageFont,ImageDraw
import re
import base64
import io
import cv2
import numpy as np
import redisAI
import redisgears
from azure.storage.blob import BlobClient


MAX_IMAGES = 50
Labels = ["CultivatedLand","InFertileLand","Others"]
Connection_String = 'DefaultEndpointsProtocol=https;AccountName=droneredissg;AccountKey=hJx8SCf/fYN0zpOJvoAdfLv+JHwDDNO0ZScseOZI4xATYOuU4mI2I4LPbCy/qerO4jrw2zf1AgIC1diDQuayWw==;EndpointSuffix=core.windows.net'
blob = BlobClient.from_connection_string(conn_str=Connection_String, container_name="droneimages", blob_name="7.jpg")
blob1 = BlobClient.from_connection_string(conn_str=Connection_String, container_name="droneimages", blob_name="8.jpg")

def add_boxes_to_images(img, predictions,classes):
    try:
        for idx,pred in enumerate(predictions):
            x = int(pred[0] * 600)
            y = int(pred[1] * 600)

            width = int(pred[2] * 600)
            height = int(pred[3] * 600)
            shape = [(x, y), (width, height)]
            
            font = ImageFont.truetype(r'/var/opt/redislabs/modules/rg/python3_1.0.6/ariblk.ttf', 20)
            text = Labels[classes[idx]]

            ImageDraw.Draw(img).rectangle(shape, outline ="red") 
            ImageDraw.Draw(img).text((x, y), text, fill ="red", align ="left",font=font)
        saveResizeImageToAzure(img)    
    except:
        xlog('add_boxes_to_images: error:', sys.exc_info()[0])

def saveImageToAzure(img):
    try:
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()
        blob.upload_blob(img_byte_arr)
    except:
        xlog('saveImageToAzure: error:', sys.exc_info()[0])

def saveResizeImageToAzure(img):
    try:
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()
        blob1.upload_blob(img_byte_arr)
    except:
        xlog('saveResizeImageToAzure: error:', sys.exc_info()[0])

def predictImage(x):
        try:
            image_data = io.BytesIO(x['value']['image'])
            image = Image.open(image_data)
            saveImageToAzure(image)
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

            detectedboxes = np.delete(arr_2d, deleteLowProbResult, axis=0)
            detectedclasses = np.delete(res3, deleteLowProbResult)

            add_boxes_to_images(image,detectedboxes,detectedclasses)
            return res1,res2,res3
        except:
            xlog('Predict_image: error:', sys.exc_info()[0])

def addToStream(x):
    # save animal name into a new stream
    try:
        redisgears.executeCommand('xadd', 'result1', '*', 'text', x[0])
        redisgears.executeCommand('xadd', 'result2', '*', 'text', x[1])
        redisgears.executeCommand('xadd', 'result3', '*', 'text', x[2])
    except:
        xlog('addToStream: error:', sys.exc_info()[0])

def xlog(*args):
    redisgears.executeCommand('xadd', 'log', '*', 'text', ' '.join(map(str, args)))


GearsBuilder('StreamReader').\
    map(predictImage).\
    foreach(addToStream).\
    register('airsimrunner')