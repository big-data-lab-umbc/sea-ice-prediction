import pandas as pd

url = "https://raw.githubusercontent.com/big-data-lab-umbc/sea-ice-prediction/main/data/Arctic_domain_mean_1979_2021.csv"
data_daily = pd.read_csv(url, index_col=0)
data_daily.index = pd.to_datetime(data_daily.index)

data_daily.to_csv("multivariate/data/arctic-domain-mean-daily.csv")
data_daily.resample("MS").mean().to_csv("multivariate/data/arctic-domain-mean-monthly.csv")
data_daily.resample("YS").mean().to_csv("multivariate/data/arctic-domain-mean-yearly.csv")