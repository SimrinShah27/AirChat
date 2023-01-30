# AirChat

DEMO: https://youtu.be/3zg3TSoShLA
A chatbot is a computer program that simulates and processes a query initiated by a user. Here, a simple rule based chatbot is created which will effectively glue
the different cloud technologies in an efficient way and inculcate the concepts covered in class. This chatbot will assist users in tracking flights, finding the cheapest flight tickets for their desired travel dates, check prices for alternate routes, get the cheapest tickets based on month and check the ratings of the airlines based on features like Customer satisfaction, Luggage and overall ratings. Overall, this chatbot is an airways information based chatbot.
In this project, the four different cloud technologies such as API Interfaces, Databases, Messaging queues and Containers are used to create a simple rulebased chatbot. Firstly, API Interfaces are used to fetch the data which will provide the access to the records of the data set. Next, the user activity will be logged in the database which will also help in debugging the project. Databases will also be used to lookup airport and airline codes and store reviews which will be processed for providing the airline ratings. Later we will be using the Messaging Queue to send desired information to users via mails. Finally, we will be making use of containers, Docker, to deploy the application in the cloud.

This chatbot will enable the user to:
1. Track flights and retrieve flight status information in real-time.
2. Find the cheapest tickets for the desired route.
3. Find the cheapest tickets grouped by month.
4. Find the prices for the alternate directions between the nearest to target
cities.
5. Get ratings based on twitter reviews of the airlines for factors like customer
satisfaction, user-friendly booking and luggage service.
6. Receive an email if they wish, regarding specific flight details that they
queried about.

Software Components: The software components required to build this project
are:
• API Interface:
(i) AviationStack API - To track the real time flight status.
(ii) TravelPayouts API - To retrieve the details of the flight
(iii) SendGrid API - To send the emails
• Database:
Sqlite - Sqlite as a Relational Database
• Messaging Queue:
RabbitMQ - To queue the messages when user requests and
delivers email based on the queue.
• Container:
(i) Docker - To deploy the application in the cloud
(ii) Kubernetes - To run multiple containers.
• Python Framework:
Flask - To build web applications (REST server)
• Cloud Platform:
Google Cloud Platform - To deploy flask application

Application Architectural Diagram Showing Interactions
![image](https://user-images.githubusercontent.com/113396912/192407015-dc8ecf9e-0085-4c63-8411-b3d5f735fb6b.png)

DEBUGGING
For debugging we have maintained the logs at each stage of the process including
information and errors. The logger logs every step right from user input to the
output which is displayed. Using the logger we found if any error occurred and
then found out what is causing the error. Using the backtracking strategy we could
locate the point where the logic went wrong and rectified the logic accordingly.
TRAINING
The chatbot is trained such that for each intent we have a set of training words and
sentences which will help identify the user query and respond accordingly.
TESTING
We have tested the chatbot with a set of user queries and expected responses.
Based on the response given by the chatbot we have maintained a score for each
intent. If the output of the chatbot matches the expected output, that intent will
have a higher score than the ones with the incorrect output. This score helped in a
way that incase the intent clashes, the intent with the higher score will be used.


