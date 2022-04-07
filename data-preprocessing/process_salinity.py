import sys
from netCDF4 import Dataset
import glob
import numpy as np

path='/umbc/xfs1/cybertrn/sea-ice-prediction/data/sea_surface_salinity/'
filename=glob.glob(path+'sosaline_ORAS5_1m_*.nc')
filename.sort()
n_file=len(filename)
year_idx=np.arange(2018-1979+1)+1979
tot_year=2018-1979+1
days=14975-365
data1=np.empty([days,180,360])
data2=np.empty([days,180,360])
month_idx=['01','02','03','04','05','06','07','08','09','10','11','12']
day30_idx=['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30']
day31_idx=['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31']
day28_idx=['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28']
day29_idx=['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29']

k=0
for i in range (0,tot_year):
	for mm in range (0,12):
		if (mm == 0 or mm == 2 or mm == 4 or mm == 6 or mm == 7 or mm == 9 or mm == 11):
        		dd=day31_idx
		if (mm == 3 or mm == 5 or mm == 8 or mm == 10):
       	 		dd=day30_idx

		modd=year_idx[i] % 4
		if mm == 1 :
        		if modd == 0 :
            			dd=day29_idx
        		else:
            			dd=day28_idx
		
		nday=len(dd)

		print(filename[i*12+mm])
		print(nday)
		df2=Dataset(filename[i*12+mm],'r')
		lon=np.array(df2.variables['lon'][:])
		lat=np.array(df2.variables['lat'][:])
		time=np.array(df2.variables['lat'][:])
		data=np.array(df2.variables['sosaline'][:])
		fill=df2.variables['sosaline'].missing_value
    
		data1[k:k+nday,:,:]=data
		k=k+nday

#subset 25N data
lat=lat+0.5
lon=lon-180.0
data2[:,:,0:179]=data1[:,:,181:360]
data2[:,:,181:360]=data1[:,:,0:179]
lat_idx=np.where(lat >= 25.0)
lat25=lat[lat_idx]
data3=data2[:,lat_idx,:]
data3=np.squeeze(data3)
#### write data to nc file ####
ncfile=Dataset('ORAS5_daily_sea_surface_salinity_25N_1979_2018.nc',mode='w',format='NETCDF4')
time_size=days
lon_size=360
lat_size=180
time_dim = ncfile.createDimension('time', time_size)
lon_dim = ncfile.createDimension('lon', lon.size)
lat_dim = ncfile.createDimension('lat', lat25.size)

date1=np.arange(days)
time = ncfile.createVariable('time', np.int, ('time'))
time.units = 'Days'
time.long_name = 'Days since 1979-01-01'
time[:]=date1

lon0 = ncfile.createVariable('lon', np.float32, ('lon',))
lon0.units = 'degree_east'
lon0.long_name = 'longitude'
lon0[:]=lon

lat0 = ncfile.createVariable('lat', np.float32, ('lat',))
lat0.units = 'degree_north'
lat0.long_name = 'latitude'
lat0[:]=lat25

wind = ncfile.createVariable('sosaline',np.float64,('time','lat','lon'))
wind.units = 'PSU'
wind.missing_value = fill
wind.standard_name = 'Sea surface salinity' # this is a CF standard name
wind[:]=data3

ncfile.close()
