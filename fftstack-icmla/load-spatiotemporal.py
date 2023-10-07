from ast import Pass
from ftplib import FTP
import os
import numpy as np
from PIL import Image

def openImage(path):
    try: 
        return Image.open(path) 
    except IOError:
        return None

def buildDirectory(directory):
    directory_array = list(filter(None, (f"/{directory}").split("/")[1:]))
    for i in range(1, len(directory_array) + 1):
        try:
            os.mkdir("/".join(directory_array[0:i]))
        except FileExistsError:
            pass

def fileIndex(files, file):
    try:
        index = files.index(file)
        return index
    except:
        return -1

def loginFTP(ftp_directory, username, password):
    print("Logging in", end="\r")
    ftp = FTP(ftp_directory)
    ftp.login(username, password)
    return ftp

def quitFTP(ftp):
    ftp.quit()

def processData(ftp, fetch_directory, save_directory, **settings):
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
        buildDirectory(save_directory)

    cur_save_files = os.listdir(save_directory)
    for file in files:
        try:
            if (update):
                if (fileIndex(cur_save_files, file) != -1):
                    raise FileExistsError
            file.index(contains)
            print("Processing..." + file, end="\r")
            ftp.retrbinary("RETR " + file, open(save_directory + file, "wb").write)
            print(file[0:len(file)-4], end="\r")

        except:
            pass
    
ftp = loginFTP("sidads.colorado.edu", "anonymous", "anonymous")

source_url = "/DATASETS/NOAA/G02135/north/monthly/geotiff/"
img_dir = "spatiotemporal/data/sie-images/"

for month_num, month_name in enumerate(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]):
    processData(ftp,
                source_url + f"{(month_num + 1):02}_{month_name}/",
                img_dir,
                contains="extent",
                make_directory=True,
                update=True)

quitFTP(ftp)