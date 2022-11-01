
# MT-IceNet - A Spatial and Multi-Temporal Deep Learning Model for Arctic Sea Ice Forecasting

## Abstract
Arctic amplification has altered the climate patterns both regionally and globally, resulting in more frequent and more intense extreme weather events in the past few decades. The essential part of Arctic amplification is the unprecedented sea ice loss as demonstrated by satellite observations. Accurately forecasting Arctic sea ice from sub-seasonal to seasonal scales has been a major research question with fundamental challenges at play. In addition to physics-based Earth system models, researchers have been applying multiple statistical and machine learning models for sea ice forecasting. Looking at the potential of data-driven approaches to study sea ice variations, we propose MT-IceNet – a UNet-based spatial and multi-temporal (MT) deep learning model for forecasting Arctic sea ice concentration (SIC). The model uses an encoder-decoder architecture with skip connections and processes multi-temporal input streams to regenerate spatial maps at future timesteps. Using bi-monthly and monthly satellite retrieved sea ice data from NSIDC as well as atmospheric and oceanic variables from ERA5 reanalysis product during 1979-2021, we show that our proposed model provides promising predictive performance for per-pixel SIC forecasting with up to 60% decrease in prediction error for a lead time of 6 months as compared to its state-of-the-art counterparts.

## Paper
The paper has been accepted in the proceedings of [IEEE BDCAT 2022](https://bdcat-conference.org/). A copy of pre-print can be provided upon request.

## Code
In this repository, we have following folders:
1. Data Preprocessing 
2. Models 

## Dataset
The dataset is publicly available to download from AWS S3 instance: https://sahara-sic.s3.us-west-2.amazonaws.com/mt_icenet_data/

