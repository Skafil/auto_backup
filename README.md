# The "auto backup" Project

The project is about making a backup of given folder(s) or file(s) and sending them to the server, where will be stored and retrieved at any moment.  

## WHAT IS USED?

I'm using Python 3.8 with modules:
- os,
- socket and ssl,
- shutil

## MAKING A BACKUP

1) User has to give a **path to file or folder**.
2) Create **zip archive** in the source path and called it  
'folder/file name' + '_backup.zip' (using `shutil`)

## SENDING THE BACKUP
### CREATING CONNECTION
1) User has to give an **IP address** and **PORT** of the server.
2) The connection is wrapped into **SSL**, so the client has to give CA certifciate and the server - server certificate and server private key. (check certs_keys/ABOUT_CERTS.md for details).

### CONFIRMING USER
Many users can make backup on one server, so there need to be some kind of login system to choose correct user.

0) There must be some kind of **database**, that holds information about user.
1) Server ask for **username and password** (or some key, read more!).
2) After successed login, server gets path to user backup folder (the name of the folder is username). If there is none, create one.

### SENDING BACKUP
After everything is ready, it's time to send backup to server.
1) Send size of backup zip to the server.
2) Send name of backup zip to the server.
3) Send backup zip to the server and place it into correct user folder.
4) Remove backup zip folder from client side.

### RETRIEVING BACKUP
    The procedure for retrieving is pretty much the same as for sending backup. The only diffrence is that now the server send zip folder and the client unzip it.


