import shutil
import os
import sys


def make_backup(source_path):
    # Source directs to folder/file that will be zipped

    try:
        # Format: <folder/file name>_backup"
        zip_name = source_path.split("/")[-1] + "_backup"
    
        shutil.make_archive(zip_name, "zip", source_path)
        zip_path = os.path.join(os.getcwd(), zip_name+".zip")
    
        return zip_path, zip_name

    except:
        print("Folder/File does not exist")
        sys.exit()

def send_backup(sock, backup_path, backup_name, BYTEORDER_LENGTH, BUFFER_SIZE, FORMAT):

    # SEND BACKUP SIZE
    backup_size = os.path.getsize(backup_path)
    backup_size_in_bytes = backup_size.to_bytes(BYTEORDER_LENGTH, "big")
    sock.send(backup_size_in_bytes)
    # print("Sending backup size: ", backup_size, " bytes")
    sock.recv(BUFFER_SIZE).decode(FORMAT)

    # SEND BACKUP NAME
    # print("Sending name of the backup: ", backup_name)
    sock.send(backup_name.encode(FORMAT))
    sock.recv(BUFFER_SIZE).decode(FORMAT)

    # SEND BACKUP
    # print("Sending backup...")
    with open(backup_path, "rb") as f:
        sock.send(f.read())
    
    sock.recv(BUFFER_SIZE).decode(FORMAT)

def receive_backup(sock, destination_path, BYTEORDER_LENGTH, BUFFER_SIZE, FORMAT, unpack=False):

     ### RECEIVE BACKUP SIZE ###
    # print("Receiving the backup size...")
    backup_size_in_bytes = sock.recv(BYTEORDER_LENGTH)
    backup_size = int.from_bytes(backup_size_in_bytes, "big")
    # print("The backup size is ", backup_size, "bytes")
    sock.send("Backup size received!".encode(FORMAT))

    ### RECEIVE BACKUP NAME ###
    # print("Receiving backup name...")
    backup_name = sock.recv(BUFFER_SIZE).decode(FORMAT) + ".zip"
    user_backup = os.path.join(destination_path, backup_name)
    # print("The backup name is ", backup_name)
    sock.send("Backup name received".encode(FORMAT))

    ### RECEIVE BACKUP ###
    # print("Receving backup...")
    # We are receiving binary data, so we use binary, not string.
    # The program will gradually adds chunks of backup to this variable until the whole backup will be received
    packet = b""

    # Until the whole backup isn't received
    while(len(packet) < backup_size):

        # if there is more to received than the buffer can contain, use whole size of buffer
        if (backup_size - len(packet)) > BUFFER_SIZE:
            received_data = sock.recv(BUFFER_SIZE)
        # if it's not the case, adjust size of buffer
        else:
            received_data = sock.recv(backup_size - len(packet))
                
            # Add this piece of data to packet
            packet += received_data

            # Finally write all the data from packet into zip
            with open(user_backup, "wb") as f:
                f.write(packet)            

            # print("The backup was received")
            sock.send("Backup received".encode(FORMAT))
            
    if unpack:
        backup_path = os.path.join(destination_path, backup_name)
        shutil.unpack_archive(backup_path, destination_path, "zip")