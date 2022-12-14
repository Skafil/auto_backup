import shutil
import os

def make_backup(source_path):
    
    if os.path.exists(source_path) is False:
        os.mkdir(source_path)

    zip_name = source_path.split("/")[-1] + "_backup"
    
    shutil.make_archive(zip_name, "zip", source_path)
    zip_path = os.path.join(os.getcwd(), zip_name+".zip")
    
    return zip_name, zip_path
        