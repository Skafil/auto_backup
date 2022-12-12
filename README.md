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
1) Send list of files and directories names to the server.
2) Send zip to the server (you have to make extra code READ MORE) and delete zip on the client side.
3) Server redirect zip to correct folder
4) Unzip the backup,
    - If the files has the same names, the files will be overridden by the new backup
    - If in the old backup there is no file/folder name on the list, that isn't in new backup, remove that file.

Alternative   
4) Take the name of zip folder, extract _backup.zip from it, use created name to check if there is existing folder. If so, then remove it completly and then unzip new backup. (This way we will create new backup files and in the same time create the ones, that no longer exist in source)

### RETRIEVING BACKUP
    The procedure for retrieving is pretty much the same as for sending backup. The only diffrence is that now the server send zip folder and the client unzip it.


