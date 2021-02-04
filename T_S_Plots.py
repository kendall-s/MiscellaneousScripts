""" Script for generating the T_S plots from the raw CTD files """

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

    plt.scatter(primary_salinity_subset_3, primary_temperature_subset_3, alpha=0.4, zorder=5, label=df.Station, s=5)

    #cb = plt.colorbar()
    #cb.set_label('Potential Density')
    #cb.set_alpha(1)
    #cb.draw_all()

x_lower, x_upper = plt.xlim()
y_lower, y_upper = plt.ylim()

dens_grid = np.zeros((125, 125))

x_grid = np.linspace(x_lower, x_upper, 125)
y_grid = np.linspace(y_lower, y_upper, 125)

for l, y in enumerate(y_grid):
    for i, x in enumerate(x_grid):
        dens_grid[l, i] = calc_pot_density(y, 0, x)

cs = plt.contour(x_grid, y_grid, dens_grid, linestyles='--', colors='black', linewidths=0.75, zorder=2)
plt.clabel(cs, fmt='%1.0f', inline=True, fontsize=6)

plt.legend()

plt.title('CTD 5, 9, 11, 12 T/S Combined')
plt.ylabel('T')
plt.xlabel('S')
plt.grid(alpha=0.3, zorder=0)
plt.savefig('C:/Users/she384/Documents/in2019_v05/Exploratory/Plots/combined.png', dpi=300)




