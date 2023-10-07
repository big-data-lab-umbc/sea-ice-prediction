import numpy as np
import pandas as pd
from scipy import stats
import scipy
import itertools
from sklearn.preprocessing import StandardScaler, MinMaxScaler

def temporal_split(data, val_percent=0.2):
    first_month = data.index.month[0]
    train_len = data.index.get_loc(data.iloc[data.index.month==first_month].iloc[int(len(data.iloc[data.index.month==first_month])*(1-val_percent))].name)
    train = data[:train_len]
    test = data[train_len:]
    return train, test

# FFTstack
class FFTTransformer:
    def __init__(self, train_size, iter_grid, threshold_grid, method="normalize", performance_threshold=0.1, weights=[1,1], verbose=False):
        self.train_size = train_size
        self.train_len = None

        self.weights = weights
        self.iter_grid = iter_grid
        self.threshold_grid = threshold_grid
        self.perform_thresh = performance_threshold
        self.method = method
        self.verbose = verbose

        self.scaler_ = None
        self.best_params = None
        self.train_ = None
        self.val_ = None
        self.final_ifft = None

        self.results_ = None

    def model_fft(self, arr, iter_num, threshold, method):
        ifft_net = np.zeros(len(arr), dtype="complex")
        fft_input = np.array(arr).astype(float)
        for i in range(iter_num):
            n = len(fft_input)
            fhat = np.fft.fft(fft_input, n)
            psd = fhat * np.conj(fhat) / n
            if (method=="standardize"):
                self.scaler_ = StandardScaler()
            elif (method=="normalize"):
                self.scaler_ = MinMaxScaler()
            std_PSD = self.scaler_.fit_transform(psd.astype(float).reshape(-1, 1))
            indices = abs(std_PSD) >= threshold
            fhat = indices.reshape(fhat.shape) * fhat
            arr_ifft = np.array(scipy.fft.ifft(fhat)).astype(float)
            ifft_net += arr_ifft
            fft_input -= arr_ifft
        return ifft_net.astype(float)

    def get_feature_names_out(self, y=None):
        return self.train_.columns

    def fit(self, data, y=None):
        self.train_, self.val_ = temporal_split(data, val_percent=0.2)
        results_grid_fft, self.best_params = [], []
        if self.verbose:
            print("Scanning search space...")
        for var_num, var in enumerate(data.columns):
            if self.verbose:
                print(var_num, end="\r")
            fft_input = self.train_[var]
            var_results = []
            for iter_, thresh_ in list(itertools.product(self.iter_grid, self.threshold_grid)):
                ifft_train = self.model_fft(fft_input, iter_num=iter_, method=self.method, threshold=thresh_)
                train_res, val_res = fft_input - ifft_train, self.val_[var] - ifft_train[:len(self.val_)]
                mad_train, mad_val = stats.median_abs_deviation(train_res), stats.median_abs_deviation(val_res)
                per_change = (mad_val-mad_train)/abs(mad_train)
                mad_avg = np.mean([mad_train, mad_val])
                if abs(per_change) < self.perform_thresh:
                    comb = mad_avg
                else:
                    comb = float("inf")
                var_results.append([iter_, thresh_, per_change, mad_avg, comb])

            cur_results = pd.DataFrame(var_results, columns=["iter", 
                                                             "thresh", 
                                                             "per_change", 
                                                             "mad_avg", 
                                                             "metric"])
            results_grid_fft.append(cur_results)
            self.best_params.append(cur_results.iloc[cur_results.metric.idxmin()])
        ifft_final_net, ifft_final_res = (pd.DataFrame(index=data.index) for i in range(2))
        results = []
        if self.verbose:
            print("Training best models...")
        for i, var in enumerate(data.columns):
            if self.verbose:
                print(i, end="\r")
            best_param = self.best_params[i]
            if best_param.per_change != float("inf"):
                ifft_final_net[var] = self.model_fft(self.train_[var].append(self.val_[var]),
                                                     iter_num=int(best_param.iter),
                                                     threshold=best_param.thresh,
                                                     method=self.method)
            else:
                ifft_final_net[var] = 0

            mad_res = stats.median_abs_deviation(self.train_[var].append(self.val_[var]) - ifft_final_net[var])
            mad_initial = stats.median_abs_deviation(self.train_[var].append(self.val_[var]))

            residual_per_of_initial = mad_res / mad_initial

            results.append([var, best_param.iter, best_param.thresh, best_param.per_change, best_param.mad_avg, best_param.metric, residual_per_of_initial])

            ifft_final_res[var] = data[var] - ifft_final_net[var]
        self.final_ifft = ifft_final_net
        self.results_ = pd.DataFrame(results, columns=["variable", 
                                                       "iter", 
                                                       "thresh", 
                                                       "per_change", 
                                                       "mad_avg", 
                                                       "metric", 
                                                       "res_percent_of_initial"])
        return self

    def transform(self, data, y=None):
        ifft_final_res = data - self.final_ifft[:len(data)].set_index(data.index)
        return ifft_final_res

    def fit_transform(self, data, y=None):
        self.fit(data)
        return self.transform(data)

    def inverse_transform(self, transformed_data, y=None):
        return self.final_ifft[:len(transformed_data)].set_index(transformed_data.index) + transformed_data