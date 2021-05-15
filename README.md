## Dronification of Crop Insurar using Drone, Redis and cloud technologies

Enable Crop Insurance company to generate insurance policy and claim settlement using Drone, Redis and Cloud Technologies to ensure transparency, Quick turn around time with 100% accuracy and client satisfaction.  

## Demo Flow:  

```sh
- Insurer logins to the portal using his credentials.  
- Register for new customer with property information.  
- Do the First inspection of the Property using drone to check, how much land is cultivated and based on this information generate sum assured and premium.  
- If Customer is fine with this information create a policy for the customer.  
- As per policy term and condition insurer is free to do another inspection of the land during the polcy period to provide recommedation to the customer if any deviation found while providing the policy.  
- If customer approach for claim then insurer again inspection the land using drone and understand how much damage happended on the land and provide the claim amount accordingly.  
```

## Technical Data Flow:  

```sh
- Using a micorsoft custom vision service, we have trained the model which can identify cultivalted, un-cultivated, high quality crop, low quality crop and other lands, this trained model will provide a Tensor flow(*.TB) file which will be used by Redis AI to help imgage modelling for drone generated images.  
- When insurer register a new customer, front end app will call "Savecustomer" API to save data in the MySQL DB.  
- When insurer click on the inspection button from the front end portal, A signal with new Inspection ID will be push to Redis Stream which inform Drone to start inspection of the land as the information provided by customer.  
- Drone started inspection, it keep pushing images to Redis stream and redis gears container will process this images using pre defined/trained transor flow model.  
- This Modelled  images save to Azure blob storage and all other information will be push to redis stream to front end app where it showing all data to insurer portal.    
- When Drone stop scanning complete, front end will call "SaveInspection" API to save all data to the MSQL DB.  
- Also based on this information system will automatically show sumassured and single premimum (single premium value also added a risk factor based on past claimed data of all other customers in that area) to the portal where customer and insurer can agree and create a new policy.  
- Similarly insurer can do multiple inspection of the same property and if required after inspection, insurer can generate a claim for the given policy.      
- Front end portal will intract with differnt microservices to save and get the data on the portal.   
```

## High Level Architecture Diagram:  

![image](https://user-images.githubusercontent.com/83917397/118265997-9d99c200-b4d7-11eb-9494-2c3f735b6041.png)


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

[Docker Compose File](https://github.com/piyushjaincloud2/CropInsurRedis/blob/main/docker-compose.yml)

Command:

``` docker-compose up```

