import typer
import requests
from Functions.auth import AuthHandler
from pydantic import BaseModel
from bcrypt import hashpw, gensalt

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
