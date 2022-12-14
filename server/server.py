import os
import socket
import ssl
import authenticate

HOST = socket.gethostbyname(socket.gethostname()) # IPv4 address
PORT = 40444
BUFFER_SIZE = 4096
BYTEORDER_LENGTH = 8 # We don't need big buffer size to send size of file
FORMAT = "utf-8"
DATABASE_NAME = "database.csv"

# Get database path (and create it if it doesn't exist)
database = os.path.join(os.getcwd(), DATABASE_NAME)
if os.path.exists(database) is False:
    os.mkdir(database)

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
    
    ### RECEIVE USERNAME ###
    sssl.send("Please enter your username and password.".encode(FORMAT))
    
    username = sssl.recv(BUFFER_SIZE).decode(FORMAT)
    password = sssl.recv(BUFFER_SIZE).decode(FORMAT)

    destination_path = os.path.join(os.getcwd(), username)

    user_exists = authenticate.authenticate_user(username, password, database, destination_path)
    if user_exists is False:
        sssl.send("The username doesn't exit. Connection closed.".encode(FORMAT))
    else:
        ### RECEIVE BACKUP SIZE ###
        print("Receiving the backup size...")
        backup_size_in_bytes = sssl.recv(BYTEORDER_LENGTH)
        backup_size = int.from_bytes(backup_size_in_bytes, "big")
        print("The backup size is ", backup_size, "bytes")
        sssl.send("Backup size received!".encode(FORMAT))

        ### RECEIVE BACKUP NAME ###
        print("Receiving backup name...")
        backup_name = sssl.recv(BUFFER_SIZE).decode(FORMAT) + ".zip"
        user_backup = os.path.join(destination_path, backup_name)
        print("The backup name is ", backup_name)
        sssl.send("Backup name received".encode(FORMAT))

        ### RECEIVE BACKUP ###
        print("Receving backup...")
        # We are receiving binary data, so we use binary, not string.
        # The program will gradually adds chunks of backup to this variable until the whole backup will be received
        packet = b""

        # Until the whole backup isn't received
        while(len(packet) < backup_size):

            # if there is more to received than the buffer can contain, use whole size of buffer
            if (backup_size - len(packet)) > BUFFER_SIZE:
                received_data = sssl.recv(BUFFER_SIZE)
            # if it's not the case, adjust size of buffer
            else:
                received_data = sssl.recv(backup_size - len(packet))
                
            # Add this piece of data to packet
            packet += received_data

            # Finally write all the data from packet into zip
            with open(user_backup, "wb") as f:
                f.write(packet)            

            print("The backup was received")
            sssl.send("Backup received".encode(FORMAT))

    
    sssl.close()
    print(f"Connection with {addr} has ended.")
    

'''
Multithreading for multi connections -check tcp chat on youtube
Errors - username, path
Make scripts -
'''

