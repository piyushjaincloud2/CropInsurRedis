FROM openjdk:11
ADD target/customer-0.0.1-SNAPSHOT.war  customer-0.0.1-SNAPSHOT.war
EXPOSE 8080
ENTRYPOINT ["java","-jar","customer-0.0.1-SNAPSHOT.war"]