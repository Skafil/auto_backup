import os
import socket
import ssl
import sys
import backup
import database_manager

HOST = socket.gethostbyname(socket.gethostname()) # IPv4 address
PORT = 40445
BUFFER_SIZE = 4096
BYTEORDER_LENGTH = 8 # We don't need big buffer size to send size of file
FORMAT = "utf-8"
DATABASE_NAME = "users.db"

# These cert and key must be of the server
server_cert = os.path.join(os.getcwd(), "cert.pem")
server_key = os.path.join(os.getcwd(), "cert-key.pem")

# The context of ssl validation is to authenticate client because this is server side.
# Default context is most optimal option in case of efficiency and security. 
context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH, cafile=server_cert)

# Load digital certificate and private key to it, so they can be used.
context.load_cert_chain(certfile=server_cert, keyfile=server_key)


# Open socket object
# This socket called "s" is for accepting communication
# socket.AF_INET --> specify that we are using Internet address family for IPv4
# socket.SOCK_STREAM --> specify that we are using TCP protocol
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket with given address and port
s.bind((HOST, PORT))

# Allow server to accept connections. There is limit of 5 connections before we start reject them
s.listen(5)

while True:

    # Wait for connection with client to come in
    # This socket called "conn" is for communication with a client. Wrap it into SSL
    conn, addr = s.accept()
    sssl = context.wrap_socket(conn, server_side=True)
    print(f'Connected to {addr}')

    ### SEND ACK SIGNAL ###
    sssl.send("Connected to server".encode(FORMAT))

    ### RECEIVE OPTION ###
    option = sssl.recv(BUFFER_SIZE).decode(FORMAT)

    # If client didn't write the command correctly, just end connection.
    if option=="bad":
        print("The server doesn't know what client want to do. Check if the script was executed correctly from terminal.")
    
    # Otherwise...
    else:
        # Send request for username and password, then receive them
        sssl.send("Please enter your username and password.".encode(FORMAT))
        username = sssl.recv(BUFFER_SIZE).decode(FORMAT)
        password = sssl.recv(BUFFER_SIZE).decode(FORMAT)
        
        # Get path to user folder (existing or not)
        user_folder = os.path.join(os.getcwd(), username)

        # Create user account, by inserting his data into database and creating his folder
        if option == "create":
            database_manager.create_user(DATABASE_NAME, username, password)

        # Client want to retrive his backup.
        # Zip user folder and send it to client
        elif option == "retrive" and database_manager.check_user(DATABASE_NAME, username, password):
            # Full path to backup and just its name in format: "<username>_backup"
            backup_path, backup_name = backup.make_backup(user_folder)
            backup.send_backup(sssl, backup_path, backup_name, BYTEORDER_LENGTH, BUFFER_SIZE, FORMAT)
            
            # Remove backup zip
            os.remove(backup_path)

        # Client is sending backup, receive it and put into his folder
        elif option == "send" and database_manager.check_user(DATABASE_NAME, username, password):    
            backup.receive_backup(sssl, user_folder, BYTEORDER_LENGTH, BUFFER_SIZE, FORMAT, unpack=True)

    sssl.close()
    print(f"Connection with {addr} has ended.")
    

'''
Multithreading for multi connections -check tcp chat on youtube
Errors - username, path
Make scripts -
'''

### PROBLEMY
# 1) W konsoli nie moze byc widoczne jakie haslo jest wpisywanie
# 2) Haslo mozna przeslac niezakodowane dzieki ssl, ale w bazie danych przechowajmy je zakodowane jakims algorytmem + sol