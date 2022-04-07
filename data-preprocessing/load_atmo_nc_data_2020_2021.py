import sys
import time
start_time = time.time()
import pandas as pd
import numpy as np
#from geopy import distance
from netCDF4 import Dataset
import warnings
warnings.filterwarnings("ignore")

def arctic_weighted_mean(data,lat):
#input data is 2-dimensional
#calculate weighted average of data in the Arctic domain
    lon_mean=np.nanmean(data,axis=1) #average along longitude
    arc=lat[lat>60]
    arcrad=np.deg2rad(arc)
    weight=np.cos(arcrad)
    results=np.average(lon_mean[lat>60],weights=weight)
    return results
    
days=609

### read atmospehric data ###
file0='ERA5_daily_10m_wind_speed_25N_2020_2021_combined.nc'
df0=Dataset(file0,'r')
wind0=np.array(df0.variables['wind_speed'][:])
#fill=df0.variables['wind_speed'].missing_value
fill=-999.0
era_lon=np.array(df0.variables['lon'][:])
era_lat=np.array(df0.variables['lat'][:])
wind1=wind0[0:days] #m/s
wind1[np.where(wind1==fill)]=np.nan

nlat=era_lat.size
nlon=era_lon.size

file1='ERA5_daily_near_surface_humidity_25N_2020_2021_combined.nc'
df1=Dataset(file1,'r')
sh0=np.array(df1.variables['specific_humidity'][:]) #kg/kg
sh1=sh0[0:days]*1000.0 #to g/kg

file2='ERA5_daily_LWdn_25N_2020_2021_combined.nc'
df2=Dataset(file2,'r')
lwdn0=np.array(df2.variables['sfc_lwdn'][:]) #W m**-2
lwdn1=lwdn0[0:days]

file3='ERA5_daily_SWdn_25N_2020_2021_combined.nc'
df3=Dataset(file3,'r')
swdn0=np.array(df3.variables['sfc_lwdn'][:]) #W m**-2
swdn1=swdn0[0:days]

file4='ERA5_daily_mean_rain_rate_25N_2020_2021_combined.nc'
df4=Dataset(file4,'r')
rain0=np.array(df4.variables['rain_rate'][:]) #mm/day
rain1=rain0[0:days]

file5='ERA5_daily_snowfall_rate_25N_2020_2021_combined.nc'
df5=Dataset(file5,'r')
snow0=np.array(df5.variables['snow_rate'][:]) #mm/day
snow1=snow0[0:days]

#file6='ORAS5_daily_sea_surface_salinity_25N_1979_2018.nc'
#df6=Dataset(file6,'r')
#sosaline0=np.array(df6.variables['sosaline'][:]) #PSU
#sos_fill=df6.variables['sosaline'].missing_value
#sosaline1=sosaline0[0:days]
sosaline1=np.empty(snow1.shape)
sosaline1[:,:,:]=np.nan

file7='ERA5_daily_sea_surface_temp_25N_2020_2021_combined.nc'
df7=Dataset(file7,'r')
sst0=df7.variables['sst'][:] #K
era_fill=df7.variables['sst'].missing_value
sst1=np.array(sst0[0:days])
sst1[np.where(sst1==-999.0)]=np.nan


file8='ERA5_daily_2m_temp_25N_2020_2021_combined.nc'
df8=Dataset(file8,'r')
t2m0=df8.variables['t2m'][:] #K
t2m1=np.array(t2m0[0:days])
t2m1[np.where(t2m1==era_fill)]=np.nan

file9='ERA5_daily_surface_pressure_25N_2020_2021_combined.nc'
df9=Dataset(file9,'r')
sp0=df9.variables['sp'][:] #Pa
sp1=np.array(sp0[0:days])/100.0 # from Pa to hPa
sp1[np.where(sp1==era_fill)]=np.nan

data_mean=np.empty([days,10])
print('0')
data_mean[:,0] =  [arctic_weighted_mean(wind1[i,:,:],era_lat) for i in range(0,days)]
print('1')
data_mean[:,1] =  [arctic_weighted_mean(sh1[i,:,:],era_lat) for i in range(0,days)]
data_mean[:,2] =  [arctic_weighted_mean(lwdn1[i,:,:],era_lat) for i in range(0,days)]
data_mean[:,3] =  [arctic_weighted_mean(swdn1[i,:,:],era_lat) for i in range(0,days)]
print('4')
data_mean[:,4] =  [arctic_weighted_mean(rain1[i,:,:],era_lat) for i in range(0,days)]
data_mean[:,5] =  [arctic_weighted_mean(snow1[i,:,:],era_lat) for i in range(0,days)]
print('6')
data_mean[:,6] =  [arctic_weighted_mean(sosaline1[i,:,:],era_lat) for i in range(0,days)]
data_mean[:,7] =  [arctic_weighted_mean(sst1[i,:,:],era_lat) for i in range(0,days)]
data_mean[:,8] =  [arctic_weighted_mean(t2m1[i,:,:],era_lat) for i in range(0,days)]
print('9')
data_mean[:,9] =  [arctic_weighted_mean(sp1[i,:,:],era_lat) for i in range(0,days)]
print('data_mean shape:',data_mean.shape)
np.save('ERA5_daily_arctic_mean_atmo_60N_2020_2021',data_mean)


print("--- %s seconds ---" % (time.time() - start_time))

