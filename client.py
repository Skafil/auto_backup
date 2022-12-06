import socket
import os

message = "hej"

HOST = socket.gethostbyname(socket.gethostname()) # Also chek on myip.is
PORT = 40444

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

s.send(message.encode("utf-8"))
print(s.recv(1024).decode("utf-8"))