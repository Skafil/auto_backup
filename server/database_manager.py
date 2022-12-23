import sqlite3
import os
import hashlib

def get_key(pw, salt):
    
    key = hashlib.pbkdf2_hmac(
        'sha256',   # Hash algorithm name
        pw.encode('utf-8'),   # Password in bytes
        salt,
        100000, # number of iterationts, recommended at least 100 000 for SHA-256
        # Optional use dklen - len of key, default is 64
    )

    return key

def create_user(database_name, username, password):
    # Connect to database( create it if doesn't exist)
    db_path = os.path.join(os.getcwd(), database_name)
    database = sqlite3.connect(db_path)

    cursor = database.cursor()
    try:
        cursor.execute(""" CREATE TABLE users (
                user text,
                salt text,
                key text
        )""")
        database.commit()
    except:
        pass

    # Generate salt in bytes. The length should be at least 16.
    # This function doesn't use pseudo-random number generator = unpredictable.
    salt = os.urandom(32)
    key = get_key(password, salt)
    cursor.execute("INSERT INTO users (user, salt, key) VALUES (:name, :salt, :key)", {'name': username, 'salt': salt, 'key': key})

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
                salt text,
                key text
        )""")
    except:
        cursor.execute("SELECT salt, key FROM users WHERE user=:name", {'name': username})
        
        # Get all the result of executing above command
        results = cursor.fetchall()

        # If there are any users with given names
        if results != None:

            # Check every one of them...
            for data in results:

                # By getting their salt, creating key and comparing it with the one in database
                salt = data[0]
                key = get_key(password, salt)
                if key == data[1]:
                    # If the keys are the same, then the user exists and the password was correct
                    user_exists = True

    database.commit()
    database.close()

    return user_exists
