# Redis with Airsim :-

This project combines several modules of Redis such as RedisGears, Redis Streams and RedisAI to analyze the images of the land captured by Drone at the real time and calculate the percentage of different categories in those images using Tensorflow, Microsoft custom vision service and RedisAI.

## Features

- Uses Redis Streams to start the drone when the inspection is triggered by the user on the frontend
- Uses RedisGears to listen to the image stream 
- Processsing and analyzing images using RedisAI, Tensorflow and Custom Vision service
- Store the analyzed images to Azure Blob Storage

## Requirements

- Docker
- UnReal Engine(>= 4.24)
- Python(>=3.6)

## Set up Unreal Engine
It requires [Unreal Engine](https://www.unrealengine.com/en-US/download) to be set up on your local machine to the simulate the flying of drones on the virtual fields.

Hardware requirements to set up Unreeal Engine

- Operating System: Windows 10 64 bit
- Video Card/DirectX Version: DirectX 11 or DirectX 12 or NVIDIA compatible graphics card
- RAM: 32 GB

Once the Unreal Engine is set up on your local environment, you need to download the folder from the [Google drive](https://drive.google.com/drive/folders/1gQwwpgchWg-XJDJ987QLkaIBY7J48LoE?usp=sharing). It includes the maps of the landscapes over which the drone needs to fly. We have placed this folder inside Google Drive due to the large size of the folder.

Once the folder is downloaded, you need to double click the 'FinalProjDroneSquad' file as shown below:

![Output](/Redis_Airsim/images/unrealengine.png)

It will launch the landscape on Unreal Editor as shown below:

![Output](/Redis_Airsim/images/maps.png)

You need to click on the 'Play' button as highlighted below to start the level 1.

![Output](/Redis_Airsim/images/mapsplay.png)

In order to change the level pf the game you can navigate to Content -> Maps folder and double click on the Level 2/Level 3 files as shown below and click on the play button.

![Output](/Redis_Airsim/images/mapslevels.png)

Thereafter you can proceed to below installation section to set up other prerequisitives.

## Installation

Install the dependencies

```sh
cd airsim
pip install -r requirements.txt
```
Then from the root folder of this project run the below docker command:
```sh
docker-compose up
```
This will create two container located in this project on your machine

- First one would be the redis container on which RedisAI and RedisGears modules are hosted
- Other one is used to initialze the model on RedisAI and register the stream using RedisGears. It will be in the exit state.

Finally we need to create the blob storage account to store the anaylzed images generated using RedisAI. Create the container inside the blob storage with name 'droneimages'.
```sh

cd redisedge\secrets
Copy the connection string from the azure blob storage account and paste it on the 'azureblobsecret' file inside the folder.
```

## Running the Demo

Open your favorite Terminal and run these commands.

On the first Tab run the below command and change the level arguments as 1, 2 and 3 for starting different levels of the game.

```sh
python flyDrone.py --level=1
```
It will initialize the drone and put the drone to waiting to take-off state.
![Output](/Redis_Airsim/images/terminal1.png)


On the second tab run the below command which will continously listen from the inspection Redis Stream on which data is entered from the front end whenever the inspection is trigerred.
```sh
python captureImagesFromDrone.py --level=1
```
![Output](/Redis_Airsim/images/terminal2.png)
Once the data arrives on the stream the drone flies off and starts capturing images which is then processed and analyzed by RedisAI using Tensorflow.

`Note`: Please note after changing the level of the game on the Unreal Editor as mentioned above, please run the above two scripts on a different terminal once again and close the existing ones.
## Output

Below is the marking of the images from the output modelled using RedisAI.

Cultivated Land with Others category           |  High Quality with Low Quality category
:------------------------------------:|:-------------------------:
![Output](/Redis_Airsim/images/cultivated_others.jpg) | ![Output](/Redis_Airsim/images/highquality_lowquality.jpg)

Infertile Land category           |  Others category
:------------------------------------:|:-------------------------:
![Output](/Redis_Airsim/images/infertile_land.jpg) | ![Output](/Redis_Airsim/images/other.jpg)
