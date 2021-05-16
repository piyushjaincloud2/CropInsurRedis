# Redis with Airsim :-

This project combines several modules of Redis such as RedisGears, Redis Streams and RedisAI to analyze the images of the land captured by Drone at the real time and calculate the percentage of different categories in those images using Tensorflow, Microsoft custom vision service and RedisAI.

## Features

- Uses Redis Streams to start the drone when the inspection is triggered by the user on the frontend
- Uses RedisGears to listen to the image stream 
- Processsing and analyzing images using RedisAI, Tensorflow and Custom Vision service
- Store the analyzed images to Azure Blob Storage

## Requirements

- Docker
- UnReal Engine
- Python(>=3.6)

## Installation

It requires [Unreal Engine](https://www.unrealengine.com/en-US/download) to be set up on your local machine to the simulate the flying of drones on the virtual fields.

Install the dependencies

```sh
cd airsim
pip install -r requirements.txt
```
Then from the root folder of this project run the below docker command to start up the redis and initialize the redis with 'customvision' ai model and register the 'inspectiondata' stream using RedisGears.
```sh
docker-compose up
```
This will create two container on your machine

- First one would be the redis container on which RedisAI and RedisGears modules are hosted
- Other one is used to initialze the model on RedisAI and register the stream using RedisGears. It will be in the exit state.

Finally we need to create the blob storage account to store the anaylzed images generated using RedisAI. Create the container inside the blob storage with name 'droneimages'.
```sh

cd redisedge\secrets
Copy the connection string from the azure blob storage account and paste it on the 'azureblobsecret' file inside the folder.
```

## Running the Demo

Open your favorite Terminal and run these commands.

On the first Tab run the below command and change the level arguments as 1, 2 and 3 for different levels

```sh
python flyDrone.py --level=1
```
It will initialize the drone and put the drone to waiting to take-off state.

On the second tab run the below command which will continously listen from the inspection Redis Stream on which data is entered from the front end whenever the inspection is trigerred.
```sh
python captureImagesFromDrone.py --level=1
```
When the input arrives on the stream the drone flies off and starts capturing images which is then processed and analyzed by RedisAI using Tensorflow.

## Output

Below is the marking of the images from the output modelled using RedisAI.

Cultivated Land with Others category           |  High Quality with Low Quality category
:------------------------------------:|:-------------------------:
![Output](/Redis_Airsim/images/cultivated_others.jpg) | ![Output](/Redis_Airsim/images/highquality_lowquality.jpg)

Infertile Land category           |  Others category
:------------------------------------:|:-------------------------:
![Output](/Redis_Airsim/images/infertile_land.jpg) | ![Output](/Redis_Airsim/images/other.jpg)
