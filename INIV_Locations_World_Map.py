import cartopy.crs as ccrs
from cartopy.io import shapereader
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from matplotlib.ticker import MaxNLocator
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.image import imread
import pandas as pd
import warnings
from PIL import Image
Image.MAX_IMAGE_PIXELS = 233280000

mpl.rc('font', family='Calibri')  # Cast Segoe UI font onto all plot text


df = pd.read_csv(r"C:\Users\she384\Documents\participants.csv")

shp = shapereader.Reader('C:/Users/she384/Downloads/gshhg-shp-2.3.7/GSHHS_shp/i/GSHHS_i_L1.shp')

def make_map(projection=ccrs.PlateCarree()):
    fig, ax = plt.subplots(figsize=(16,14), subplot_kw=dict(projection=projection))
    grid_lines = ax.gridlines(draw_labels=False, alpha=0.2, color='black')
    grid_lines.xlabels_top = grid_lines.ylabels_right = False
    grid_lines.xformatter = LONGITUDE_FORMATTER
    grid_lines.yformatter = LATITUDE_FORMATTER
    grid_lines.xlabel_style = {'size': 24}
    grid_lines.ylabel_style = {'size': 24}

    return fig, ax

fig, ax = make_map(projection=ccrs.PlateCarree())


ax.imshow(imread('C:/Users/she384/Downloads/HYP_HR_SR_OB_DR/HYP_HR_SR_OB_DR/HYP_HR_SR_OB_DR.tif'), origin='upper',
          extent=[-180, 180, -90, 90], transform=ccrs.PlateCarree())

#for record, geometry in zip(shp.records(), shp.geometries()):
#    ax.add_geometries([geometry], ccrs.PlateCarree(), facecolor='#c4c8ce', edgecolor='black', lw=0, alpha=0.1)
df = df.loc[df['EOI resp'] == 1]

plt.scatter(df['Long'], df['Lat'], facecolor='#F8F240', edgecolor='#292929', s=105, linewidths=0.6, alpha=0.9)

plt.savefig('C:/Users/she384/Documents/world_map_august.svg', format='svg')
