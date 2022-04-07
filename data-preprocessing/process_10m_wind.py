#calculate 10-m wind velocity from u and v-component 10-m wind
#by Yiyi Huang
#12/08/2020

import sys
import numpy as np
from netCDF4 import Dataset
from combine_era5_era5t import combine


##Note: Calculate 10-m wind velocity

#### read data ####
path='/umbc/xfs1/cybertrn/sea-ice-prediction/data/update_data_2020_2021/'
file0=path+'ERA5_daily_10m_wind_25N_2020_2021.nc'
df1=Dataset(file0,'r')
time=df1.variables['time'][:]
lon=(df1.variables['longitude'][:])
lat=(df1.variables['latitude'][:])
u10m=np.array(df1.variables['u10'][:])
v10m=np.array(df1.variables['v10'][:])
fill=df1.variables['u10'].missing_value
time_size=time.size
lon_size=lon.size
lat_size=lat.size

a=combine()
#!!! Changes made by Y.Huang on March 18, 2022
#u10m_3d=a.combine_era(u10m,fill)
#v10m_3d=a.combine_era(v10m,fill)

#No need to combine ERA5 and ERA5T data
u10m_3d=u10m
v10m_3d=v10m
#!!! the end - March 18, 2022

new_data=np.empty([time_size,lat_size,lon_size])

#for i in range (0,time_size):
#    for j in range (0,lat_size):
#        for k in range (0,lon_size):
#            if u10m[i,j,k] != fill and v10m[i,j,k] != fill:
#                new_data[i,j,k]=np.sqrt(u10m[i,j,k]**2+v10m[i,j,k]**2)
#            else:
#                new_data[i,j,k]=-999.0

new_data=np.sqrt(u10m_3d**2+v10m_3d**2)
missing=np.where((u10m_3d == fill) | (v10m_3d == fill))
new_data[missing]=-999.0



#### write data to nc file ####
ncfile=Dataset('ERA5_daily_10m_wind_speed_25N_2020_2021_combined.nc',mode='w',format='NETCDF4')
time_dim = ncfile.createDimension('time', time_size)
lon_dim = ncfile.createDimension('lon', lon_size)
lat_dim = ncfile.createDimension('lat', lat_size)

time0 = ncfile.createVariable('time', np.float64, ('time',))
time0.units = 'hours since 1900-01-01 00:00:00.0'
time0.long_name = 'time'
time0.calendar='gregorian'
time0[:]=time

lon0 = ncfile.createVariable('lon', np.float32, ('lon',))
lon0.units = 'degree_east'
lon0.long_name = 'longitude'
lon0[:]=lon

lat0 = ncfile.createVariable('lat', np.float32, ('lat',))
lat0.units = 'degree_north'
lat0.long_name = 'latitude'
lat0[:]=lat

wind = ncfile.createVariable('wind_speed',np.float32,('time','lat','lon'))
wind.units = 'm/s'
wind.missing_value = -999.0
wind.standard_name = '10-m wind speed' # this is a CF standard name
wind[:]=new_data

ncfile.close()
