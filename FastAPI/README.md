## FastAPI
As part of FastAPI implementation, the functions provides endpoints to register new users, login, extract files from Geos and Nexrad, and download files from Geos and Nexrad.
A user is authenticated with the credentials and the rate limiting is monitored based on the plan created for a specific user.


### Installation
Install the following packages:
- FastAPI
- pydantic
- uvicorn

These can be installed packages using pip:
```
pip install fastapi pydantic uvicorn 
```

##### Getting Started
To start the server, run the following command in your terminal:
```
uvicorn main:app --reload
```
This will start the server at http://localhost:8000/.


# Endpoints

## Register new user

**POST /register**

This endpoint allows users to register new accounts. It expects a JSON object with the following keys:

- `name`: The name of the user.
- `username`: The username for the account.
- `password`: The password for the account.
- `plan`: The subscription plan for the account.

If the registration is successful, the endpoint returns a JSON object with the following keys:

- `success`: A boolean indicating whether the registration was successful.
- `message`: A message indicating that the registration was successful.

If the registration fails, the endpoint returns an error message with a 400 status code.

## Login

**POST /login**

This endpoint allows users to log in to their accounts. It expects a JSON object with the following keys:

- `username`: The username for the account.
- `password`: The password for the account.

If the login is successful, the endpoint returns a JSON object with the following keys:

- `success`: A boolean indicating whether the login was successful.
- `message`: A message indicating that the login was successful.
- `token`: A JWT token that can be used to authenticate future requests.

If the login fails, the endpoint returns an error message with a 401 status code.

## Extract files from Geos by path

**GET /geos-get-by-path/{username}/{station}/{year}/{day}/{hour}**

This endpoint extracts all files from Geos by path. It expects the following path parameters:

- `username`: The username for the account.
- `station`: The station for the files.
- `year`: The year for the files.
- `day`: The day for the files.
- `hour`: The hour for the files.

If the extraction is successful, the endpoint returns a JSON object with the following keys:

- `success`: A boolean indicating whether the extraction was successful.
- `message`: A message indicating that the extraction was successful.
- `data`: A list of extracted files.

If the extraction fails, the endpoint returns an error message with a 400 status code.

## Extract files from Nexrad by path

**GET /nexrad-get-by-path/{username}/{year}/{month}/{day}/{station}**

This endpoint extracts all files from Nexrad by path. It expects the following path parameters:

- `username`: The username for the account.
- `year`: The year for the files.
- `month`: The month for the files.
- `day`: The day for the files.
- `station`: The station for the files.

If the extraction is successful, the endpoint returns a JSON object with the following keys:

- `success`: A boolean indicating whether the extraction was successful.
- `message`: A message indicating that the extraction was successful.
- `data`: A list of extracted files.

If the extraction fails, the endpoint returns an error message with a 400 status code.

## Download file from Geos by filename

**GET /geos-download-by-name/{username}/{filename}**

This endpoint downloads a file from Geos by filename.

## Download file from Nexrad by filename

**GET /nexrad-download-by-name/{username}/{filename}**

This endpoint downloads a file from Nexrad by filename.