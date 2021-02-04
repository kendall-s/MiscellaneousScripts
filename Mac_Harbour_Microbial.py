""" Script to generate extremely accurate and high definition plot of microbial data in maquarie harbour """

import cartopy.crs as ccrs
from cartopy.io import shapereader
from cartopy import feature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
from PIL import Image
Image.MAX_IMAGE_PIXELS = 233280000 # Hack for high resolution image output
mpl.rc('font', family='Segoe UI')

SAVE_PATH = 'C:/Users/she384/Documents/checking_mac_harbour.png'
EXTENT_BOUNDS = [145.10, 145.60, -42.10, -42.50]

data = pd.read_csv(r'C:\Users\she384\Documents\Macquarie Harbour 2018-12 microbial samples contextual data v2.csv')

# High resolution coastline shape file - download here: http://www.soest.hawaii.edu/pwessel/gshhg/gshhg-shp-2.3.7.zip
# **NOTE** If using full file script will take a very long time to run - >5mins, use chopped down version of AUS area
#shp = shapereader.Reader('C:/Users/she384/Downloads/gshhg-shp-2.3.7/GSHHS_shp/f/GSHHS_f_L1.shp')

shp = shapereader.Reader(r'P:\Sherrin\Shape\High-res-aus\highres_aus.shp')


def make_map(projection=ccrs.PlateCarree()):
    fig, ax = plt.subplots(figsize=(15, 8), subplot_kw=dict(projection=projection))
    grid_lines = ax.gridlines(draw_labels=False, alpha=0.3, color='black',
                              xlocs=[145.1001, 145.20, 145.30, 145.40, 145.50, 145.59999],
                              ylocs=[-42.1001, -42.20, -42.30, -42.40, -42.49999])
    grid_lines.xlabels_top = grid_lines.ylabels_right = False
    grid_lines.xformatter = LONGITUDE_FORMATTER
    grid_lines.yformatter = LATITUDE_FORMATTER
    grid_lines.xlabel_style = {'size': 24}
    grid_lines.ylabel_style = {'size': 24}

    return fig, ax


fig, ax = make_map()
ax.set_extent(EXTENT_BOUNDS)

# Cheating way to add in ocean colour not using typical Cartopy API method
ax.background_patch.set_facecolor('#bde1f1')

# Draw the coastline polygon onto the map from the shape file
for record, geometry in zip(shp.records(), shp.geometries()):
    ax.add_geometries([geometry], ccrs.PlateCarree(), facecolor='#c4c8ce', edgecolor='black', lw=0.5)

# Dict for the marker styling and legend label
marker_styles = {'S':['o', 50, 'Surface'], 'P':['s', 75, 'Paravane']}

for x in ['P', 'S']:
    plt.scatter(data['Long'].loc[data['Layer']==x], data['Lat'].loc[data['Layer']==x],
                c=data['T'].loc[data['Layer']==x], marker=marker_styles[x][0], s=marker_styles[x][1],
                label=marker_styles[x][2], cmap='seismic', zorder=10)

cbar = plt.colorbar()
cbar.ax.tick_params(labelsize=16)
cbar.set_label(label='Temperature (C)', size=20)

legend = plt.legend(fontsize=15)

plt.savefig(SAVE_PATH, dpi=300)
