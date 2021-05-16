## Dronification of Crop Insurer using Drone, Redis and cloud technologies

Enable Crop Insurance company to generate insurance policy and claim settlement using Drone, Redis and Cloud Technologies to ensure transparency, Quick turn around time with 100% accuracy and client satisfaction.  

## Projects:
- Redis_Airsim:
  -  RedisMod for loading Redis modules
  -  Image modelling using RedisAI
  -  Stream Registration using RedisGears
  -  Modules to create virtual farm using Unreal Engine objects
  -  Azure blob storage integration
- Frontend:
  -  Front end app code
  -  Integration with Redis stream
  -  Integration with microservice
- Microservices:
  -  Microservice code- Java springboot framework
  
## Demo Flow:  

![image](https://user-images.githubusercontent.com/83917397/118404229-9f0dea80-b68f-11eb-96c4-06012e286cc2.png)


```sh
- Insurer logins to the portal using his credentials.  
- Registers for the new customer with property information.  
- Do the First inspection of the Property using drone to check how much land is cultivated and based on this information generate sum assured and premium.  
- If Customer is fine with this information create a policy for the customer.  
- As per policy terms and conditions insurer is free to do another inspection of the land during the polcy period to provide recommedation to the customer if any deviation found while providing the policy.  
- If customer approach for claim then insurer again inspection the land using drone and understand how much damage happended on the land and provide the claim amount accordingly.  
```

## Technical Data Flow:  

```sh
- Using the Microsoft Custom Vision service, we have trained the model which can identify Cultivalted, InFertileLand, High quality crop, Low quality crop and other lands. This trained model will provide a Tensor flow(*.TB) file which will then be used by RedisAI to help image modelling of images returned through drone.  
- When insurer register a new customer, front end app will call "Savecustomer" API to save the data in MySQL DB.  
- When insurer clicks on the inspection button from the front end portal, a signal with new Inspection ID will be pushed to Redis Stream named 'inspection' which will inform Drone to start the inspection of the land.  
- When the drone is flying over the simulated land, it keep pushing images to Redis stream named 'inspectiondata' and RedisGears container which is listening to that Redis Stream will process this images using trained transor flow model at RedisAI.
- This modelled images are then saved to Azure blob storage and all other information will be pushed to redis stream which will then be consumed by front end app where it is showing all data to insurer portal.    
- When all data is received at the front end, it calls "SaveInspection" API to save all data to the MSQL DB.  
- Also based on this information system will automatically show sumassured and single premimum (single premium value also added a risk factor based on past claimed data of all other customers in that area) to the portal where customer and insurer can agree and create a new policy.  
- Similarly insurer can do multiple inspection of the same property and if required after inspection, insurer can generate a claim for the given policy.      
- Front end portal will interact with different microservices to save and get the data on the portal.   
```

## High Level Architecture Diagram:  

![image](https://user-images.githubusercontent.com/83917397/118373643-9e188280-b5d5-11eb-8310-51c462572ed1.png)


## Technology Stack

**Development**  
 
- [Next.JS](https://nextjs.org/)
- [Python](https://www.python.org/)
- [Java](https://www.java.com/en/)
- [Springboot](https://spring.io/projects/spring-boot)
   
**Cloud and Services**  

- [Azure cloud](https://azure.microsoft.com/en-in/)
- [Redis Gears](https://redislabs.com/modules/redis-gears/)
- [Redis AI](https://redislabs.com/modules/redis-ai/)
- [Redis Cache](https://redis.io/)
- [Redis Streaming](https://redis.io/topics/streams-intro)
- [Dockers](https://www.docker.com/)
- [Microsoft Airsim](https://microsoft.github.io/AirSim/)
- [Custom Vision Service](https://azure.microsoft.com/en-us/services/cognitive-services/custom-vision-service/)

## Run Application in Docker Environment

Run the below command from the root folder:
```sh
docker-compose up
```
## README.MD for the sub projects

- [Redis_Airsim](https://github.com/piyushjaincloud2/CropInsurRedis/blob/main/Redis_Airsim/README.md)
- [Frontend](https://github.com/piyushjaincloud2/CropInsurRedis/blob/main/frontend/README.md)
-  [Microservices](https://github.com/piyushjaincloud2/CropInsurRedis/blob/main/microservices/README.md)

## Troubleshooting

Sometimes you might face an issue in the inspection screen when you are receiving images captured by the drone, the page goes in the loading state to continously get the images. In that case, please restart the front end webapp container named `cropinsurredis_droan-webapp_1` and trigger in inspection again.

## Known Issues

- After converting to claim, claim amount is not showing on the front-end app
- Missing proper validations on the customer validation form, so proper data needs to be entered otherwise it will give 500 error.


## Product Future Enhancements

- Provide the feature to search the Customer within the app.
- Add a risk factor while calculating sum assured and premium based on the past data of a particular location.
- In the Inspection table, recent inspections coming from the stream should appear on the top.
- Export the policy data in `PDF` format.


## Application Screenshots
#### Login page
![image](https://piyushjaincloud2.github.io/CropInsurRedis/login.png)
#### Customer Registration page
![image](https://piyushjaincloud2.github.io/CropInsurRedis/customer-register.png)
#### Customer List page
![image](https://piyushjaincloud2.github.io/CropInsurRedis/customer-list.png)
#### Inspection page
![image](https://piyushjaincloud2.github.io/CropInsurRedis/inspection-data.png)
