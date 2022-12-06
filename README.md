The purpose of this project is to create a program that will automatically create a backup of files and folder in other locations.
Seperate users will have seperate backup folders. To access backup folder, the user will need IP address and ...

How it will be done:
    1. Search for folders & files.
    2. On the given, dynamic location create folder for particular user
    3. The backup file's name default will be the same name with date of modification added, but user can change it

LOCATION OF THE SOURCE AND BACKUP FILES
The potential locations of the source and backup files are 4:
    1) both source and backup files are in project directory,
    2) both source and backup files are in remote location,
    3) Source file is in project directory and backup file is in remote location,
    4) Source file is in remote location and backup file is in project directory.

There will be only one block of code to manage all of the cases.