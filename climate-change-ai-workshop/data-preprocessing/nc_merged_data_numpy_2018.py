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


path='/.../sea-ice-prediction/data/'
save_path  = '/.../sea-ice-prediction/data/merged_data'

#### read data ####
file1=path+'ERA5_daily_surface_pressure_25N_1979_2019.nc'
file2=path+'ERA5_daily_10m_wind_speed_25N_1979_2019.nc'
file3=path+'ERA5_daily_near_surface_humidity_25N_1979_2019.nc'
file4=path+'ERA5_daily_2m_temp_25N_1979_2019.nc'
file5=path+'ERA5_daily_SWdn_25N_1979_2019.nc'
file6=path+'ERA5_daily_LWdn_25N_1979_2019.nc'
file7=path+'ERA5_daily_mean_rain_rate_25N_1979_2019.nc'
file8=path+'ERA5_daily_mean_snowfall_rate_25N_1979_2019.nc'
file9=path+'ERA5_daily_sea_surface_temp_25N_1979_2019.nc'
file10=path+'NSIDC_sea_ice_concentration_daily_1deg_25N_1979_2019.nc'
file11=path+'ORAS5_daily_sea_surface_salinity_25N_1979_2018.nc'



dataset = Dataset(file2,'r')

#time and geolocation:
time = np.array(dataset.variables['time'][:14610])
lat = np.array(dataset.variables['lat'][:])
lon = np.array(dataset.variables['lon'][:])

#variables
sp = np.array(Dataset(file1,'r').variables['sp'][:14610,:,:])
wind_speed = np.array(Dataset(file2,'r').variables['wind_speed'][:14610,:,:])
specific_humidity = np.array(Dataset(file3,'r').variables['specific_humidity'][:14610,:,:])
t2m = np.array(Dataset(file4,'r').variables['t2m'][:14610,:,:])
shortwave = np.array(Dataset(file5,'r').variables['sfc_lwdn'][:14610,:,:])
longwave = np.array(Dataset(file6,'r').variables['sfc_lwdn'][:14610,:,:])
rain_rate = np.array(Dataset(file7,'r').variables['rain_rate'][:14610,:,:])
snow_rate = np.array(Dataset(file8,'r').variables['snow_rate'][:14610,:,:])
sst = np.array(Dataset(file9,'r').variables['sst'][:14610,:,:])
sea_ice_mask = np.array(Dataset(file10,'r').variables['SIC_mask'][:14610])
sea_ice = np.array(Dataset(file10,'r').variables['Sea_ice_concentration'][:14610,:,:])
sosaline = np.array(Dataset(file11,'r').variables['sosaline'][:])

#Check missing values and replace them with average of 2 preceding and 2 succeeding timestamps        

#save file as numpy
test_data = TemporaryFile()
np.savez(save_path + '/' + '1979_2018_combined_data.npz', time = time, lat = lat, lon = lon, sp = sp, wind_speed = wind_speed, specific_humidity = specific_humidity,t2m = t2m, shortwave = shortwave, longwave = longwave, rain_rate = rain_rate, snow_rate = snow_rate, sst = sst, sea_ice_mask = sea_ice_mask, sea_ice = sea_ice, sosaline = sosaline)
_ = test_data.seek(0) 
