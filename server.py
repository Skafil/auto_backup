import os
import socket

message = "Polaczono z serwerem"
HOST = socket.gethostbyname(socket.gethostname()) # IPv4 address
PORT = 40444



# Open socket object
# This socket called "s" is for accepting communication
# socket.AF_INET --> specify that we are using Internet address family for IPv4
# socket.SOCK_STREAM --> specify that we are using TCP protocol
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket with given address and port
s.bind((HOST, PORT))

# Allow server to accept connections, there is limit of 5 connections before we start reject them
s.listen(5)

while True:

    # Wait for connection with client to come in
    # This socket called "conn" is for communication with a client
    conn, addr = s.accept()
    print(f'Connected to {addr}')
    print(conn)

    # Get data sended by client and decode them
    # Buffer size = 1024 bytes
    data = conn.recv(1024).decode()

    conn.send(message.encode("utf-8"))

    conn.close()
    print(f"Connection with {addr} has ended.")

'''Multithreading for multi connections
    check tcp chat on youtube'''