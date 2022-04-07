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
file0=path+'ERA5_hourly_surface_LWdn_25N_ampm_2020_2021.nc'
df1=Dataset(file0,'r')
time=df1.variables['time'][:]
lon=(df1.variables['longitude'][:])
lat=(df1.variables['latitude'][:])
q_raw=(df1.variables['strd'][:])
fill=df1.variables['strd'].missing_value

file2=path+'ERA5_daily_2m_temp_25N_2020_2021.nc'
df2=Dataset(file2,'r')
time_era=df2.variables['time'][:]
time_size=time.size
lon_size=lon.size
lat_size=lat.size
ndays=time_era.size

q_raw1=q_raw[0:ndays*2,:,:,:]

a=combine()
q=a.combine_era(q_raw1,fill)

q[np.where(q == fill)]=np.nan
new_data=np.empty([ndays,lat_size,lon_size])
n=2
for i in range(0,lat.size):
	for j in range (0,lon.size):
		#q1=q[0:-1,i,j]
		q1=np.squeeze(q[:,i,j])
		new_data[0:,i,j]=np.nanmean(q1.reshape(-1,n), axis=1)
		#new_data[ndays-1,i,j]=q[-1,i,j]


scale=3600.0
new_data=new_data/scale



#### write data to nc file ####
ncfile=Dataset('ERA5_daily_LWdn_25N_2020_2021_combined.nc',mode='w',format='NETCDF4')
time_dim = ncfile.createDimension('time', ndays)
lon_dim = ncfile.createDimension('lon', lon_size)
lat_dim = ncfile.createDimension('lat', lat_size)

time0 = ncfile.createVariable('time', np.float64, ('time',))
time0.units = 'hours since 1900-01-01 00:00:00.0'
time0.long_name = 'time'
time0.calendar = 'gregorian'
time0[:]=time_era

lon0 = ncfile.createVariable('lon', np.float32, ('lon',))
lon0.units = 'degree_east'
lon0.long_name = 'longitude'
lon0[:]=lon

lat0 = ncfile.createVariable('lat', np.float32, ('lat',))
lat0.units = 'degree_north'
lat0.long_name = 'latitude'
lat0[:]=lat

wind = ncfile.createVariable('sfc_lwdn',np.float32,('time','lat','lon'))
wind.units = 'W m**-2'
wind.missing_value = 'NaN'
wind.standard_name = 'Surface downwelling longwave flux' # this is a CF standard name
wind[:]=new_data

ncfile.close()
