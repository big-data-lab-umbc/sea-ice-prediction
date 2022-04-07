#calculate rainfall rate from total precipitation and snowfall rate
#by Yiyi Huang
#12/09/2020

import sys
import numpy as np
from netCDF4 import Dataset
from combine_era5_era5t import combine


##Note: Calculate 10-m wind velocity

#### read data ####
path='/umbc/xfs1/cybertrn/sea-ice-prediction/data/update_data_2020_2021/'
file0=path+'ERA5_daily_specific_humidity_900-1000_pressure_levels_2020_2021.nc'
df1=Dataset(file0,'r')
time=df1.variables['time'][:]
level=df1.variables['level'][:]
lon=(df1.variables['longitude'][:])
lat=(df1.variables['latitude'][:])
q=(df1.variables['q'][:])
fill=df1.variables['q'].missing_value
#q[np.where(q==fill)]=np.nan

time_size=time.size
lon_size=lon.size
lat_size=lat.size
level_size=level.size

a=combine()
q_4d=a.combine_era4d(q,fill)
q_4d[np.where(q_4d == fill)]=np.nan

new_data=np.empty([time_size,lat_size,lon_size])
new_data=np.nanmean(q_4d[:,:,:,:],axis=1)

#### write data to nc file ####
ncfile=Dataset('ERA5_daily_near_surface_humidity_25N_2020_2021_combined.nc',mode='w',format='NETCDF4')
time_dim = ncfile.createDimension('time', time_size)
lon_dim = ncfile.createDimension('lon', lon_size)
lat_dim = ncfile.createDimension('lat', lat_size)

time0 = ncfile.createVariable('time', np.float64, ('time',))
time0.units = 'hours since 1900-01-01 00:00:00.0'
time0.long_name = 'time'
time0.calendar = 'gregorian'
time0[:]=time

lon0 = ncfile.createVariable('lon', np.float32, ('lon',))
lon0.units = 'degree_east'
lon0.long_name = 'longitude'
lon0[:]=lon

lat0 = ncfile.createVariable('lat', np.float32, ('lat',))
lat0.units = 'degree_north'
lat0.long_name = 'latitude'
lat0[:]=lat

wind = ncfile.createVariable('specific_humidity',np.float64,('time','lat','lon'))
wind.units = 'kg kg**-1'
wind.missing_value = 'NaN'
wind.standard_name = 'Specific humidity' # this is a CF standard name
wind[:]=new_data

ncfile.close()

