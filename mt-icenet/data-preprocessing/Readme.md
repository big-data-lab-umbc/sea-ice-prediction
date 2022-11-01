This document walks you through the data downloading and preprocessing steps for ERA5 reanalysis data and NSIDC observational data for the two models mt_icenet and sic_icenet. Some of the preprocessing steps overlap with our previous projects. For this, we have provided the link to those repositories to avoid duplication.

## Prerequisites:
1. To be able to download ERA5 data, you must first set up a CDS account and populate your .cdsapirc file. Follow the 'Install the CDS API key' instructions [here](https://cds.climate.copernicus.eu/api-how-to#install-the-cds-api-key).
2. To download sea_ice data using binaries, you need an account registration at [Earthdata](https://urs.earthdata.nasa.gov/users/new). 

## Combining ERA5 and NSIDC Data into one Spatiotemporal Dataset:
The following code files provide a template to download and preprocess the data for 1979 - 2021. The provided code can be updated to download data for any period of time from 1979 till present: https://github.com/big-data-lab-umbc/sea-ice-prediction/blob/main/data-preprocessing/Readme.md

## Preprocessing combined Spatiotemporal Dataset

Step 1: Create a rolling window dataset for monthly data. [Code](https://github.com/big-data-lab-umbc/big-data-reu/tree/main/2021-projects/team-1/preprocessing/convlstm)
Step 2: Create a rolling window dataset for bi-monthly data. [Code](https://github.com/big-data-lab-umbc/sea-ice-prediction/tree/main/mt-icenet/data-preprocessing)
