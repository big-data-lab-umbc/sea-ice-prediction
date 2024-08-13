This document walks you through the data downloading and preprocessing steps for ERA5 reanalysis data and NSIDC observational data.

## Prerequisites:
1. To be able to download ERA5 data, you must first set up a CDS account and populate your .cdsapirc file. Follow the 'Install the CDS API key' instructions [here](https://cds.climate.copernicus.eu/api-how-to#install-the-cds-api-key).
2. To download sea_ice data using binaries, you need an account registration at [Earthdata](https://urs.earthdata.nasa.gov/users/new). 

## Steps:
The following code files provide a template to download and preprocess the data for 2020 - 2021. The provided code can be updated to download data for any period of time from 1979 till present.

**To download ERA5 data:**
1. run download_*.py

**Note:** You would need to import csdapi package to run download_*.py and update your PYTHONPATH system variable.

export PYTHONPATH="/.../lib/python3.7/site-packages:$PYTHONPATH"

**To download daily/monthly sea ice values:**
1. Go the NSIDC dataset repository through this [link](https://nsidc.org/data/G02135/versions/3).
2. Download N_seaice_extent_daily_v3.0.csv and remove rows from the end that lie outside the range of dates under consideration.
**Note:** Duplicate Feb 19 and Feb 22 to make up for Feb 20-21, 2021

**To download 25km sea_ice data using binaries:**
1. run nsidc-download_NSIDC-0081.001_2021_data.py. You would need to update ‘end_time’ in this file
2. run update_sea_ice_from_raw_data.py.
This should give you the up-to-date sea ice data in 25 km resolution.

**To preprocess the downloaded data:**
1. run process_*.py
2. run load_atmo_nc_data_2020_2021.py. You would need to update ‘days’ in this file to reflect the number of days the data corresponds to.

**To generate combined dataset:**
1. run nc_merged_data_numpy_25km_2021.py to generate npz version of 25km dataset. You would need to update the offset to reflect latest number of months

**To transform spatiotemporal data to time-series data:**
1. run generate_csv_arctic_2021.py (for daily data). You would need to update ‘days’ and ‘time_range’ -> ‘end’
2. run generate_csv_arctic_monthly_2021.py. You would need to update ‘mons’, ‘time_range’ and ‘time_range1’
 
**To download other tools such as land mask, etc:**
1. https://nsidc.org/data/polar-stereo/tools.html
2. https://nsidc.org/data/NSIDC-0051/versions/1
