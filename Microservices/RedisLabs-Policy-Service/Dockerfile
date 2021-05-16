FROM openjdk:11
ADD target/policy-0.0.1-SNAPSHOT.war  policy-0.0.1-SNAPSHOT.war
EXPOSE 8081
ENTRYPOINT ["java","-jar","policy-0.0.1-SNAPSHOT.war"]