from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
import matplotlib.pyplot as plt
import json
import cv2
from msrest.authentication import ApiKeyCredentials
from azure.cosmosdb.table.tableservice import TableService
from azure.storage.blob import BlobClient
import asyncio
import os
import uuid

class CustomVisionService: 

    # Ignore prediction less than probability of confidence level
    @staticmethod
    def append_predictions(result, confidence_level = 0.2):
        predictions = []
        for prediction in result.predictions:
            if prediction.probability > confidence_level:
                predictions.append(prediction)
                print(prediction.probability, prediction.tag_name)
        return predictions

    # Add box marking on image
    @staticmethod
    def add_boxes_to_images(img, predictions,temp_dir,fileName,customVisionTraininglabels):
        predictionObject = {}
        foundPredictions = []
        for pred in predictions:
            x = int(pred.bounding_box.left * img.shape[0])
            y = int(pred.bounding_box.top * img.shape[1])
            probability_normalized = pred.probability*100
            foundPredictions.append(pred.tag_name)
            width = x + int(pred.bounding_box.width * img.shape[0])
            height = y + int(pred.bounding_box.height * img.shape[1])
            predictionObject[pred.tag_name] = probability_normalized
            img = cv2.rectangle(img, (x, y), (width, height), (0,0,255), 2)
            img = cv2.putText(img, pred.tag_name + "( " + str(probability_normalized) +  " )", (x + 5, y + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,255), 2, cv2.LINE_AA, False)
         
        for label in customVisionTraininglabels:
            if not label in foundPredictions:
                predictionObject[label] = 0

        cv2.imwrite(os.path.join(temp_dir , fileName), img)
        return predictionObject

    @staticmethod
    async def ClassifyImage(account_name,account_key,imageFile, rowKey,connection_string,filePath, fileName,weather, windspeed):

        endpoint1 = "https://southcentralus.api.cognitive.microsoft.com/"
        training_key = "595cfc30a70c4043a3509aa847a85707"
        table_service = TableService(account_name=account_name, account_key=account_key)
        credentials = ApiKeyCredentials(in_headers={"Training-key": training_key})
        train = CustomVisionTrainingClient(endpoint=endpoint1, credentials = credentials)
        predict = CustomVisionPredictionClient(endpoint=endpoint1,credentials = credentials)
        projects = train.get_projects()
        customVisionTraininglabels = ['CultivatedLand','DamageArea','HighQualityCrop','LowQualityCrop','OtherAreas','UnFertileLand']
        project = None

        # get the object detection project
        for p in projects:
            if p.name == "DroneSquad":
                project = p

        print(project.id)
        
        # get predictions from custom vision service
        with open(imageFile, mode="rb") as image_data:
            await asyncio.sleep(0.1)
            customvisionprediction = predict.detect_image(project.id, "Iteration13", image_data)

        predictions = CustomVisionService.append_predictions(customvisionprediction)

        img = cv2.imread(imageFile)
        temp_dir = os.path.join(os.getcwd(), "airsim_drone_boxedimages")
        # generate prediction object
        predictionObject = CustomVisionService.add_boxes_to_images(img, predictions,temp_dir,fileName,customVisionTraininglabels)
        predictionObject['fileName'] = 'https://hawathon.blob.core.windows.net/drone/'+ fileName
        predictionObject['inspectionId'] = rowKey
        predictionObject['RowKey'] = str(uuid.uuid4())
        predictionObject['PartitionKey'] = str(uuid.uuid4())
        predictionObject['Weather'] = weather
        predictionObject['WindSpeed'] = windspeed
        predictionObject['isDone'] = False
        print(predictionObject)
        table_service.insert_entity('Field', predictionObject) # store prediction objectto table stoarge
        blob = BlobClient.from_connection_string(conn_str=connection_string, container_name="drone", blob_name= fileName) # store boxed images to blob storage
        with open(os.path.join(temp_dir , fileName), "rb") as data:
            blob.upload_blob(data)