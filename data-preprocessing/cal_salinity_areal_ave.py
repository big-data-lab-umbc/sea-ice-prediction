import sys
import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
#import cartopy.crs as ccrs
#import cartopy
#from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
#import matplotlib.ticker as mticker
from netCDF4 import Dataset
#from geopy import distance
import warnings
warnings.filterwarnings("ignore")

def regional_mean(data1,mask1,lat1,regs1):
    results=np.empty(regs1)
    for i in range(0,regs1):
        dd=data1[mask1==i+2] #region 2-10
        arc=lat1[mask1==i+2]
        arcrad=np.deg2rad(arc)
        weight=np.cos(arcrad)
        dd1=dd[np.where(dd!=era_fill)]
        weight1=weight[np.where(dd!=era_fill)]
        results[i]=np.average(dd1,weights=weight1)
    return results
    

### variables: Sea surface salinity
### Tranform ERA data (1deg) to NSIDC polar projection (448x304)
### Calculate atmospheric variables in different sub-regions
### Save spatial data to netCDF file
### created by Yiyi Huang
### Created on Feb.15, 2021
    

### read data ###
with open("region_n.msk", "rb") as fr:
    hdr = fr.read(300)
    mask = np.fromfile(fr, dtype=np.uint8)
    mask=mask.reshape(448,304)
        
lat = np.fromfile('psn25lats_v3.dat', dtype=np.dtype('<i'))
lat=lat.reshape(448,304)
lat = lat/100000.0

lon = np.fromfile('psn25lons_v3.dat', dtype=np.dtype('<i'))
lon=lon.reshape(448,304)
lon = lon/100000.0

area = np.fromfile('psn25area_v3.dat', dtype=np.dtype('<i'))
area=area.reshape(448,304)
area = area/1000.0

loc_for=np.load('Convert_ERA_to_NSIDC_mask.npy')

### read atmospehric data ###
days=14610
file0='ORAS5_daily_sea_surface_salinity_25N_1979_2018.nc'
df0=Dataset(file0,'r')
sh0=np.array(df0.variables['sosaline'][:]) #kg/kg
era_lon=np.array(df0.variables['lon'][:])
era_lat=np.array(df0.variables['lat'][:])
sh1=sh0[0:days]
time=np.array(df0.variables['time'][:])
time1=time[0:days]
era_fill=df0.variables['sosaline'].missing_value

nlat=era_lat.size
nlon=era_lon.size
        
### build ERA data based on NSIDC mask ###
data=np.empty([days,448,304])
for i in range(0,448):
    for j in range(0,304):
        idx=loc_for[i,j,0]
        idy=loc_for[i,j,1]
        data[:,i,j]=sh1[:,idx,idy]
        
        
### calculate regional mean based on NSIDC mask ###
regs=9
data_mean=np.empty([days,regs])

data_mean[:,:] = [regional_mean(data[i,:,:],mask,lat,regs) for i in range(0,days)]

np.save('Arctic_regional_mean_salinity',data_mean)

#### write spatial data to nc file ####
fill=-999.0
data[np.where(data==era_fill)]=fill
ncfile=Dataset('ORAS5_daily_sea_surface_salinity_448x304_1979_2018.nc',mode='w',format='NETCDF4')
time_dim = ncfile.createDimension('time', days)
x_dim = ncfile.createDimension('x_dim', 448)
y_dim = ncfile.createDimension('y_dim', 304)

time0 = ncfile.createVariable('time', np.float64, ('time',))
time0.units = 'seconds since 1970-01-01'
time0.long_name = 'MOSAiC time'
time0[:]=time1

lon0 = ncfile.createVariable('lon', np.float32, ('x_dim','y_dim'))
lon0.units = 'degree_east'
lon0.long_name = 'longitude'
lon0[:]=lon

lat0 = ncfile.createVariable('lat', np.float32, ('x_dim','y_dim'))
lat0.units = 'degree_north'
lat0.long_name = 'latitude'
lat0[:]=lat

wind = ncfile.createVariable('sosaline',np.float32,('time','x_dim','y_dim'))
wind.units = 'PSU'
wind.missing_value = fill
wind.standard_name = 'Sea surface salinity' # this is a CF standard name
wind[:]=data

ncfile.close()

sys.exit()
        
            




