# The "auto backup" Project

This application creates backup in the form of zip archive and send it to the server. Application is designed for terminal.

## General description
Generally, user has 3 options - create backup, restore backup or create account to gain access to backup folder.

To create backup user has to give path to folder/file, so the zip of it can be created. Then the connection with SSL between user and a server is estabilished. Afterwards server asks user to give username and password. If it is corrected, then server gets size and name of zip first, and then zip itself. Finally the zip is redirected to user's folder. The zip on client side is removed.


## WHAT IS USED?

I'm using Python 3.8 with modules:
- os,
- socket and ssl,
- shutil,
- argparse, sys,
- hashlib, getpass,

## QUICK START
0) Use `python3 server.py` to run server.
1) Use `python3 client.py -c` to create account and folder for backup on the server.
2) Use `python3 client.py <path/to/source>` to create backup pointed by the path and send it to server.
3) To retrive backup use `python3 client.py <where to receive backup>`. 

## MAKING A BACKUP

1) User has to give a **path to file or folder**.
2) Create **zip archive** in the source p.ath and called it  
'folder/file name' + '_backup.zip' (using `shutil`)

## **CREATING ACCOUNT**
1) User gives username and password and they are sent unhashed, because ssl provide secure communication.
2) Server receive user data. Then the server create random salt using `os.urandom(32)` function and the key using `hashlib.pbkdf2_hmac()` function.
3) Username, salt and key are stored in database. All the operations goes by using **`sqlite3`** module.

## **SENDING THE BACKUP**

### CREATING CONNECTION
1) The socket is created automatically and the connection is from/to local server and the port 40445. You can change these settings on the top of `server.py` and `client.py`.
2) The connection is wrapped into **SSL**, so the client has to give CA certifciate and the server - server certificate and server private key. (check `ABOUT_CERTS.md` for details).

### AUTHENTICATE USER

0) Username, salt and key are stored in **`user.db`**.
1) Server ask for **username and password**, then check it in database.
2) Server compares two keys, if they are the same, then user is "log in" successfully.

### SENDING BACKUP
1) Send **size** of backup zip to the server.
2) Send **name** of backup zip to the server.
3) Send **backup** zip to the server and place it into correct user folder, using his name given earlier during authentication. The zip is unpacked.
4) Remove backup zip folder on client and server side.

## **RETRIEVING BACKUP**
The procedure for retrieving is pretty much the same as for sending backup.
1) In terminal user has to specify that he want to retrive backup and also give path, where the backup will be placed.
2) Server asks user for username and password.
3) If logged successfully, server sends zip the same way, like client to server (but doesn't remove zip on client side!).
