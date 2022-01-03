import os
import math
import glob
import numpy as np
import pandas as pd

#load data
lstm_df = pd.read_csv('/.../Arctic_domain_mean_1979_2018.csv')

#Converting date columns to date type
lstm_df['Date'] = pd.to_datetime(lstm_df['Date'], format='%Y-%m-%d')

#Remove rows with 31st day
new_df = lstm_df[lstm_df['Date'].dt.day != 31]
new_df = new_df.reset_index(drop=True)
lstm_df = new_df

#Adding duplicate rows in February for leap and non-leap years
from datetime import datetime
 
narray = np.array(lstm_df)
for i in range(1979,2022):
  if (i%4==0): 
    len_index = np.where((narray[:,0] > datetime(i, 2, 28))&(narray[:,0] < datetime(i, 3, 1)))
    print('leap year index:',len_index[0])
    arr = narray[len_index[0]]
    print('leap year - before:',narray[len_index[0]+1])
    narray = np.insert(narray, len_index[0], arr, 0)
      #print(narray[len_index[0]])
    print('leap year - after:',narray[len_index[0]+1])

  else:
   len_index = np.where(narray[:,0] == datetime(i, 2, 28))
   print(len_index[0])
   arr = narray[len_index[0]]
   narray = np.insert(narray, len_index[0], arr, 0)
   narray = np.insert(narray, len_index[0], arr, 0)
  
#Remove date column
narray = np.delete(narray,0,1)

# convert an array of values into a dataset matrix
def reshape_features(dataset, timesteps=1):
    print(dataset.shape)
    X = dataset.reshape((int(dataset.shape[0]/timesteps)), timesteps, dataset.shape[1])
    return X
  
timesteps = 30
narray = reshape_features(narray, timesteps)
print(narray.shape)

#Saving features in numpy
np.save('/.../dailyt30_features.npy', narray)
