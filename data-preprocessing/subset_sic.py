#subset SIC above 25N
#provide sea ice prediction mask
#by Yiyi Huang
#12/09/2020

import sys
import numpy as np
from netCDF4 import Dataset

#### read data ####
path='/umbc/xfs1/cybertrn/sea-ice-prediction/data/'
file0=path+'NSIDC_sea_ice_concentration_daily_1deg_1979_2019.nc'
df1=Dataset(file0,'r')
time=df1.variables['time'][:]
lon2=np.array(df1.variables['lon'][:])
#lat2=np.array(df1.variables['lat'][:])
sic0=np.array(df1.variables['Sea_ice_concentration'][:])

lat2=np.linspace(-89.5,89.5,180)
time_size=time.size
lon_size=lon2.size
lat_size=lat2.size

sea_ice_mask=np.empty([lat_size,lon_size],dtype=int)
lat_idx=np.where(lat2 >= 24.5)
lat25=lat2[lat_idx]
sic1=sic0[:,lat_idx,:]
sic1=np.squeeze(sic1)

sea_ice_mask=np.empty([lat25.size,lon_size],dtype=int)
for i in range (0,lat25.size):
    for j in range (0,lon_size):
        a1=sic1[:,i,j]
        ct=a1[np.where(a1>0.0)].size
        if ct >= 1:
            sea_ice_mask[i,j]=1
        else:
            sea_ice_mask[i,j]=0


#### write data to nc file ####
days=time.size
ncfile=Dataset(path+'NSIDC_sea_ice_concentration_daily_1deg_25N_1979_2019.nc',mode='w',format='NETCDF4')
time_dim = ncfile.createDimension('time', days)
lat_dim = ncfile.createDimension('lat', lat25.size)     # latitude axis
lon_dim = ncfile.createDimension('lon', 360)    # longitude axis


lat = ncfile.createVariable('lat', np.float32, ('lat',))
lat.units = 'degrees_north'
lat.long_name = 'latitude'
lat[:]=lat25

lon = ncfile.createVariable('lon', np.float32, ('lon',))
lon.units = 'degrees_east'
lon.long_name = 'longitude'
lon[:]=lon2

date1=np.arange(days)
time = ncfile.createVariable('time', np.int, ('time'))
time.units = 'Days'
time.long_name = 'Days since 1979-01-01'
time[:]=date1

sic = ncfile.createVariable('Sea_ice_concentration',np.float64,('time','lat','lon'))
sic.units = '%'
sic.standard_name = 'NSIDC_sea_ice_concentration' # this is a CF standard name
sic[:]=np.array(sic1)

sic_mask = ncfile.createVariable('SIC_mask',np.float64,('lat','lon'))
sic_mask.units = ' '
sic_mask.long_name = 'NSIDC sea ice concentration mask: 1 for valid sea ice grid box; 0 for no sea ice all the time' # this is a CF standard name
sic_mask[:]=sea_ice_mask

ncfile.close()



