from PIL import Image
import numpy as np
from numpy import savetxt
import os
import pandas as pd

def openImage(path):
    try: 
        return Image.open(path) 
    except IOError:
        return None

def build_directory(directory):
    directory_array = list(filter(None, (f"/{directory}").split("/")[1:]))
    for i in range(1, len(directory_array) + 1):
        try:
            os.mkdir("/".join(directory_array[0:i]))
        except FileExistsError:
            pass

img_dir = "spatiotemporal/data/sie-images/"
csv_dir = "spatiotemporal/data/sie-csv/"
build_directory(csv_dir)

for file in os.listdir(img_dir):
    img_file_name = img_dir + file
    cur_img = openImage(img_file_name).convert('1')
    cur_img.save(img_file_name)
    cur_img_array = np.asarray(cur_img).astype(int)
    csv_file_name = csv_dir + file[0:len(file)-4] + ".csv"
    np.savetxt(csv_file_name, 
           cur_img_array,
           delimiter =",",
           fmt ='% s')
    year, month = file[2:6], file[6:8]
    img_csv = list(np.loadtxt(csv_file_name, delimiter=",", dtype=int).reshape(1,136192)[0])
    print(file[0:len(file)-4], end="\r")
