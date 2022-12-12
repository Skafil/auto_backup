import shutil
import os

def get_files_data(path):
    """Returns list containing objects with name, path and mtime of files"""
    data = []
    file_data = {}

    for dirpath, dirnames, filenames in os.walk(path):
            for file in filenames:
                file_path = os.path.join(dirpath, file)
                file_mtime = os.path.getmtime(file_path)

                file_data["name"] = file
                file_data["path"] = file_path
                file_data["mtime"] = file_mtime
                
                data.append(file_data)
    return data

def make_backup(source_path):
    """Walk through source dirs & files and make backup of them"""
    
    if os.path.exists(source_path) is False:
        os.mkdir(source_path)


    # for dirpath, dirnames, filenames in os.walk(source_path):
        
    #     # The path where files will be copied
    #     current_path = dirpath.replace(source_path, destination_path)
        
    #     # Create subdirectories
    #     for subdir in dirnames:
    #         try:
    #             os.mkdir(os.path.join(current_path, subdir))
    #         except FileExistsError:
    #             continue

    #     # Make a copy of files
    #     for file in filenames:
    #         file_path = os.path.join(dirpath, file) 
    #         shutil.copy2(file_path, current_path)
    zip_name = source_path.split("/")[-1] + "_backup"
    
    shutil.make_archive(zip_name, "zip", source_path)
    zip_path = os.path.join(os.getcwd(), zip_name+".zip")
    
    return zip_name, zip_path

    # shutil.unpack_archive(zip_path, destination_path, "zip")

                 
           
