## Inspection-Service:-
This Service is used to handle all Inspection related requests and created all Inspection specific endpoints.
### Technology Stack:-
 Java,SpringBoot,RestAPI,Mysql,RedisCache etc.

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

#### Steps to Setup on Local
```
 Step 1: Install Java 8+ Version
 Step 2: Install Latest Maven
 Step 3: Download and Install Mysql8+ version
 Step 4: mvn clean install
 Step 5: Update jdbc connection host,username,password,db etc in propertiles file
 Step 6: mvn spring-boot:run
```
#### Steps to Setup in docker environment
```
 Step 1: Download and Install Docker
 Step 2: mvn clean package(Need to run this command in root dir of MicroService)
 Step 3: docker build -f Dockerfile -t inspection-service .
 Step 4: docker run -d -p 8082:8082 inspection-service
```
#### Want to run all MicroServices in One Command?
```docker-compose up```

#### API EndsPoints
```
Create Inspection:- ```POST http://localhost:8082/inspection/save```
Get Inspection by Inspection Id:- ```GET http://localhost:8082/inspection/get/4cb4bdd9-492d-49f2-8e98-c11f5902015f```
Get Inspections by Customer Id:- ```GET http://localhost:8082/inspection/findByCustomerId/sasa2d92d-49f2-8e98-c11f5902015f```
```
[Download Postman Collection](https://github.com/sagarmal624/RedisLabs-Policy-Service/blob/master/Redis%20Lab.postman_collection.json)