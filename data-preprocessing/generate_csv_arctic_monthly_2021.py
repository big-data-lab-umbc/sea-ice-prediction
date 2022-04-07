import sys
import time
start_time = time.time()
import pandas as pd
import numpy as np
#from geopy import distance
from netCDF4 import Dataset
import warnings
warnings.filterwarnings("ignore")
import datetime
from datetime import datetime

def arctic_weighted_mean(data,lat):
#input data is 2-dimensional
#calculate weighted average of data in the Arctic domain
    lon_mean=np.nanmean(data,axis=1) #average along longitude
    arc=lat[lat>60]
    arcrad=np.deg2rad(arc)
    weight=np.cos(arcrad)
    results=np.average(lon_mean[lat>60],weights=weight)
    return results

    
yrs=2020-1979+1
mons=yrs*12+8
print('total mons:',mons)
sie_mon=np.empty([mons])
### read sea ice monthly extent data in the entire Arctic ###
df0=pd.read_csv('gsfc.nasateam.month.extent.1978-2020.n',delim_whitespace=True)
df1=df0.iloc[2:,:]
arc=np.array(df1['TotalArc'])
sie_mon[0:107]=arc[0:107]
sie_mon[107]=arc[106] #missing 1987/12-replace by value in 1987/11
sie_mon[108:108+396]=arc[107:]

sie_mon[-6:]=[13480000,14390000,14640000,13840000,12660000,10710000] #2020 data-reads from other sources

### read atmospehric data ###
atmo1=np.load('ERA5_daily_arctic_mean_atmo_60N_1979_2019.npy')
atmo2=np.load('ERA5_daily_arctic_mean_atmo_60N_2020_2021.npy')
atmo=np.concatenate((atmo1,atmo2),axis=0)

### average daily data to monthly average data
time_range=pd.date_range(start="1979-01-01",end="2021-08-31",freq='D')
time_range1=pd.date_range(start="1979-01-01",end="2021-08-31",freq='M')

atmo_mon=np.empty([mons,10])

mon0=time_range.month
year0=time_range.year
for i in range(0,mons):
    mon1=time_range1[i].month
    year1=time_range1[i].year
    #average all days within a month
    time_idx=np.where((mon0==mon1) & (year0==year1))
    atmo_mon[i,:]=np.nanmean(atmo[time_idx,:],axis=1)


thre=99999.0
fmt='%Y-%m'
#removing sosaline
# 'sosaline':atmo_mon[:,6]
dict={'Date':time_range1.strftime(fmt),'wind_10m':atmo_mon[:,0],'specific_humidity':atmo_mon[:,1],'LW_down':atmo_mon[:,2],\
    'SW_down':atmo_mon[:,3],'rainfall':atmo_mon[:,4],'snowfall':atmo_mon[:,5],'sst':atmo_mon[:,7],'t2m':atmo_mon[:,8],\
    'surface_pressure':atmo_mon[:,9],'sea_ice_extent':sie_mon}
data=pd.DataFrame(dict)

data.to_csv('Arctic_domain_mean_monthly_1979_2021.csv',header=True,index=False)

print("--- %s seconds ---" % (time.time() - start_time))

