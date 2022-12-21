import sqlite3
import os

def create_user(database_name, username, password):
    # Connect to database( create it if doesn't exist)
    db_path = os.path.join(os.getcwd(), database_name)
    database = sqlite3.connect(db_path)

    cursor = database.cursor()

    try:
        cursor.execute(""" CREATE TABLE users (
                user text,
                password text
        )""")
    except:
        cursor.execute("INSERT INTO users (user, password) VALUES (:name, :pass)", {'name': username, 'pass': password})

    database.commit()
    database.close()

    user_folder = os.path.join(os.getcwd(), username)
    os.mkdir(user_folder)

def check_user(database_name, username, password):
    user_exists = False

    # Connect to database( create it if doesn't exist)
    db_path = os.path.join(os.getcwd(), database_name)
    database = sqlite3.connect(db_path)

    cursor = database.cursor()

    # In case this is the very first command runned, create table
    try:
        cursor.execute(""" CREATE TABLE users (
                user text,
                password text
        )""")
    except:
        cursor.execute("SELECT * FROM users WHERE user=:name AND password=:pass", {'name': username, 'pass': password})
        
        data = cursor.fetchone()
        if data != None:
            user_exists = True
    database.commit()
    database.close()

    return user_exists
