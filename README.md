# Assignement 3 : Data-as-a-Service


## About 

We previously decoupled our application into two microservices - Streamlit and FastAPI, along with dockerization and Airflow.
In the scope of this assignment, <br>
We have enabled rate limiting for authentiacated users in accordance to the plan specific to a user. <br>
Enhanced the Streamlit application with adding a dashboard to track users' activity and show analytics at user level for registered authenticated users. <br>
Designed a CLI for accessing the endpoints and packaged it as a wheel. <br>



## Links
* Codelab Documentation - [Codelab](https://codelabs-preview.appspot.com/?file_id=1CwPu13u5ciGguLL0QcZjw2f8TZfOqSlW74EaKc7tRBE/#2)
* GitHub Organization - [GitHub](https://github.com/BigDataIA-Spring2023-Team-12)
* Streamlit Application - [Streamlit]()
* FastAPI - [FastAPI]()


## LEARNINGS/TECH USED
Streamlit<br>
AWS<br>
SQLite<br>
Great-Expectations<br>
Pytest<br>
AirFlow<br>
FastAPI<br>
Docker<br>
Contrab<br>
Rate Limiting<br>
Designing CLI<br>
Creating a python package as wheel<br>
End-user testing<ur>
Git (Version Control)<br>
Documentation on Codelabs<br>


## Process Flow

1. Made public and private endpoints with JWT Token based authentication enabled for private endpoints.
2. Designed service plan as below:
- Free - 10 API request limit - reset everyhour
- Gold - 15 API request limit - reset everyhour
- Platinum - 20 API request limit  - reset everyhour
3. Created user registration page with functionality
- Registering as new user and choosing a plan
- Feature to change the password
4. Test the workflow using 3 users each created for a specific plan   
5. Enhanced the logging to capture all user activity request to check the API request count and compare with enrolled plan for the given user.
6. Designed dashboard within streamlit accessible by the admin/developers/owner only to track users’ activity
7. Designed a dashboard for user level analytics 
8. Created a CLI using typer1 to execute the functionality
9. Package the entire CLI as a python wheel package to access all endpoints 
10. Dockerize the microservices
11. Deploy on cloud


### Project Directory Structure

##### /FastAPI
This folder contains all the functions created for FastAPI endpoints and their respective functional dependencies.

##### /CronJob
The folder contains a python file to update scape the metadata which will be used for daily scheduling of cron to keep the metadata updated.
##### /database
All the SQLite databases and present under this folder.
##### /ge
All the files related related to great-expectations data validation, such as validation suites, checkpoints and generated reports are contained under this folder.
##### /streamlit
The entire user-interface built using streamlit, the login/registration page, GEOS and Nexrad file downloads and dashboards.
##### /test
The folder contains files with functions written for unit testing.



## Run the project
1. Open terminal
2. Browse the location where you want to clone the repository
3. Write the following command and press enter 
````
 git clone https://github.com/BigDataIA-Spring2023-Team-12/JWT-Docker-FastAPI-Wheel-Airflow-Streamlit.git
 ````
 4. Create a virtual environment and activate
 ````
  python -m venv <Virtual_environment_name>
 ````
 5. Install the required dependencies using requirements.txt
 ````
  pip install -r /path/to/requirements.txt
 ````
6. Start up docker desktop, docker compose up and run all required containers.
7. Launch the application by firing up the main.py file in /streamlit




---
## Team Members
1. Harsh Shah - NUID: 002704406 - (shah.harsh7@northeastern.edu)
2. Parva Shah - NUID: 002916822 - (shah.parv@northeastern.edu)
3. Dev Shah - NUID: 002978981 - (shah.devs@northeastern.edu)



## Undertaking

> WE ATTEST THAT WE HAVEN’T USED ANY OTHER STUDENTS’ WORK IN OUR ASSIGNMENT AND ABIDE BY THE POLICIES LISTED IN THE STUDENT HANDBOOK
**Contribution**: 
*   Harsh Shah &emsp; :`33.33%`
*   Parva Shah &emsp; :`33.33%`
*   Dev Shah &emsp;   :`33.33%`







