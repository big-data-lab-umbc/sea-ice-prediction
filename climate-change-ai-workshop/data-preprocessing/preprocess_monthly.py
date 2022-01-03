#import packages
from tempfile import TemporaryFile

#load data

lstm_df = pd.read_csv('/.../Arctic_domain_mean_monthly_1979_2018.csv')
print(lstm_df.info())

#drop unwanted variables and retain important features
lstm_df = lstm_df.drop(['Date'],axis=1)

narray = np.array(lstm_df)
print(narray.shape)

#assign last column to target variable
target = narray[:,-1]

# convert an array of values into a dataset matrix
def reshape_features(dataset, timesteps=1):
    print(dataset.shape)
    X = dataset.reshape((int(dataset.shape[0]/timesteps)), timesteps, dataset.shape[1])
    return X
  
timesteps = 1
narray = reshape_features(narray, timesteps)

#Saving features and target in numpy

data = TemporaryFile()
np.save('/.../monthly_features.npy', narray)
np.save('/.../monthly_target.npy', target)
