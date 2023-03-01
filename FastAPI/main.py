from fastapi import FastAPI, Depends, HTTPException, Body, BackgroundTasks
from Functions.auth import AuthHandler
from Functions.schema import LoginDetails, RegisterDetails
from Functions.database import check_username_taken, register_user, get_password, login_user, log_data, verify_token

from Functions.extractFiles import extract_files
from Functions.urlGen import geos_url_gen
from Functions.urlGen import nexrad_url_gen

app = FastAPI()

auth_handler = AuthHandler()
users = []


# endpoint to register new user
@app.post('/register', status_code=201)
def register(register: RegisterDetails):
    # if block checks is username is taken
    if check_username_taken(register.username):  # <---- Function check_user needed
        raise HTTPException(status_code=400, detail='Username is taken')
    # hash the password
    hashed_password = auth_handler.get_password_hash(register.password)
    # append user info into DB
    res = register_user(register.name, register.username, hashed_password, register.plan)
    return res


# endpoint to login user
@app.post('/login')
def login(login: LoginDetails, status_code=201):
    endpoint = "/login"
    # if block checks if username or password is incorrect and raises an error    
    if (not check_username_taken(login.username)) or (not auth_handler.verify_password(login.password, get_password(
            login.username))):  # <------ Function verify_user needed
        raise HTTPException(status_code=401, detail='Invalid username and/or password')
    # create access token 
    token = auth_handler.encode_token(login.username)
    # updates the user's access to new token 
    status = login_user(token, login.username)
    # log user data 
    log_data(login.username, endpoint, call_status=201)
    return status


# endpoint to change password


# endpoint to extract all files from geos by path
@app.get("/geos-get-by-path/{username}/{station}/{year}/{day}/{hour}")
async def geos_get_files_path(username, station, year, day, hour):
    # define endpoint
    endpoint = f"/geos-get-by-path/{username}/{station}/{year}/{day}/{hour}"
    # If block checks token validity
    if verify_token(username):
        # extract all files
        path = "{}/{}/{}/{}/".format(station, year, day, hour)
        result = extract_files("noaa-goes18", path)
        # if block checks if the result is valid, if not it raises error
        if not result:
            # logging if any error
            log_data(username, endpoint, call_status=400)
            raise HTTPException(status_code=400, detail='path parameters not valid')
        # logging successful calls
        log_data(username, endpoint, call_status=201)
        return result


# endpoint to extract all files from nexrad by path
@app.get("/nexrad-get-by-path/{username}/{year}/{month}/{day}/{station}")
async def nexrad_get_files_path(username, year, month, day, station):
    # define endpoint
    endpoint = f"/nexrad-get-by-path/{username}/{year}/{month}/{day}/{station}"
    # If block checks token validity
    if verify_token(username):
        # extract all files
        path = "{}/{}/{}/{}/".format(year, month, day, station)
        result = extract_files("noaa-nexrad-level2", path)
        # if block checks if the result is valid, if not it raises error
        if not result:
            # logging if any error
            log_data(username, endpoint, call_status=400)
            raise HTTPException(status_code=400, detail='path parameters not valid')
        # logging successful calls
        log_data(username, endpoint, call_status=201)
        return result


# endpoint to download file from geos by filename
@app.get("/geos-download-by-name/{username}/{filename}")
async def geos_download_file_name(username, filename):
    # define endpoint
    endpoint = f"/geos-download-by-name/{username}/{filename}"
    # If block checks token validity
    if verify_token(username):
        # try block tests if there are any errors, expect block is executed if error
        try:
            result = geos_url_gen(filename)
        except:
            # logs error in DB
            log_data(username, endpoint, call_status=400)
            raise HTTPException(status_code=400, detail='Filename is not valid!')
        # logging successful calls
        log_data(username, endpoint, call_status=201)
        return result


# endpoint to download file from nexrad by filename
@app.get("/nexrad-download-by-name/{username}/{filename}")
async def nexrad_download_file_name(username, filename):
    # define endpoint
    endpoint = f"/nexrad-download-by-name/{username}/{filename}"
    # try block tests if there are any errors, expect block is executed if error
    if verify_token(username):
        try:
            result = nexrad_url_gen(filename)
        except:
            # logs error in DB
            log_data(username, endpoint, call_status=400)
            raise HTTPException(status_code=400, detail='Filename is not valid!')

        # logging successful calls
        log_data(username, endpoint, call_status=201)
        return result
