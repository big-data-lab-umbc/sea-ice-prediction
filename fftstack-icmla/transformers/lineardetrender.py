import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from scipy import stats 

# Conditional linear detrending
class LinearDetrender:
    def __init__(self, p_thresh=None, trend_freq=None):
        self.p_thresh = p_thresh
        self.trend_freq = trend_freq
        self.models = None
        self.columns = None
        self.start_date = None
        self.should_fit = None
        self.results_ = None

    def get_feature_names_out(self, y=None):
        return self.columns

    def date_to_month_ordinal(self, date_series):
        year = self.start_date.year
        month = self.start_date.month
        month_ordinal = (date_series.year - year) * 12 + (date_series.month - month)
        return month_ordinal

    def fit(self, df, y=None):
        self.columns = df.columns
        self.start_date = df.index[0]

        self.models = pd.DataFrame()
        results = []
        for col in self.columns:
            x = np.arange(len(df)).reshape(-1, 1)
            y = df[col]
            model = LinearRegression()
            model.fit(x, y)

            if self.p_thresh!=None:
                if self.trend_freq!=None:
                    subsample = df.resample(self.trend_freq).mean()
                else:
                    subsample = df

                x_subsample = np.arange(len(subsample)).reshape(-1, 1)
                y_subsample = subsample[col]

                slope, intercept, r_value, p_value, std_err = stats.linregress(x_subsample.reshape(len(x_subsample)),
                                                                               np.array(y_subsample))

                if p_value<0.001:
                    rounded_p = "<0.001"
                elif p_value<=0.01:
                    rounded_p = round(p_value, 3)
                elif p_value>0.01:
                    rounded_p = round(p_value, 2)

                results.append([col, slope, intercept, r_value, p_value, rounded_p])
                if p_value < self.p_thresh:
                    self.models[col] = [model]
                else:
                    self.models[col] = [None]
            else:
                self.models[col] = [model]
        
        self.results_ = pd.DataFrame(results, columns=["variable", 
                                                       "slope", 
                                                       "intercept", 
                                                       "r_value", 
                                                       "p_value", 
                                                       "rounded_p"])

        return self

    def transform(self, df, y=None):
        detrended = pd.DataFrame(0, index=np.arange(len(df)), columns=df.columns)
        for col in df.columns:
            month_ordinal = self.date_to_month_ordinal(df.index)
            model = self.models[col][0]
            if model!=None:
                x = np.array(month_ordinal).reshape(-1, 1)
                detrended[col] = model.predict(x)
            else:
                detrended[col] = np.mean(df[col])
        return df - detrended.set_index(df.index)

    def fit_transform(self, df, y=None):
        self.fit(df)
        return self.transform(df)

    def inverse_transform(self, df_detrended, y=None):
        retrended = []
        for col in df_detrended.columns:
            x = np.array(self.date_to_month_ordinal(df_detrended.index)).reshape(-1, 1)
            y_detrended = df_detrended[col]
            model = self.models[col]
            original_column = y_detrended + model[0].predict(x)
            retrended.append(original_column)
        return pd.DataFrame(np.array(retrended).T, columns=df_detrended.columns).set_index(df_detrended.index)