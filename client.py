import socket
import os
import json
import backup

# In future the user will have to input these information
HOST = socket.gethostbyname(socket.gethostname()) # Also check on myip.is
PORT = 40444

src_path = os.path.join(os.getcwd(), "dane")

data = "Hejka"
#backup_path = backup.make_backup(src_path, dst_path)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

s.send(data.encode("utf-8"))
print(s.recv(1024).decode("utf-8"))
