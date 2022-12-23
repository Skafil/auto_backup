import os
import socket
import ssl
import argparse
import sys
from getpass import getpass
import backup

# In future the user will have to input these information
HOST = socket.gethostbyname(socket.gethostname()) # Also check on myip.is
PORT = 40445
BUFFER_SIZE = 4096
BYTEORDER_LENGTH = 8 # We don't need big buffer size to send size of file
FORMAT = "utf-8"
src_path = ""   # This will be set by user in command prompt
# This must be cert of CA
ca_cert = os.path.join(os.getcwd(), "ca.pem")

"""
There are three options - 
    1. create and send backup to the server. (default)
    2. retrive backup from server.
    3. Create account.

In first option, user has to give only path.
In second option, user has to specify option -r and give path to where zip should be placed.
In third option user has to only specify option -c 
"""
parser = argparse.ArgumentParser(usage="client.py [-r] <path> OR client.py [-c] [-h]")
parser.add_argument('path', nargs="?", help="Give path of file/folder to make backup of it and send it to the server.")
parser.add_argument('-c', '--create', action="store_true", help="Create folder on the server only for your backup by creating account")
parser.add_argument('-r', '--retrive', nargs='?', type=str, help="Retrive backup from the server. Give path to where receive backup.")

args = parser.parse_args()


# The context is that we want to authenticate server, because this is a client side.
# Default context is most optimal option in case of efficiency and security. 
context = ssl.create_default_context()

# Load the CA certificate, that will be used to validate others peers' (someone with equal status in group) certificates.
context.load_verify_locations(ca_cert)

# Create socket and wrap it into SSL
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sssl = context.wrap_socket(s, server_hostname=HOST)

sssl.connect((HOST, PORT))

# cert = sssl.getpeercert()
# print("Cert: ", cert)



# Recive acknowledge signal from the server
ack_signal = sssl.recv(BUFFER_SIZE).decode(FORMAT)

if (ack_signal.lower() == "connected to server") :
    print(ack_signal) # Signal received and connection estabilished

    # Option will determinate later, what program should do    
    option = ""
    
    # Send "create" option to server to create account
    if args.create and (len(sys.argv) == 2):
        sssl.send("create".encode(FORMAT))
    
    # Send "retrive" option to server to retrive backup
    elif args.retrive and (len(sys.argv) == 3) and os.path.exists(sys.argv[2]):
        option = "retrive"
        src_path = sys.argv[2] # /home/skafil/auto_backup_project/client/dane

        sssl.send("retrive".encode(FORMAT))

    # Send "send" option to server to get server to know, that you will be sending backup
    elif (len(sys.argv) == 2) and (args.retrive == None) and (os.path.exists(sys.argv[1])):
        option = "send"
        src_path = sys.argv[1]
        sssl.send("send".encode(FORMAT))

    # If the command was typed something incorrectly in terminal, send "bad" option and close connection with server.
    else:
        print("Arguments passed in wrong way.\nusage:", parser.usage)
        sssl.send("bad".encode(FORMAT))
        sssl.close()
        sys.exit()

    # Receive request for username and password
    sssl.recv(BUFFER_SIZE).decode(FORMAT)

    ### Sending username  and password ###
    username = str(input("Enter username: "))
    password = str(getpass("Enter password: "))
    sssl.send(username.encode(FORMAT))
    sssl.send(password.encode(FORMAT))

    if option == "send":
        # Create backup zip, get its path and name
        backup_path, backup_name = backup.make_backup(src_path)

        # Send backup to the server with given parameters
        backup.send_backup(sssl, backup_path, backup_name, BYTEORDER_LENGTH, BUFFER_SIZE, FORMAT)

        # Remove backup zip
        os.remove(backup_path)

    elif option == "retrive":
        # Backup will be sended to the place from where the script was runned
        backup.receive_backup(sssl, os.getcwd(), BYTEORDER_LENGTH, BUFFER_SIZE, FORMAT)

    
    sssl.close()
    print("Connection closed")

### CHEAT SHEET HOW THE COMMUNICATION GOES IN CASE CLIENT SEND ZIP ###
# 1) server --> client  :   ACK signal
#
# 2) client --> server  :   Option chosen
#
# 3) server --> client  :   Request for user data
#
# 4) client --> server  :   Username and password
#
# 5) client --> server  :   name of zip
#    server --> client  :   confirmation
#
# 6) client --> server  :   size of zip
#    server --> client  :   confirmation
#
# 7) client --> server  :   zip
#    server --> client  :   confirmation