'''
This file takes sequential image data and applies a rolling window to the dataset to make it stateless.
The input data begins in shapes (384 months, 448x304 pixels, 5 features) for training data
and (96 months, 448x304 pixels, 5 features) for testing data.
The output data begins in shapes (384 months, 448x304 pixels, 1 feature) for training data
and (96 months, 448x304 pixels, 1 feature) for testing data
A rolling window is then applied to the input data, reshaping it into size (372 samples, 12 months each, 448x304 pixels, and 5 features) for training data
and size (96 samples, 12 months, 448x304 pixels, 5 feature) for testing data
Sample 1 of our input data contains months 1-12, sample 2 contains months 2-13, ..., and sample 372 contains months 372-384.
Output samples stay the same size, with one sample representing the prediction made for the month following the 12 months of input data in each sample  
'''

# import packages
import pandas as pd
import numpy as np
import tensorflow as tf

#load data
data = np.load('data/whole_data_biweekly_5f.npy',allow_pickle=True)
ice = data[:,:,:,-1]
# Fill North Pole Hole
ice[:, 208:260, 120:180][np.isnan(ice[:, 208:260, 120:180])] = 100.0

# replace ice maps in data
data[:, :, :, -1] = ice
print(data.shape)

n = 2 #no of instances in a month
# import data from numpy
X_train = data[:408*n,:,:,:]
X_test = data[408*n:,:,:,:]

# print data shapes
print(X_train.shape, X_test.shape)

# create sliding sequence for every 12 months to convert data into 5 dimensions
# sliding window code from : https://stackoverflow.com/questions/6811183/rolling-window-for-1d-arrays-in-numpy
def sliding_window(a, window, freq):
    shape = (a.shape[0] - window + 1, window) + a.shape[1:]
    strides = (a.strides[0], ) + a.strides
    rolled = np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides)
    return rolled[np.arange(0,shape[0],freq)]

#define amount of timesteps
timesteps = 24

# apply function to X train and test sets
X_train_convlstm_filled_seq = sliding_window(X_train, timesteps,2)
X_test_convlstm_filled_seq = sliding_window(X_test, timesteps,2)

#check data shape
print(X_train_convlstm_filled_seq.shape, X_test_convlstm_filled_seq.shape)

# Saving final arrays
np.save('X_train_convlstm_rolling_biweekly_5f.npy', X_train_convlstm_filled_seq)
np.save('X_test_convlstm_rolling_biweekly_5f.npy', X_test_convlstm_filled_seq)