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
- argparse

## MAKING A BACKUP

1) User has to give a **path to file or folder**.
2) Create **zip archive** in the source path and called it  
'folder/file name' + '_backup.zip' (using `shutil`)

## **SENDING THE BACKUP**

### CREATING CONNECTION
1) User has to give an **IP address** and **PORT** of the server.
2) The connection is wrapped into **SSL**, so the client has to give CA certifciate and the server - server certificate and server private key. (check `ABOUT_CERTS.md` for details).

### AUTHENTICATE USER
Many users can make backup on one server, so there need to be some kind of login system to choose correct user.

0) The login data are stored in **`database.csv`**. Password must be hashed.
1) Server ask for **username and password**, then check it in database.
2) If logged successfully, the program goes on, otherwise the connections is closed.

### SENDING BACKUP
1) Send **size** of backup zip to the server.
2) Send **name** of backup zip to the server.
3) Send **backup** zip to the server and place it into correct user folder, using his name given earlier during authentication.
4) Remove backup zip folder from client side.

## **RETRIEVING BACKUP**
The procedure for retrieving is pretty much the same as for sending backup.
1) In terminal user has to specify that he want to retrive backup and also give path, where the backup will be placed.
2) Server asks user for username and password.
3) If logged successfully, server sends zip the same way, like client to server (but doesn't remove zip on its side!).

## **CREATING ACCOUNT**
1) User gives username and password
2) Before sending, password is hashed. The function for hashing must be the same on both side of connection.
3) Data are addedd to database.


