## Policy-Service:-
This Service is used to handle all Policy and Claim related requests and created all policy and claims specific endpoints.
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
 Step 4: mvn spring-boot:run
``` 
#### Steps to Setup in docker enviornment
```
 Step 1: Download and Install Docker
 Step 2: mvn clean package ```(Need to run this command in root dir of MicroService)
 Step 3: docker build -f Dockerfile -t policy-service .
 Step 4: docker run -d -p 8081:8081 policy-service
```
#### Want to run all MicroServices in One Command
```docker-compose up```

#### API EndsPoints

```
Create Policy:- POST http://localhost:8081/policy/save
Create Claim:- POST http://localhost:8081/policy/claim

```
[Download Postman Collection](https://github.com/sagarmal624/RedisLabs-Policy-Service/blob/master/Redis%20Lab.postman_collection.json)