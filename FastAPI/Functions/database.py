import sqlite3
import pandas as pd
import os
from datetime import datetime
from Functions.auth import AuthHandler
from fastapi import HTTPException

# create table in the sqlite databae conn = sqlite3.connect("../auth_data.db") cursor = conn.cursor() cursor.execute(
# "CREATE TABLE IF NOT EXISTS users (username TEXT ,name TEXT, password TEXT, token TEXT, tier INTEGER, role TEXT,
# join_date TEXT, PRIMARY KEY (username), FOREIGN KEY(username) REFERENCES logs(logs))") cursor.execute("CREATE TABLE
# IF NOT EXISTS logs (username TEXT ,timestamp TEXT, endpoint TEXT, call_status INTEGER, PRIMARY KEY (username,
# timestamp))")

auth_handler = AuthHandler()


def get_db(db):
    # establish connection with db
    db_path = os.getcwd() + "/{}".format(db)
    conn = sqlite3.connect(db_path, check_same_thread=False)
    cursor = conn.cursor()
    return conn, cursor


def get_user_auth_table():
    db_path = os.getcwd() + "/{}".format(db)
    conn = sqlite3.connect(db_path, check_same_thread=False)
    cur = conn.cursor()
    df = pd.read_sql_query("SELECT * FROM user_auth", conn)
    return df


# check user in DB
def check_username_taken(username):
    # conect to db
    conn, cur = get_db("auth_data.db")
    # checks if username exists in table
    res = cur.execute(f"SELECT username FROM users WHERE users.username = '{username}'")
    check = res.fetchone()
    # Close the database connection
    conn.close()

    if check is None:
        return False
    else:
        return True


# Get password for a given username
def get_password(username):
    # connect to db
    conn, cur = get_db("auth_data.db")
    # get password of given username
    res = cur.execute(f"SELECT password FROM users WHERE users.username = '{username}'")
    password = res.fetchone()
    # Close the database connection
    conn.close()
    if password == None:
        return False
    return password[0]


def login_user(token, username):
    # connect to db
    conn, cur = get_db("auth_data.db")
    # Execute the UPDATE query to update token the row to the table
    query = "UPDATE users SET token = '{0}' WHERE username = '{1}'".format(token, username)
    cur.execute(query)
    # Commit the changes to the database
    conn.commit()
    # Close the database connection
    conn.close()
    return {"status": f"{username} logged in Successfully!"}


# Register user & append user details in databas
def register_user(name, username, password, plan):
    # connect to DB
    conn, cur = get_db("auth_data.db")
    # get joining time
    join_date = datetime.now()
    # Execute the INSERT query to add the row to the table
    query = "INSERT INTO users (name,username, password, plan, role, join_date) VALUES (?, ?, ?, ?, ?,?)"
    cur.execute(query, (name, username, password, plan, "user", join_date))
    # Commit the changes to the database
    conn.commit()
    # Close the database connection
    conn.close()
    # cursor.execute("INSERT INTO auth_data VALUES ({},{})".format(username,hashed_password))   
    return {"status": "User Registration Successful! Please login to continue..."}


# log data in db
def log_data(username, endpoint, call_status):
    # connect to db
    conn, cur = get_db("auth_data.db")
    # get joining time
    timestamp = datetime.now()
    # Execute the INSERT query to add the row to the table
    query = "INSERT INTO logs (username, timestamp, endpoint, call_status) VALUES (?, ?, ?, ?)"
    cur.execute(query, (username, timestamp, endpoint, call_status))
    # Commit the changes to the database
    conn.commit()
    # Close the database connection
    conn.close()
    return {"status": f"{username} logged in Successfully!"}


# Verify if user token is valid
def verify_token(username):
    if not check_username_taken(username):
        raise HTTPException(status_code=400, detail='Username is invalid')
    # connect to db
    conn, cur = get_db("auth_data.db")
    # get token of given username
    res = cur.execute(f"SELECT token FROM users WHERE users.username = '{username}'")
    token = res.fetchone()[0]
    # Close the database connection
    conn.close()
    # validate if token is correct
    if auth_handler.decode_token(token) == username:
        return True
    return False
