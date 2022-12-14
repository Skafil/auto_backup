import os
import socket
import ssl
import backup

# In future the user will have to input these information
HOST = socket.gethostbyname(socket.gethostname()) # Also check on myip.is
PORT = 40444
BUFFER_SIZE = 4096
BYTEORDER_LENGTH = 8 # We don't need big buffer size to send size of file
FORMAT = "utf-8"
src_path = os.path.join(os.getcwd(), "dane")

# This must be cert of CA
ca_cert = os.path.join(os.getcwd(), "ca.pem")
data = "Hejka"

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

ack_signal = sssl.recv(BUFFER_SIZE).decode(FORMAT)
if (ack_signal.lower() == "connected to server") :
    print("ACK signal received, ", ack_signal)

    ### Sending username  and password ###
    sssl.recv(BUFFER_SIZE).decode(FORMAT)

    username = str(input("Enter username: "))
    password = str(input("Enter password: "))
    
    sssl.send(username.encode(FORMAT))
    sssl.send(password.encode(FORMAT))

    # Create backup zip, get path to it and its name
    backup_name, backup_path = backup.make_backup(src_path)

    print("Sending size of backup in bytes to the server...")
    backup_size = os.path.getsize(backup_path)
    backup_size_in_bytes = backup_size.to_bytes(BYTEORDER_LENGTH, "big")
    sssl.send(backup_size_in_bytes)
    print("Sending backup size: ", backup_size, " bytes")
    sssl.recv(BUFFER_SIZE).decode(FORMAT)

    print("Sending name of the backup: ", backup_name)
    sssl.send(backup_name.encode(FORMAT))
    sssl.recv(BUFFER_SIZE).decode(FORMAT)

    print("Sending backup...")
    with open(backup_path, "rb") as f:
        sssl.send(f.read())
    
    sssl.recv(BUFFER_SIZE).decode(FORMAT)


    sssl.close()
    print("Connection closed")

    # Remove backup zip from client side
    os.remove(backup_path)
































# ssl_socket = ssl.wrap_socket(s, ssl_version=ssl.PROTOCOL_TLSv1, ciphers="ADH-AES256-SHA")

# ssl_socket.connect((HOST, PORT))


# ssl_socket.send(data.encode("utf-8"))
# print(ssl_socket.recv(1024).decode("utf-8"))
