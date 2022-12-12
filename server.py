import os
import socket
import ssl
import json

message = "Polaczono z serwerem"
HOST = socket.gethostbyname(socket.gethostname()) # IPv4 address
PORT = 40444

# These cert and key must be of the server
server_cert = os.path.join(os.getcwd(), "certs_keys/cert.pem")
server_key = os.path.join(os.getcwd(), "certs_keys/cert-key.pem")

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
    # This socket called "conn" is for communication with a client
    conn, addr = s.accept()
    print(f'Connected to {addr}')

    # Wrap socket in SSL, so the connection will be secured
    sssl = context.wrap_socket(conn, server_side=True)

    print("Sending message...")
    sssl.send(message.encode("utf-8"))
    data = sssl.recv(1024).decode("utf-8")
    print(data)
    sssl.close()

    print(f"Connection with {addr} has ended.")

'''Multithreading for multi connections
    check tcp chat on youtube'''