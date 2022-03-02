
#Regrid the sic data from 25*25 km to 1*1 degree using bilinear method
#Fill in missing values beteween 1979 and 1988
#by Yiyi Huang
#12/07/2020


import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import numpy as np
import xarray as xr
import xesmf as xe
import netCDF4
from netCDF4 import Dataset
import sys
import pandas as pd


#****** read original data
diri='data/'
file0 = diri+'NSIDC_sea_ice_concentration_daily_25km_filled_1979_2019.nc'

days=14975
londim=448
latdim=304

#dd1=np.empty([mon,latdim,londim])
yy=file0
data=Dataset(yy)
lat1=np.array(data.variables['lat'][:])
lon1=np.array(data.variables['lon'][:])
dd2=np.array(data.variables['sea_sic'][:][:][:])


for i in range (0,4000):
	data0=dd2[i,:,:]
	non=np.where(data0 != -999.0)
	count=data0[non].size
	if count == 0:
		j=i+1
		while count == 0:
			data1=dd2[j,:,:]
			non=np.where(data1 != -999.0)
			count=data0[non].size
			j=j+1
		dd2[i,:,:]=data1
		
missing=np.where(dd2 == -999.0)
dd2[missing]=np.nan

#****** check the original dataset 
plt.figure(figsize=(15,10));
ax = plt.axes(projection=ccrs.PlateCarree());
#ax.set_extent([-180, 180, 60, 90], crs=ccrs.PlateCarree());
ax.coastlines();
#data_crs = ccrs.PlateCarree();
plt.pcolormesh(lon1,lat1,dd2[1,:,:]);
plt.savefig('observation.png')



#****** regridding process
ds_out = xe.util.grid_global(1, 1) # the new grid is 1x1 degree
ds_out  # contains lat/lon values of cell centers and boundaries.

grid_in = {'lon': lon1,
           'lat': lat1
          }

regridder = xe.Regridder(grid_in, ds_out, 'bilinear')
dr_out = regridder(dd2)

lat2=np.linspace(-89.5,89.5,180)
lon2=np.linspace(-179.5,179.5,360)

#****** check the output dataset 
plt.figure(figsize=(15,10));
ax = plt.axes(projection=ccrs.NorthPolarStereo());
ax.set_extent([-180, 180, 60, 90], crs=ccrs.PlateCarree());
ax.coastlines();
data_crs = ccrs.PlateCarree();
ax.contourf(ds_out.lon,ds_out.lat,dr_out[1,:,:],transform=data_crs);
plt.savefig('NSIDC_Jan_bilinear.png')

plt.figure(figsize=(15,10));
ax = plt.axes(projection=ccrs.NorthPolarStereo());
ax.set_extent([-180, 180, 60, 90], crs=ccrs.PlateCarree());
ax.coastlines();
data_crs = ccrs.PlateCarree();
ax.contourf(ds_out.lon,ds_out.lat,dr_out[255,:,:],transform=data_crs);
plt.savefig('NSIDC_Sept_bilinear.png')

#******  write to nc file
### save data and write it to nc file ###
ncfile=Dataset(diri+'NSIDC_sea_ice_concentration_daily_1deg_bilinear_1979_2019.nc',mode='w',format='NETCDF4')
time_dim = ncfile.createDimension('time', days)
lat_dim = ncfile.createDimension('lat', 180)     # latitude axis
lon_dim = ncfile.createDimension('lon', 360)    # longitude axis
 

lat = ncfile.createVariable('lat', np.float32, ('lat',))
lat.units = 'degrees_north'
lat.long_name = 'latitude'
lat=lat2

lon = ncfile.createVariable('lon', np.float32, ('lon',))
lon.units = 'degrees_east'
lon.long_name = 'longitude'
lon=lon2

#date0=pd.date_range(start="1979-01-01",end="2019-12-31")
#date1=date0.strftime("%Y%m%d")
date1=np.arange(days)
time = ncfile.createVariable('time', np.int, ('time'))
time.units = 'Days'
time.long_name = 'Days since 1979-01-01'
time[:]=date1

sic = ncfile.createVariable('Sea_ice_concentration',np.float64,('time','lat','lon')) 
sic.units = '%' 
sic.standard_name = 'NSIDC_sea_ice_concentration' # this is a CF standard name
sic[:]=np.array(dr_out)

ncfile.close()

