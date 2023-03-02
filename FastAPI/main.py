from fastapi import FastAPI, HTTPException, Request
from Functions.auth import AuthHandler
from Functions.schema import LoginDetails, RegisterDetails, ChangePasswordDetails
from Functions.database import check_username_taken, register_user, get_password, login_user, log_data, verify_token, call_counter, verify_rate_limit
from Functions.database import reset_calls, verify_admin, admin_data, update_password,user_data
from Functions.extractFiles import extract_files
from Functions.uploadFileToS3 import upload_file_to_s3

from Functions.urlGen import geos_url_gen
from Functions.urlGen import nexrad_url_gen
from fastapi_utils.tasks import repeat_every
import pandas as pd


app = FastAPI()
auth_handler = AuthHandler()

# This function repeats every 1 hour and resets all api_calls to 0
@app.on_event("startup")
@repeat_every(seconds=60)  # 1 hour
def reset_api_calls() -> None:
    reset_calls()
    

# endpoint to register new user
@app.post('/register', status_code=201)
def register(register: RegisterDetails):
    # if block checks is username is taken
    if check_username_taken(register.username): # <---- Function check_user needed
        raise HTTPException(status_code=400, detail='Username is taken')
    # hash the password
    hashed_password = auth_handler.get_password_hash(register.password)
    # append user info into DB
    res = register_user(register.name,register.username,hashed_password,register.plan)
    return res

# endpoint to login user
@app.post('/login')
def login(login: LoginDetails, request: Request):
    endpoint= "/login"
    # if block checks if username or password is incorrect and raises an error    
    if (not check_username_taken(login.username)) or ( not auth_handler.verify_password(login.password, get_password(login.username))):#<------ Function verify_user needed
        raise HTTPException(status_code=401, detail='Invalid username and/or password')
    # get users ip address
    ip = request.client.host
    # create access token 
    token = auth_handler.encode_token(login.username)
    # updates the user's token and ip_address  
    status = login_user(token,login.username,ip)
    # log user data 
    log_data(login.username, endpoint, call_status=201)
    return status


# endpoint to change password
@app.post('/change-password')
def change_password(change: ChangePasswordDetails, request: Request):
    endpoint= '/change-password'
    # if block checks if username or password is incorrect and raises an error    
    if (not check_username_taken(change.username)) or ( not auth_handler.verify_password(change.current_password, get_password(change.username))):#<------ Function verify_user needed
        raise HTTPException(status_code=401, detail='Invalid username and/or password')
    # get users ip address
    ip = request.client.host
    if verify_token(change.username,ip):
         # hash the password
        hashed_password = auth_handler.get_password_hash(change.new_password)
        # append user info into DB
        res = update_password(change.username, hashed_password)
        return res

# endpoint to extract all files from geos by path
@app.get("/geos-get-by-path/{username}/{station}/{year}/{day}/{hour}")
async def geos_get_files_path(username,station,year,day,hour,request: Request):
    # define endpoint
    endpoint = f"/geos-get-by-path/{username}/{station}/{year}/{day}/{hour}"
    # verify if plan rate is exceeded
    if not verify_rate_limit(username):
        log_data(username, endpoint, call_status=429)
        raise HTTPException(status_code=429, detail='API rate limit exceeded! upgrade plan to continue')
    
    # get users ip address
    ip = request.client.host
    # If block checks token validity and ip_address
    if verify_token(username,ip):
        # extract all files
        path = "{}/{}/{}/{}/".format(station, year, day, hour)
        result = extract_files("noaa-goes18",path)
        # if block checks if the result is valid, if not it raises error
        if not result:
            # logging if any error
            log_data(username, endpoint, call_status=400)
            raise HTTPException(status_code=400, detail='path parameters not valid')
        # logging successfull calls
        log_data(username, endpoint, call_status=201)
        # API call counter
        call_counter(username)
        return result
    

# endpoint to extract all files from nexrad by path
@app.get("/nexrad-get-by-path/{username}/{year}/{month}/{day}/{station}")
async def nexrad_get_files_path(username,year,month,day,station,request: Request):
    # define endpoint
    endpoint = f"/nexrad-get-by-path/{username}/{year}/{month}/{day}/{station}"
     # verify if plan rate is exceeded
    if not verify_rate_limit(username):
        log_data(username, endpoint, call_status=429)
        raise HTTPException(status_code=429, detail='API rate limit exceeded! upgrade plan to continue')
    
    # get users ip address
    ip = request.client.host
    # If block checks token validity
    if verify_token(username,ip):
        # extract all files
        path = "{}/{}/{}/{}/".format(year,month,day,station)
        result = extract_files("noaa-nexrad-level2",path)
        # if block checks if the result is valid, if not it raises error
        if not result:
            # logging if any error
            log_data(username, endpoint, call_status=400)
            raise HTTPException(status_code=400, detail='path parameters not valid')
        # logging successfull calls
        log_data(username, endpoint, call_status=201)
        # API call counter
        call_counter(username)
        return result


# endpoint to download file from geos by filename
@app.get("/geos-download-by-name/{username}/{filename}")
async def geos_download_file_name(username,filename,request: Request):
    # define endpoint
    endpoint = f"/geos-download-by-name/{username}/{filename}"
     # verify if plan rate is exceeded
    if not verify_rate_limit(username):
        log_data(username, endpoint, call_status=429)
        raise HTTPException(status_code=429, detail='API rate limit exceeded! upgrade plan to continue')
    
    # get users ip address
    ip = request.client.host
    # If block checks token validity
    if verify_token(username,ip):
        # try block tests if there are any errors, expect block is executed if error
        try:
            result = geos_url_gen(filename)
        except:
            # logs error in DB
            log_data(username, endpoint, call_status=400)
            raise HTTPException(status_code=400, detail='Filename is not valid!')
        # logging successfull calls
        log_data(username, endpoint, call_status=201)
        # API call counter
        call_counter(username)
        return result
    
# endpoint to download file from nexrad by filename
@app.get("/nexrad-download-by-name/{username}/{filename}")
async def nexrad_download_file_name(username,filename,request: Request):
    # define endpoint
    endpoint = f"/nexrad-download-by-name/{username}/{filename}"
     # verify if plan rate is exceeded
    if not verify_rate_limit(username):
        log_data(username, endpoint, call_status=429)
        raise HTTPException(status_code=429, detail='API rate limit exceeded! upgrade plan to continue')
    
    # get users ip address
    ip = request.client.host
    # try block tests if there are any errors, expect block is executed if error
    if verify_token(username,ip):
        try:
            result = nexrad_url_gen(filename)
        except:
            # logs error in DB
            log_data(username, endpoint, call_status=400)
            raise HTTPException(status_code=400, detail='Filename is not valid!')
            
        # logging successfull calls
        log_data(username, endpoint, call_status=201)
        # API call counter
        call_counter(username)
        return result
    
@app.get("/get-admin-data/{username}")
async def get_admin_data(username,request: Request):
    # define endpoint
    endpoint = f"/get-admin-data/{username}"
     # verify if plan rate is exceeded
    if not verify_admin(username):
        raise HTTPException(status_code=400, detail='unauthorized access!')
    
    # get users ip address
    ip = request.client.host
    # try block tests if there are any errors, expect block is executed if error
    if verify_token(username,ip):
        # data is extracted in json format
        admin_data = admin_data()
        return admin_data

# get user data
@app.get("/get-user-data/{username}")
async def get_user_data(username,request: Request):
    # get users ip address
    ip = request.client.host
    # try block tests if there are any errors, expect block is executed if error
    if verify_token(username,ip):
        # data is extracted in json format
        users_data = user_data(username)
        return users_data

