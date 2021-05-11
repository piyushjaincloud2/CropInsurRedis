"""Sample prediction script for TensorFlow 2"""
from PIL import Image, ImageDraw,ImageFont
import redisai
import re
import base64
import io
import os
import numpy as np
import cv2
from azure.storage.blob import BlobClient

MODEL_FILENAME = 'model.pb'
LABELS_FILENAME = 'labels.txt'



Labels = ["CultivatedLand","InFertileLand","Others"]
Connection_String = 'DefaultEndpointsProtocol=https;AccountName=droneredissg;AccountKey=hJx8SCf/fYN0zpOJvoAdfLv+JHwDDNO0ZScseOZI4xATYOuU4mI2I4LPbCy/qerO4jrw2zf1AgIC1diDQuayWw==;EndpointSuffix=core.windows.net'
blob = BlobClient.from_connection_string(conn_str=Connection_String, container_name="droneimages", blob_name="2.png")


class ObjectDetection:
    INPUT_TENSOR_NAME = 'image_tensor:0'
    OUTPUT_TENSOR_NAMES = ['detected_boxes:0', 'detected_scores:0', 'detected_classes:0']
    

    def predict_image(self):

        conn = redisai.Client(host='localhost', port=6379)
        # inputShape = [320,320]
        # print(image)
        # image = image.convert('RGB') if image.mode != 'RGB' else image
        # image = image.resize(inputShape)

        # img0 = cv2.imread("2.jpg")
        # _, data = cv2.imencode('.jpg', img0)
        # storedimg = data.tobytes()
                
        # image_data = io.BytesIO(storedimg)
        # image = Image.open(image_data)
        # numpy_img = np.array(image)
        # resize_img = cv2.resize(numpy_img, (320, 320), interpolation=cv2.INTER_LINEAR)

        # inputs = np.array(resize_img, dtype=np.float32)[np.newaxis, :, :, :]

        with open("2.jpg", "rb") as image_file:
            encodedimage = base64.b64encode(image_file.read()).decode('utf8')

        base64string = 'data:image/png;base64,' + encodedimage
        base64_data = re.sub('^data:image/.+;base64,', '', base64string)
        byte_data = base64.b64decode(base64_data)
        image_data = io.BytesIO(byte_data)
        img = Image.open(image_data)
        inputShape = [320,320]
        image = img.convert('RGB') if img.mode != 'RGB' else img
        image = image.resize(inputShape)
        inputs = np.array(image, dtype=np.float32)[np.newaxis, :, :, :]
        print(inputs)




        print(inputs)

        # img_ba = bytearray(inputs.tobytes())
        # v1 = redisAI.createTensorFromBlob('FLOAT', [1, 320, 320, 3], img_ba)
        # print(img_ba)
        
        # conn.tensorset("image_tensor", inputs)
        # res = conn.modelrun("customvisionmodel", ["image_tensor"], ['detected_boxes', 'detected_scores', 'detected_classes'])

        # self.detectedboxes = conn.tensorget('detected_boxes')
        # self.detectedscores = conn.tensorget('detected_scores')
        # self.detectedclasses = conn.tensorget('detected_classes')

        # graphRunner = redisai.createModelRunner('customvisionmodel')
        # redisai.modelRunnerAddInput(graphRunner, 'image_tensor', inputs)
        # redisai.modelRunnerAddOutput(graphRunner, 'detected_boxes')
        # redisai.modelRunnerAddOutput(graphRunner, 'detected_scores')
        # redisai.modelRunnerAddOutput(graphRunner, 'detected_classes')

        # run the graph and translate the result to python list
        # res = redisAI.tensorToFlatList(redisAI.modelRunnerRun(graphRunner)[0])
        # print(res)
       
        # print(self.detectedboxes)
        # print(self.detectedscores)
        # print(self.detectedclasses)

        deleteLowProbResult = []
        for idx,prediction in enumerate(self.detectedscores):
            if(prediction < 0.5):
                deleteLowProbResult.append(idx)
        
        self.detectedboxes = np.delete(self.detectedboxes, deleteLowProbResult, axis=0)
        self.detectedclasses = np.delete(self.detectedclasses, deleteLowProbResult)
                
        # print(self.detectedboxes)
        # print(self.detectedclasses)
        

def add_boxes_to_images(img, predictions,classes):
    for idx,pred in enumerate(predictions):
        width, height = img.size
        x = int(pred[0] * width)
        y = int(pred[1] * height)

        width = int(pred[2] * width)
        height = int(pred[3] * height)
        shape = [(x, y), (width, height)]
        
        font = ImageFont.truetype("ariblk.ttf", 14)
        text = Labels[classes[idx]]

        ImageDraw.Draw(img).rectangle(shape, outline ="red") 
        ImageDraw.Draw(img).text((x, y), text, fill ="red", align ="left", font=font)
        saveImageToAzure(img)

def saveImageToAzure(img):
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        blob.upload_blob(img_byte_arr)

def base64_to_image(base64_str, image_path=None):
    base64_data = re.sub('^data:image/.+;base64,', '', base64_str)
    byte_data = base64.b64decode(base64_data)
    image_data = io.BytesIO(byte_data)
    img = Image.open(image_data)
    return img

def predict():
    od_model = ObjectDetection()
    #image = base64_to_image(base64str)
    od_model.predict_image()
    #add_boxes_to_images(image, od_model.detectedboxes,od_model.detectedclasses)

def main():
    predict()

if __name__ == '__main__':
    main()
