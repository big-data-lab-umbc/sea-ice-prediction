#Code Paths:
#/umbc/xfs1/cybertrn/sea-ice-prediction/data/nc_data_merge.py

import sys
import csv
import numpy as np
from pyhdf.SD import SD, SDC
import h5py
import glob
import pandas as pd
import numpy as np
import os
import datetime
from datetime import timedelta
from netCDF4 import Dataset
from numpy import linalg as LA
from math import *
from tempfile import TemporaryFile
import warnings


path='/umbc/xfs1/cybertrn/sea-ice-prediction/data/update_data_2020_2021/'
path1='/umbc/xfs1/cybertrn/sea-ice-prediction/data/update_data_2020_2021_sea_ice/'
save_path  = '/umbc/xfs1/cybertrn/sea-ice-prediction/data/merged_data'
#save_path  = '/umbc/rs/nasa-access/sea_ice/data/'

#### read data ####
file1=path+'ERA5_daily_surface_pressure_448x304_2020_2021.nc'
file2=path+'ERA5_daily_10m_wind_speed_448x304_2020_2021.nc'
file3=path+'ERA5_daily_near_surface_humidity_448x304_2020_2021.nc'
file4=path+'ERA5_daily_2m_temperature_448x304_2020_2021.nc'
file5=path+'ERA5_daily_SWdn_448x304_2020_2021.nc'
file6=path+'ERA5_daily_LWdn_448x304_2020_2021.nc'
file7=path+'ERA5_daily_mean_rain_rate_448x304_2020_2021.nc'
file8=path+'ERA5_daily_mean_snow_rate_448x304_2020_2021.nc'
file9=path+'ERA5_daily_sea_surface_temperature_448x304_2020_2021.nc'
file10=path1+'NSIDC_sea_ice_concentration_daily_25km_filled_2020_2021.nc'
#file11=path+'ORAS5_daily_sea_surface_salinity_448x304_2020_2021.nc'



dataset = Dataset(file2,'r')

#time and geolocation:
time = np.array(dataset.variables['time'][:609])
lat = np.array(dataset.variables['lat'][:])
lon = np.array(dataset.variables['lon'][:])

#read variables, check missing values and replace them with nans
sp = np.array(Dataset(file1,'r').variables['sp'][:609,:,:])
print(len(sp))
fill1=Dataset(file1,'r').variables['sp'].missing_value
sp[np.where(sp==fill1)]=np.nan

wind_speed = np.array(Dataset(file2,'r').variables['wind_speed'][:609,:,:])
fill2=Dataset(file2,'r').variables['wind_speed'].missing_value
wind_speed[np.where(wind_speed==fill2)]=np.nan

specific_humidity = np.array(Dataset(file3,'r').variables['specific_humidity'][:609,:,:])
fill3=Dataset(file3,'r').variables['specific_humidity'].missing_value
specific_humidity[np.where(specific_humidity==fill3)]=np.nan

t2m = np.array(Dataset(file4,'r').variables['t2m'][:609,:,:])
fill4=Dataset(file4,'r').variables['t2m'].missing_value
t2m[np.where(t2m==fill4)]=np.nan

shortwave = np.array(Dataset(file5,'r').variables['sfc_swdn'][:609,:,:])
fill5=Dataset(file5,'r').variables['sfc_swdn'].missing_value
shortwave[np.where(shortwave==fill5)]=np.nan

longwave = np.array(Dataset(file6,'r').variables['sfc_lwdn'][:609,:,:])
fill6=Dataset(file6,'r').variables['sfc_lwdn'].missing_value
longwave[np.where(longwave==fill6)]=np.nan

rain_rate = np.array(Dataset(file7,'r').variables['rain_rate'][:609,:,:])
fill7=Dataset(file7,'r').variables['rain_rate'].missing_value
rain_rate[np.where(rain_rate==fill7)]=np.nan

snow_rate = np.array(Dataset(file8,'r').variables['snow_rate'][:609,:,:])
fill8=Dataset(file8,'r').variables['snow_rate'].missing_value
snow_rate[np.where(snow_rate==fill8)]=np.nan

sst = np.array(Dataset(file9,'r').variables['sst'][:609,:,:])
fill9=Dataset(file9,'r').variables['sst'].missing_value
sst[np.where(sst==fill9)]=np.nan


sea_ice = np.array(Dataset(file10,'r').variables['sea_sic'][:609,:,:])
fill10=Dataset(file10,'r').variables['sea_sic'].missing_value
sea_ice[np.where(sea_ice==fill10)]=np.nan

#sosaline = np.array(Dataset(file11,'r').variables['sosaline'][:])
#fill11=Dataset(file11,'r').variables['sosaline'].missing_value
#sosaline[np.where(sosaline==fill11)]=np.nan
      
#save file as numpy
test_data = TemporaryFile()
np.savez(save_path + '/' + '2020_2021_combined_data_25km.npz', time = time, lat = lat, lon = lon, sp = sp, wind_speed = wind_speed, specific_humidity = specific_humidity,t2m = t2m, shortwave = shortwave, longwave = longwave, rain_rate = rain_rate, snow_rate = snow_rate, sst = sst, sea_ice = sea_ice)
_ = test_data.seek(0) 
