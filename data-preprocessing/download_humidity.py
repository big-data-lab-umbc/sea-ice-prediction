import cdsapi

c = cdsapi.Client()

c.retrieve(
    'reanalysis-era5-pressure-levels',
    {
        'product_type': 'reanalysis',
        'format': 'netcdf',
        'variable': 'specific_humidity',
        'pressure_level': [
            '900','925','950','975','1000',
        ],
        'year': [
            '2020', '2021',
        ],
        'month': [
            '01', '02', '03',
            '04', '05', '06',
            '07', '08', '09',
            '10', '11', '12',
        ],
        'day': [
            '01', '02', '03',
            '04', '05', '06',
            '07', '08', '09',
            '10', '11', '12',
            '13', '14', '15',
            '16', '17', '18',
            '19', '20', '21',
            '22', '23', '24',
            '25', '26', '27',
            '28', '29', '30',
            '31',
        ],
        'time': [
            '00:00',
        ],
        'area': [
            90, -180, 25,
            180,
        ],
	'grid':[1.0,1.0],
    },
    'ERA5_daily_specific_humidity_900-1000_pressure_levels_2020_2021.nc')
