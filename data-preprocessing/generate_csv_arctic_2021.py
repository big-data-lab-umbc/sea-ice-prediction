import sys
import time
start_time = time.time()
import pandas as pd
import numpy as np
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

##Average atmospheric variable data in the arctic (>60deg)
##Save data into CSV file
    
days=14610+365+366+243
### read sea ice extent data in the entire Arctic ###
df0=pd.read_csv('gsfc.nasateam.daily.extent.1978-2020.n',delim_whitespace=True)
df1=df0.iloc[34:,:]
arc=df1['TotalArc']
doy=df1['DOY']

sie=np.empty([days])
nn=0
for i in range(1979,2021):
    modd= i % 4
    if modd ==0:
        dd=366
    else:
        dd=365
    a1=np.where(df1.iloc[:,0]==i)
    b1=list(doy.iloc[a1])
    data1=arc.iloc[a1]
    for j in range(0,dd):
        if b1.count(j+1)==1:
            idx=b1.index(j+1)
            sie[nn+j]=data1.iloc[idx]
        else:
            if i==1979 and j==0:
                sie[nn+j]=df0.iloc[34,5]
            if i>1979 and j==0:
                sie[nn+j]=data1.iloc[0]
            if j>0:
                sie[nn+j]=data1.iloc[idx]
    nn=nn+dd
    
#sie[3288:3299]=sie[3287]

#Append SIE in 2021 from other data source
df2=pd.read_csv('N_seaice_extent_daily_v3.0.csv')

#Print this to cross-check the number of days in SIE
print('sie[14610+365+366:]',len(sie[14610+365+366:]))

#Print this to check the data samples in csv data file
print(len(df2.iloc[13758:,3]))

sie[14610+365+366:]=df2.iloc[13758:,3] 

sie[14610+365+366:]=sie[14610+365+366:]*(10**6) 

### read atmospehric data ###
atmo1=np.load('ERA5_daily_arctic_mean_atmo_60N_1979_2019.npy')
#print('atmo1',atmo1.shape)
atmo2=np.load('ERA5_daily_arctic_mean_atmo_60N_2020_2021.npy')
#print('atmo2',atmo2.shape)
atmo=np.concatenate((atmo1,atmo2),axis=0)
print('atmo',atmo.shape)
time_range=pd.date_range(start="1979-01-01",end="2021-08-31",freq='D')
print('time range',len(time_range))
thre=99999.0
fmt='%Y-%m-%d'
#removing sosaline from dict
# 'sosaline':atmo[:,6]
dict={'Date':time_range.strftime(fmt),'wind_10m':atmo[:,0],'specific_humidity':atmo[:,1],'LW_down':atmo[:,2],'SW_down':atmo[:,3],\
    'rainfall':atmo[:,4],'snowfall':atmo[:,5],'sst':atmo[:,7],'t2m':atmo[:,8],'surface_pressure':atmo[:,9],\
    'sea_ice_extent':sie}
data=pd.DataFrame(dict)

data.to_csv('Arctic_domain_mean_1979_2021.csv',header=True,index=False)

print("--- %s seconds ---" % (time.time() - start_time))

