from ast import Pass
from ftplib import FTP
import os
import numpy as np

def build_directory(directory):
    directory_array = list(filter(None, (f"/{directory}").split("/")[1:]))
    for i in range(1, len(directory_array) + 1):
        try:
            os.mkdir("/".join(directory_array[0:i]))
        except FileExistsError:
            pass

def file_index(files, file):
    try:
        index = files.index(file)
        return index
    except:
        return -1

def login_ftp(ftp_directory, username, password):
    print("Logging in", end="\r")
    ftp = FTP(ftp_directory)
    ftp.login(username, password)
    return ftp

def quit_ftp(ftp):
    ftp.quit()

def process_data(ftp, fetch_directory, save_directory, **settings):
    contains, make_directory, update = (settings.get("contains", ""), 
                                        settings.get("make_directory", True), 
                                        settings.get("update", False))      
    
    print("Changing to "+ fetch_directory, end="\r")
    try:
        ftp.cwd(fetch_directory)
    except:
        print("Directory error", end="\r")

    files = ftp.nlst()
    files = files[2:]

    if (make_directory): 
        print("Building directory...", end="\r")
        build_directory(save_directory)

    cur_save_files = os.listdir(save_directory)
    for file in files:
        try:
            if (update):
                if (file_index(cur_save_files, file) != -1):
                    raise FileExistsError
            file.index(contains)
            print("Processing..." + file, end="\r")
            ftp.retrbinary("RETR " + file, open(save_directory + file, "wb").write)
            print(file[0:len(file)-4], end="\r")

        except:
            pass
    
ftp = login_ftp("sidads.colorado.edu", "anonymous", "anonymous")

source_url = "/DATASETS/NOAA/G02135/north/monthly/geotiff/"
img_dir = "spatiotemporal/data/sie-images2/"

for month_num, month_name in enumerate(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]):
    process_data(ftp,
                source_url + f"{(month_num + 1):02}_{month_name}/",
                img_dir,
                contains="extent",
                make_directory=True,
                update=True)

quit_ftp(ftp)