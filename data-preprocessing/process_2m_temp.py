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
file0=path+'ERA5_daily_2m_temp_25N_2020_2021.nc'
df1=Dataset(file0,'r')
time=df1.variables['time'][:]
lon=(df1.variables['longitude'][:])
lat=(df1.variables['latitude'][:])
expver=df1.variables['expver'][:]
sst=np.array(df1.variables['t2m'][:])
fill=df1.variables['t2m'].missing_value
time_size=time.size
lon_size=lon.size
lat_size=lat.size

a=combine()
sst_3d=a.combine_era(sst,fill)

new_data=np.empty([time_size,lat_size,lon_size])

#for i in range (0,time_size):
#    for j in range (0,lat_size):
#        for k in range (0,lon_size):
#            if u10m[i,j,k] != fill and v10m[i,j,k] != fill:
#                new_data[i,j,k]=np.sqrt(u10m[i,j,k]**2+v10m[i,j,k]**2)
#            else:
#                new_data[i,j,k]=-999.0

missing=np.where(sst_3d == fill)
sst_3d[missing]=-999.0

#### write data to nc file ####
ncfile=Dataset('ERA5_daily_2m_temp_25N_2020_2021_combined.nc',mode='w',format='NETCDF4')
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

wind = ncfile.createVariable('t2m',np.float32,('time','lat','lon'))
wind.units = 'K'
wind.missing_value = -999.0
wind.standard_name = 'air temperature at 2m' # this is a CF standard name
wind[:]=sst_3d

ncfile.close()
