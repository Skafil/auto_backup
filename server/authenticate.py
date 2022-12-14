import os
import csv

def authenticate_user(username, password, database, dst_path):
    user_exists = False

    with open(database, "r") as f:
        csvFile = csv.reader(f)

        for line in csvFile:
            if (line[0] == username) and (line[1] == password):
                if os.path.exists(dst_path) is False:
                    os.mkdir(dst_path)
                user_exists = True
        f.close()
    return user_exists        
                 


    