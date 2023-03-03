import typer
import httpx
import requests
from pydantic import BaseModel
from bcrypt import hashpw, gensalt
from Functions.auth import AuthHandler
from Functions.schema import LoginDetails, RegisterDetails, ChangePasswordDetails
from Functions.database import check_username_taken, register_user, get_password, login_user, log_data, verify_token, call_counter, verify_rate_limit
from Functions.database import reset_calls, verify_admin, admin_data, update_password,user_data
from Functions.extractFiles import extract_files
from Functions.uploadFileToS3 import upload_file_to_s3
from fastapi import Request, HTTPException

from Functions.urlGen import geos_url_gen
from Functions.urlGen import nexrad_url_gen

from Functions.extractFiles import extract_files



app = typer.Typer()
auth_handler = AuthHandler()



base_url = "http://localhost:8000"

"""def hash_password(password: str):
    salt = gensalt()
    hashed = hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')"""

@app.command()
def register_user(name: str, username: str, password: str, plan: str):
    #hashed_password = hash_password(password)
    url = f"{base_url}/register"
    data = {
        "name": name,
        "username": username,
        "password": password,
        "plan": plan
    }
    response = requests.post(url, json=data)
    if response.ok:
        typer.echo("User registered successfully!")
    else:
        typer.echo(response.json()["detail"])




@app.command()
def login_user(username: str, password: str):
    url = f"{base_url}/login"
    data = {
        "username": username,
        "password": password
    }
    response = requests.post(url, json=data)
    if response.ok:
        typer.echo("User logged in successfully!")
        token = response.json()["token"]
        typer.echo(f"Access token: {token}")
    else:
        typer.echo(response.json()["detail"])


@app.command()
def change_password(username: str, current_password: str, new_password: str):
    url = f"{base_url}/change-password"
    data = {
        "username": username,
        "current_password": current_password,
        "new_password": new_password
    }
    response = requests.post(url, json=data)
    if response.ok:
        typer.echo("Password changed successfully!")
    else:
        typer.echo(response.json()["detail"])







@app.command()
def geos_get_files_path(
    username: str = typer.Argument(..., help="The username of the user making the request"),
    station: str = typer.Argument(..., help="The station of the files to be extracted"),
    year: str = typer.Argument(..., help="The year of the files to be extracted"),
    day: str = typer.Argument(..., help="The day of the files to be extracted"),
    hour: str = typer.Argument(..., help="The hour of the files to be extracted"),
):
    """
    Extracts files based on the provided parameters.
    """
    # Define endpoint URL
    endpoint = f"http://localhost:8000/geos-get-by-path/{username}/{station}/{year}/{day}/{hour}"

    # Send HTTP GET request to endpoint
    response = httpx.get(endpoint)

    # Check response status code
    if response.status_code == 200:
        typer.echo(response.text)
    else:
        typer.echo(f"Error: {response.status_code} - {response.text}")








"""
@app.command()
def geos_get_files_path(
    username: str = typer.Argument(..., help="The username of the user making the request"),
    station: str = typer.Argument(..., help="The station of the files to be extracted"),
    year: str = typer.Argument(..., help="The year of the files to be extracted"),
    day: str = typer.Argument(..., help="The day of the files to be extracted"),
    hour: str = typer.Argument(..., help="The hour of the files to be extracted"),
):
  
    # Import required modules

    # Define endpoint
    endpoint = f"/geos-get-by-path/{username}/{station}/{year}/{day}/{hour}"

    # Verify if plan rate is exceeded
    if not verify_rate_limit(username):
        log_data(username, endpoint, call_status=429)
        raise HTTPException(status_code=429, detail='API rate limit exceeded! Upgrade plan to continue')

    # Get user's IP address
    ip = Request().client.host

    # Check token validity and IP address
    if verify_token(username, ip):
        # Extract all files
        path = f"{station}/{year}/{day}/{hour}/"
        result = extract_files("noaa-goes18", path)

        # Check if the result is valid, if not it raises an error
        if not result:
            # Log error
            log_data(username, endpoint, call_status=400)
            raise HTTPException(status_code=400, detail='Path parameters not valid')

        # Log successful call
        log_data(username, endpoint, call_status=201)

        # Increment API call counter
        call_counter(username)

        return result







@app.command()
def geos_get_files_path(username: str, station: str, year: int, day: int, hour: int):
    url = f"{base_url}/geos-get-by-path/{username}/{station}/{year}/{day}/{hour}"
    #path = f"{station}/{year}/{day}/{hour}"
    response = requests.get(url)
    if response.ok:
        #extract_files("noaa-goes18",path)

        typer.echo("Files extracted successfully!")
        typer.echo(response.json())
    else:
        typer.echo(response.json()["detail"])


"""


@app.command()
def nexrad_get_files_path(username: str, year: int, month: int, day: int, station: str):
    url = f"{base_url}/nexrad-get-by-path/{username}/{year}/{month}/{day}/{station}"
    response = requests.get(url)
    if response.ok:
        typer.echo("Files extracted successfully!")
        typer.echo(response.json())
    else:
        typer.echo(response.json()["detail"])



if __name__ == "__main__":
    app()
