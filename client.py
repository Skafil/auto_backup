import socket
import os
import json
import backup
import ssl

# In future the user will have to input these information
HOST = socket.gethostbyname(socket.gethostname()) # Also check on myip.is
PORT = 40444
src_path = os.path.join(os.getcwd(), "dane")

# This must be cert of CA
ca_cert = os.path.join(os.getcwd(), "certs_keys/ca.pem")
data = "Hejka"
#backup_path = backup.make_backup(src_path, dst_path)


print("Host: ", HOST)

# The context is that we want to authenticate server, because this is a client side.
# Default context is most optimal option in case of efficiency and security. 
context = ssl.create_default_context()

# Load the CA certificate, that will be used to validate others peers' (someone with equal status in group) certificates.
context.load_verify_locations(ca_cert)

# Create socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Wrap socket in SSL, so the connection will be secured.
conn = context.wrap_socket(s, server_hostname=HOST)
print("Connection wrapped in ssl!")

conn.connect((HOST, PORT))
print("Connection made!")

# cert = conn.getpeercert()
# print("Cert: ", cert)

conn.send(data.encode("utf-8"))
message = conn.recv(1024).decode("utf-8")
print("Message from server: ", message)

conn.close()
print("Connection closed")
































# ssl_socket = ssl.wrap_socket(s, ssl_version=ssl.PROTOCOL_TLSv1, ciphers="ADH-AES256-SHA")

# ssl_socket.connect((HOST, PORT))


# ssl_socket.send(data.encode("utf-8"))
# print(ssl_socket.recv(1024).decode("utf-8"))
