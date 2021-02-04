"""Script used to generate the line plots of CTD sensor values"""

import matplotlib.pyplot as plt
import xarray as xr
import statistics
import numpy as np
from ConductivitytoSalinity import calc_salt
from PotentialTemperature import calc_pot_temp
from PotentialDensity import calc_pot_density
import os
import math
import matplotlib as mpl

mpl.style.use('seaborn-muted')
mpl.rc('font', family='Segoe UI Symbol')

fig, profile = plt.subplots()

for file in os.listdir(r'C:\Users\she384\Documents\in2019_v05\Exploratory\CTD\subset'):

    df = xr.open_dataset('C:/Users/she384/Documents/in2019_v05/Exploratory/CTD/subset/' + file)

    #df = xr.open_dataset('C:/Users/she384/Documents/in2019_v05/Exploratory/CTD/subset/in2019_v05005Ctd.nc')

    scan_rate = int(round(float(df.ScanRate), 0))
    num = 104088
    temp = df.sensorProcValue[:, 0].values

    multiple = math.floor(len(temp)/scan_rate)

    offset = len(temp) - (multiple*24)

    primary_temperature = df.sensorProcValue[offset:, 0].values
    secondary_temperature = df.sensorProcValue[offset:, 3].values

    primary_conductivity = df.sensorProcValue[offset:, 1].values
    secondary_conductivity = df.sensorProcValue[offset:, 4].values

    pressure = df.sensorProcValue[offset:, 2].values


    primary_temperature_subset = np.median(primary_temperature.reshape(-1, 24), axis=1)
    pressure_subset = np.median(pressure.reshape(-1, 24), axis=1)
    primary_conductivity_subset = np.median(primary_conductivity.reshape(-1, 24), axis=1)

    primary_salinity = calc_salt(primary_temperature_subset, primary_conductivity_subset, pressure_subset)

    #for x in pressure_subset:
    #    print(x)

    index_max = np.argmax(pressure_subset)
    print(index_max)

    primary_temperature_subset_2 = primary_temperature_subset[index_max:]
    primary_salinity_subset_2 = primary_salinity[index_max:]
    pressure_subset_2 = pressure_subset[index_max:]

    end_index_of_cast = np.where(abs(pressure_subset_2-15) <= 0.5)

    primary_temperature_subset_3 = primary_temperature_subset_2[:end_index_of_cast[0][0]]
    primary_salinity_subset_3 = primary_salinity_subset_2[:end_index_of_cast[0][0]]
    pressure_subset_3 = pressure_subset_2[:end_index_of_cast[0][0]]

    primary_potential_temperature = calc_pot_temp(primary_temperature_subset_3, pressure_subset_3)

    potential_density = calc_pot_density(primary_temperature_subset_3, 0, primary_salinity_subset_3)

    profile.plot(primary_salinity_subset_3, pressure_subset_3, lw=1, label=df.Station)

    profile.set_xlabel('Salinity (PSU)')
    profile.set_ylabel('Pressure (dbar)')
    #profile_2 = profile.twiny()
    #profile_2.set_xlabel('Temperature (degC)')
    #profile_2.plot(primary_temperature_subset_3, pressure_subset_3, lw=1, color='black')

plt.ylim(0, 1200)
profile.invert_yaxis()
plt.legend()
plt.grid(alpha=0.5, zorder=0)
#plt.show()
plt.savefig('C:/Users/she384/Documents/in2019_v05/Exploratory/Plots/ctd/' +'combined__temp_salt_profile.png', dpi=400)
profile.clear()
#profile_2.clear()