import sys
import pandas as pd
import numpy as np
from os import path
from netCDF4 import Dataset

#Goal: Read sea ice raw data in binary format and store it in netCDF file
#Update the data in 2020 and 2021
#By Yiyi Huang
#Created on July 14, 2021

#### Read lon/lat information
lat = np.fromfile('psn25lats_v3.dat', dtype=np.dtype('<i'))
lat=lat.reshape(448,304)
lat = lat/100000.0

lon = np.fromfile('psn25lons_v3.dat', dtype=np.dtype('<i'))
lon=lon.reshape(448,304)
lon = lon/100000.0

#### Read sea ice data
#Note: Update to 2021-08-31!!!!
time_range=pd.date_range(start="2020-01-01",end="2021-08-31",freq='D')
tot_steps=time_range.size-1
ice_data=np.empty([tot_steps,448,304])

fillvalue=-999.0
filepath='/umbc/xfs1/cybertrn/sea-ice-prediction/data/update_data_2020_2021_sea_ice/sea_ice_binary_data/'
for i in range(0,tot_steps):
    if time_range[i].year==2020:
        filename=filepath+'nt_'+time_range[i].strftime('%Y%m%d')+'_f17_v1.1_n.bin'
    else:
        filename=filepath+'nt_'+time_range[i].strftime('%Y%m%d')+'_f18_nrt_n.bin'
        
    if path.isfile(filename) == True:  #to determine whether the file exists
            with open(filename, 'rb') as fr:
                hdr = fr.read(300)
                ice = np.fromfile(fr, dtype=np.uint8)
                ice = ice.reshape(448,304)/2.5 #rescale the data
                ice[np.where(ice>100.0)] = fillvalue #remove non-sea ice values
                ice_data[i,:,:]=ice
    else:
                ice_data[i,:,:]=ice_data[i-1,:,:] #fill the gap in the data with the sea ice in the pervious day
                print('no file:'+filename)
                print(i)

#### write spatial data to nc file ####
xx=448 #x_dim
yy=304 #y_dim
ncfile=Dataset('NSIDC_sea_ice_concentration_daily_25km_filled_2020_2021.nc',mode='w',format='NETCDF4')
time_dim = ncfile.createDimension('time', tot_steps)
x_dim = ncfile.createDimension('x_dim', xx)
y_dim = ncfile.createDimension('y_dim', yy)

lon0 = ncfile.createVariable('lon', np.float32, ('x_dim','y_dim'))
lon0.units = 'degree_east'
lon0.long_name = 'longitude'
lon0[:]=lon

lat0 = ncfile.createVariable('lat', np.float32, ('x_dim','y_dim'))
lat0.units = 'degree_north'
lat0.long_name = 'latitude'
lat0[:]=lat

wind = ncfile.createVariable('sea_sic',np.float32,('time','x_dim','y_dim'))
wind.units = '%'
wind.missing_value = fillvalue
wind.standard_name = 'Sea ice concentration' # this is a CF standard name
wind[:]=ice_data

ncfile.close()

sys.exit()
            

