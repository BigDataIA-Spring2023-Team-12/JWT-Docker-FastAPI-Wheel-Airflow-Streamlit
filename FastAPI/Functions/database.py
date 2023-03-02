import sqlite3
import pandas as pd
import os
from datetime import  datetime 
from Functions.auth import AuthHandler
from fastapi import FastAPI, Depends, HTTPException, Body, BackgroundTasks

# create table in the sqlite databae
# conn = sqlite3.connect("../auth_data.db")
# cursor = conn.cursor()
# cursor.execute("CREATE TABLE IF NOT EXISTS users (username TEXT ,name TEXT, password TEXT, token TEXT, tier INTEGER, role TEXT, join_date TEXT, PRIMARY KEY (username), FOREIGN KEY(username) REFERENCES logs(logs))")   
# cursor.execute("CREATE TABLE IF NOT EXISTS logs (username TEXT ,timestamp TEXT, endpoint TEXT, call_status INTEGER, PRIMARY KEY (username,timestamp))")   
 
auth_handler = AuthHandler()

def get_db(db):
    # eastablish connection with db
    db_path = os.getcwd() + "/database/{}".format(db)
    conn = sqlite3.connect(db_path,check_same_thread=False)
    cursor = conn.cursor()
    return conn, cursor

# get admin data
def admin_data():
    # conect to db
    conn, cur = get_db("auth_data.db")
    # get logs table
    df = pd.read_sql_query("SELECT * FROM logs", conn)
    log_json = df.to_json(orient='records', lines=True)
    # Close the database connection
    conn.close()
    return log_json

# get user data
def user_data(username):
    # conect to db
    conn, cur = get_db("auth_data.db")
    # get user data
    df = pd.read_sql_query(f"SELECT * FROM logs INNER JOIN users ON users.username = logs.username WHERE logs.username = '{username}'", conn)
    df = df.loc[:,~df.columns.duplicated()].copy()
    log_json = df.to_json(orient='records', lines=True)
    # Close the database connection
    conn.close()
    return log_json

# verify if admin
def verify_admin(username):
    # conect to db
    conn, cur = get_db("auth_data.db")
    # checks if username exists in table
    res = cur.execute(f"SELECT role FROM users WHERE users.username = '{username}'")
    check = res.fetchone()[0]
    # Close the database connection
    conn.close()

    if check != 'admin':
        return False
    else:
        return True

# check user in DB
def check_username_taken(username):
    # conect to db
    conn, cur = get_db("auth_data.db")
    # checks if username exists in table
    res = cur.execute(f"SELECT username FROM users WHERE users.username = '{username}'")
    check = res.fetchone()
    # Close the database connection
    conn.close()

    if check == None:
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
def update_password(username,password):
    # connect to db
    conn, cur = get_db("auth_data.db")
     # Execute the UPDATE query to update token the row to the table
    query = "UPDATE users SET password = '{0}' WHERE username = '{1}'".format(password,username)
    cur.execute(query)
    # Commit the changes to the database
    conn.commit()
    # Close the database connection
    conn.close()
    return {"status":f"{username} changed password successfully!"}


def login_user(token,username,ip):
    # connect to db
    conn, cur = get_db("auth_data.db")
     # Execute the UPDATE query to update token the row to the table
    query = "UPDATE users SET token = '{0}', ip_address = '{1}' WHERE username = '{2}'".format(token,ip,username)
    cur.execute(query)
    # Commit the changes to the database
    conn.commit()
    # Close the database connection
    conn.close()
    return {"status":f"{username} logged in Successfully!"}

# Register user & append user details in databas
def register_user(name,username,password,plan):
    # connect to DB
    conn, cur = get_db("auth_data.db")
    # get joining time
    join_date = datetime.now()
    # Execute the INSERT query to add the row to the table
    query = "INSERT INTO users (name,username, password, plan, role, join_date, calls_per_hour) VALUES (?, ?, ?, ?, ?,?,?)"
    cur.execute(query, (name,username, password,plan,"user",join_date,0))
    # Commit the changes to the database
    conn.commit()
    # Close the database connection
    conn.close()
    # cursor.execute("INSERT INTO auth_data VALUES ({},{})".format(username,hashed_password))   
    return {"status":"User Registration Successful! Please login to continue..." }

def reset_calls():
    # connect to DB
    conn, cur = get_db("auth_data.db")
    # Execute the UPDATE query to update token the row to the table
    query = "UPDATE users SET calls_per_hour = '0'"
    cur.execute(query)
    # Commit the changes to the database
    conn.commit()
    # Close the database connection
    conn.close()    

# check if call limit for user's plan exceeds
def verify_rate_limit(username):
    # connect to db
    conn, cur = get_db("auth_data.db")
    # get token of given username
    res = cur.execute(f"SELECT plan, calls_per_hour FROM users WHERE users.username = '{username}'")
    u_data = res.fetchone()
    plan = u_data[0]
    calls = u_data[1]
    # Commit the changes to the database
    conn.commit()
    # Close the database connection
    conn.close()
    if plan == "free":
        if calls >= 10:
            return False
        else:
            return True
    elif plan == "gold":
        if calls >= 15:
            return False
        else:
            return True
    elif plan == "platinum":
        if calls >= 20:
            return False
        else:
            return True
def call_counter(username):
    # connect to db
    conn, cur = get_db("auth_data.db")
     # get token of given username
    res = cur.execute(f"SELECT calls_per_hour FROM users WHERE users.username = '{username}'")
    calls = res.fetchone()[0]
    calls += 1
    # Execute the UPDATE query to update token the row to the table
    query = "UPDATE users SET calls_per_hour = '{0}' WHERE username = '{1}'".format(calls,username)
    cur.execute(query)
    # Commit the changes to the database
    conn.commit()
    # Close the database connection
    conn.close()

# log data in db
def log_data(username,endpoint,call_status):
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
    return {"status":f"{username} logged in Successfully!"}

# Verify if user token is valid
def verify_token(username,ip):
    if not check_username_taken(username):
        raise HTTPException(status_code=400, detail='Username is invalid')
    # connect to db
    conn, cur = get_db("auth_data.db")
    # get token and ip of given username
    res = cur.execute(f"SELECT token, ip_address FROM users WHERE users.username = '{username}'")
    u_data = res.fetchone()
    token = u_data[0]
    usr_ip = u_data[1]
    # Close the database connection
    conn.close()
    # validate if token is correct
    if auth_handler.decode_token(token) == username and usr_ip==ip:
        return True
    return False
        