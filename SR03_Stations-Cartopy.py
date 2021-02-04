""" Projection matched map using Cartopy for the SR03 transect line showing stations """

import cartopy.crs as ccrs
from cartopy.io import shapereader
from cartopy import feature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import matplotlib.pyplot as plt
import matplotlib as mpl
from netCDF4 import Dataset
import numpy as np
import xarray as xr

import matplotlib.font_manager

import pandas as pd
from PIL import Image
Image.MAX_IMAGE_PIXELS = 233280000


from collections import OrderedDict

matplotlib.font_manager._rebuild()

mpl.rc('font', family='Source Sans Pro')

#df = pd.read_csv('C:/Users/she384/Documents/in2018_v01HydroDep.csv')

#shp = shapereader.Reader(r"C:\Users\she384\Downloads\gshhg-shp-2.3.7\GSHHS_shp\h\GSHHS_h_L1.shp")

shp = shapereader.Reader('C:/Users/she384/Documents/High-res-aus/highres_aus.shp')
antarctic_shp = shapereader.Reader(r"C:\Users\she384\Downloads\gshhg-shp-2.3.7\GSHHS_shp\f\GSHHS_f_L5.shp")

#extent = [-180, 180, 90, -90]
extent = [128, 152, -40, -70]

lat_lines = np.linspace(-40, -70, 5)
lon_lines = np.linspace(128, 152, 5)


def make_map(projection=ccrs.PlateCarree()):
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection=projection))
    grid_lines = ax.gridlines(draw_labels=False, alpha=0.2, color='black', linestyle='--', xlocs=lon_lines, ylocs=lat_lines)
    grid_lines.xlabels_top = grid_lines.ylabels_right = False
    grid_lines.xformatter = LONGITUDE_FORMATTER
    grid_lines.yformatter = LATITUDE_FORMATTER

    grid_lines.xlabel_style = {'size': 15}
    grid_lines.ylabel_style = {'size': 15}

    return fig, ax


fig, ax = make_map(projection=ccrs.PlateCarree())
ax.set_extent(extent)
#oc = feature.NaturalEarthFeature(category='physical', name='ocean', scale='10m', facecolor='#9dc2ed', zorder=-1)
#ax.add_feature(oc)

mapdata = Dataset('C:/Users/she384/Downloads/GEBCO_2014/GEBCO_2014_2D.nc')

lat_bounds = [-90, 0]
lon_bounds = [90, 180]

map_lat = mapdata.variables['lat'][:]
map_lon = mapdata.variables['lon'][:]

lat_low_ind = np.argmin(np.abs(map_lat - lat_bounds[0]))
lat_upp_ind = np.argmin(np.abs(map_lat - lat_bounds[1]))
to_plot_lat = mapdata.variables['lat'][lat_low_ind:lat_upp_ind]

lon_low_ind = np.argmin(np.abs(map_lon - lon_bounds[0]))
lon_upp_ind = np.argmin(np.abs(map_lon - lon_bounds[1]))
to_plot_lon = mapdata.variables['lon'][lon_low_ind:lon_upp_ind]

height = mapdata.variables['elevation'][lat_low_ind:lat_upp_ind, lon_low_ind:lon_upp_ind]

mainmap = ax.contour(to_plot_lon, to_plot_lat, height, vmax=5000, transform=ccrs.PlateCarree(), cmap='bone',
                    linewidths=0.3, levels=[-6000, -5000, -4000, -3000, -2000, -1000, -500], alpha=0.18)

#c4c8ce
for record, geometry in zip(shp.records(), shp.geometries()):
    ax.add_geometries([geometry], ccrs.PlateCarree(), facecolor='#6C7076', edgecolor='black', lw=0.5, zorder=3)

for record, geometry in zip(antarctic_shp.records(), antarctic_shp.geometries()):
    ax.add_geometries([geometry], ccrs.PlateCarree(), facecolor='#6C7076', edgecolor='black', lw=0.5, zorder=3)

ax.clabel(mainmap, [-6000, -5000, -4000, -3000, -2000, -1000, -500], fmt='%1.0f')

df2 = pd.read_csv('C:/Users/she384/Documents/SOTS Nutrient Variability Paper/Data/in2018_v07HydroDep.csv')
df = pd.read_csv('C:/Users/she384/Documents/Proposed_Stations.csv')
sr03 = pd.read_csv(r"S:\Marine Technology and Equipment\Hydrochemistry\Archive\Archive Jan 2020\Facilities\MNF\Data\in2018_v01 for datacentre\processed\in2018_v01_Hydro_Deployments_CSV\in2018_v01HydroDep.csv")
df3 = pd.read_csv('C:/Users/she384/Documents/Proposed_Stations2.csv')

ship_track = xr.open_dataset(r"C:\Users\she384\Documents\in2018_v01uwy.nc")
ship_lat = ship_track.latitude[:]
ship_lon = ship_track.longitude[:]

ax.plot(ship_lon, ship_lat, linestyle=":", lw=0.7, label='Ship Track', color='black', alpha=0.85)

#sots_site = plt.scatter(df2['Longitude'], df2['Latitude'], color='#37ce9c', label = 'SOTS Mooring Site', marker='*', s=600, edgecolors='#2ca37c', zorder=10)

stations = sorted(list(set(sr03['Deployment'])))

for x in stations:
    # C2BF14'
    plt.plot(sr03['Longitude'].loc[sr03['Deployment'] == x].iloc[0],
             sr03['Latitude'].loc[sr03['Deployment'] == x].iloc[0],
             ms=5, lw=0, marker='x', mfc='#f2f542', mec='#535353', label='CTD Station')

#plt.plot(df3['Longitude'], df3['Latitude'], ms=14, color='#000000', lw=0.75, linestyle='--')

#station_marks, =  plt.plot(df['Longitude'], df['Latitude'], ms=14, label='SR03 Station', mfc='#f2f542', mec='#dbd814', lw=0, marker='o')

#plt.legend(handles=[station_marks], fontsize=16, loc=4)

#for i, x in enumerate(df['Station']):
#    plt.annotate(x, (df['Longitude'].iloc[i] + 0.04, df['Latitude'].iloc[i] + 0.01), zorder=10)

#plt.annotate('940nm', xy=(144.5, -49.9), xytext=(145.5, -50.6), xycoords='data',
#            fontsize=12, ha='center', va='bottom', rotation=0,
#            bbox=dict(boxstyle='round', fc='white', alpha=0.7, edgecolor='#cfcfcf'),
#            arrowprops=dict(arrowstyle='-[, widthB=20.4, lengthB=0.2', lw=1))

station_31 = {'Longitude': 141.3344, 'Latitude': -54.5249}
station_56 = {'Longitude': 139.8539, 'Latitude': -65.3987}

plt.plot(station_31['Longitude'], station_31['Latitude'], ms=6, marker='o', mfc='#535353', mec='#535353')
plt.plot(station_56['Longitude'], station_56['Latitude'], ms=6, marker='o', mfc='#535353', mec='#535353')

lon_labels = list(np.around(lon_lines, 3))
lon_labels = [(str(x) + '°E') for x in lon_labels]

lat_labels = list(np.around(lat_lines, 3))
lat_labels = [(str(x) + '°S') for x in lat_labels]

ax.set_xticklabels(labels=lon_labels, fontsize=16)
ax.set_xticks(lon_lines)
ax.set_yticks(lat_lines)
ax.set_yticklabels(labels=lat_labels, fontsize=16)
ax.set_ylabel('Latitude', fontsize=17)
ax.set_xlabel('Longitude', fontsize=17)

ax.annotate('SR03', (141, -51), fontsize=19)
ax.annotate('S04', (131.1, -56.5), fontsize=19)
ax.annotate('P11S', (149, -61.6), fontsize=19)

ax.annotate('Station 31', (141.3344-3.7, -54.5247), fontsize=15.5)
ax.annotate('Station 56', (139.8526-3.7, -65.3991), fontsize=15.5)

ax.set_title('in2018_v01 Voyage Track and CTD Stations', fontsize=21)


handles, labels = ax.get_legend_handles_labels()
by_label = OrderedDict(zip(labels, handles))

plt.legend(by_label.values(), by_label.keys(), loc=2, fontsize=15)

plt.savefig('C:/Users/she384/Documents/sr3_map_bathy7.png', dpi=400)