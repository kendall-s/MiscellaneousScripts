"""
Use this script to replace phosphate results from the CSV into the respective NC file. Where in this case
the data in the NC file is incorrect but correct in the CSV file.

"""

import xarray as xr
import pandas as pd

PATH_TO_CSV = r"S:\Marine Technology and Equipment\Hydrochemistry\Hydrochemistry Current\Facilities\MNF\Data\in2019_v06\Hydro_Working_Data\Raw Data\csv\in2019_v06_leg1HydroDep_corrected for DO and PO4.csv"
PATH_TO_NCS = "C:/Users/she384/Documents/in2019_v06_Leg1_Deployments_NetCDF/new/updated for DO files"

NC_NAME_PREFIX = "in2019_v06_leg1Hydro"

csv_data = pd.read_csv(PATH_TO_CSV)

# Get all of the deployments

deployments_list = sorted(list(set(csv_data['Deployment'])))

for deployment in deployments_list:
    print(deployment)

    csv_phosphate = csv_data['Phosphate (uM)'].loc[csv_data['Deployment'] == deployment].values
    csv_rp = csv_data['RP'].loc[csv_data['Deployment'] == deployment].values
    print(csv_phosphate)
    print(csv_rp)

    nc_file = PATH_TO_NCS + '/' + NC_NAME_PREFIX + f"{deployment:03d}" + '.nc'
    nc_data = xr.open_dataset(nc_file)

    nc_rps = nc_data.rosettePosition[0, 0, :, 0][:].values
    print(nc_rps)
    try:
        nc_phosphate = nc_data.phosphate[0, 0, :, 0][:].values
        found = True
    except AttributeError:
        nc_phosphate = 0
        found = False
    print(nc_phosphate)

    if found:
        for i, x in enumerate(csv_phosphate):
            for l, y in enumerate(nc_phosphate):
                if csv_rp[i] == nc_rps[l]:
                    nc_phosphate[l] = csv_phosphate[i]
        print(nc_phosphate)
        nc_data.phosphate[0, 0, :, 0] = nc_phosphate
        print(nc_phosphate)

        nc_data.to_netcdf(path=nc_file, mode='a')
