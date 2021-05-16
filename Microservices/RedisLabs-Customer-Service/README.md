## Customer-Service:-
This Service is used to handle all customer related requests and created all customer specific endpoints.
### Technology Stack:-
 Java,SpringBoot,RestAPI,Mysql etc

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

#### Steps to Setup on Local
``` 
 Step 1: Install Java 8+ Version
 Step 2: Install Latest Maven
 Step 3: Download and Install Mysql8+ version
 Step 4: mvn clean install
 Step 5: Update jdbc connection host,username,password,db etc in propertiles file
 Step 4: mvn spring-boot:run
``` 
 
#### Steps to Setup in docker enviornment
```
 Step 1:  Download and Install Docker
 Step 2:  mvn clean package (Need to run this command in root dir of MicroService)
 Step 3:  docker build -f Dockerfile -t customer-service .
 Step 4:  docker run -d -p 8080:8080 customer-service
```
#### Want to run all MicroServices in One Command

```docker-compose up```

#### API EndsPoints
```
Save Customer:- POST http://localhost:8080/customer/save
Get Customer by Id:- GET http://localhost:8080/customer/get/4cb4bdd9-492d-49f2-8e98-c11f5902015f```
Get All Customer:- GET http://localhost:8080/customer/get
```

[Download Postman Collection](https://github.com/sagarmal624/RedisLabs-Customer-Service/blob/master/Redis%20Lab.postman_collection.json)