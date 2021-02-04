import matplotlib.pyplot as plt
import xarray as xr
import statistics
import numpy as np
import pandas as pd
import os
import math
import matplotlib as mpl
import calendar, time
import cartopy.crs as ccrs
from matplotlib import cm


mpl.style.use('seaborn-muted')
mpl.rc('font', family='Segoe UI Symbol', )

MAX_PRESSURE = 300

extent = [153.8, 155.2, -26.8, -27.8]
extent2 = [153.6, 155.4, -26.6, -28]

mooring_sites = [[-27.102, 155.299], [-27.206, 154.648], [-27.249, 154.297], [-27.283, 154.137],
                 [-27.318, 154.001], [-27.329, 153.898]]
mooring_labels = ['M6_4800', 'M5_4700', 'M4_4200', 'M3_3200', 'M2_2000', 'M1_500']

fig = plt.figure(figsize=(16, 13))

fig.set_tight_layout(tight=True)

map_plot = plt.subplot2grid((2, 5), (0, 0), projection=ccrs.PlateCarree(), colspan=2)

nut_map = plt.subplot2grid((2, 5), (1, 0), projection=ccrs.PlateCarree(), colspan=2)

nut_map.background_patch.set_facecolor('#bde1f1')
map_plot.background_patch.set_facecolor('#bde1f1')

#nut_map.gridlines(alpha=0.5, color='black', linestyle='--', zorder=0)
#map_plot.gridlines(alpha=0.5, color='black', linestyle='--', zorder=0)
nut_map.set_extent(extent)
map_plot.set_extent(extent2)

x_ticks = np.linspace(extent[0], extent[1], 5)
y_ticks = np.linspace(extent[2], extent[3], 5)

x_ticks2 = np.linspace(extent2[0], extent2[1], 5)
y_ticks2 = np.linspace(extent2[2], extent2[3], 5)

map_plot.set_xticks([153.6, 153.8, 154, 154.2, 154.4, 154.6, 154.8, 155, 155.2, 155.4])
map_plot.set_yticks(y_ticks2)
nut_map.set_xticks(x_ticks)
nut_map.set_yticks(y_ticks)

adcp_u_plot = plt.subplot2grid((4,5), (0, 2), colspan=3)

adcp_v_plot = plt.subplot2grid((4,5), (1, 2), colspan=3)

triaxus_salt = plt.subplot2grid((4,5), (2, 2), colspan=3)

triaxus_temp = plt.subplot2grid((4,5), (3, 2), colspan=3)

#triaxus_chl = plt.subplot2grid((5,3), (4, 1), colspan=2)

#nut_hist = plt.subplot2grid((3,3), (1, 0))

nowcast = xr.open_dataset(r"C:\Users\she384\Documents\in2019_v05\Exploratory\Nowcast\ocean_fc_2019091612_024_surface.nc")
triaxus = xr.open_dataset(r"C:\Users\she384\Documents\in2019_v05\Exploratory\Triaxus\in2019_v05_02_002.nc")
adcp = xr.open_dataset(r"C:\Users\she384\Documents\in2019_v05\Exploratory\150ACDP\os150nb.nc")
rvi_uwy = xr.open_dataset(r"C:\Users\she384\Documents\in2019_v05\Exploratory\Underway\in2019_v05uwy.nc")
nuts_uwy = xr.open_dataset(r'C:\Users\she384\Documents\in2019_v05\Exploratory\AA100\in2019_v05.nc')

triaxus_start_time = calendar.timegm(time.strptime(triaxus.start_time[:20], "%b %d %Y %H:%M:%S"))

epochdate = rvi_uwy.Epoch
datetoconvert = epochdate[-22:-3]
uwyformat = '%Y-%m-%d %H:%M:%S'
ts = time.strptime(datetoconvert, uwyformat)
epochtimestamp = calendar.timegm(ts)
starttime = epochtimestamp + float(epochdate[0:8])

rvi_lat = rvi_uwy.latitude.values

rvi_times = np.array([(starttime + (i * 5)) for i, x in enumerate(rvi_lat)])

rvi_uwy_start_index = np.where(rvi_times > triaxus_start_time)

rvi_lat = rvi_uwy.latitude[rvi_uwy_start_index[0][0]:]
rvi_lon = rvi_uwy.longitude[rvi_uwy_start_index[0][0]:]

rvi_fluoro = rvi_uwy.fluorescence[rvi_uwy_start_index[0][0]:].values

F_temp_df = pd.DataFrame(list(zip(rvi_fluoro, rvi_lon, rvi_lat)), columns=['F', 'lon', 'lat'])

F_df = F_temp_df.loc[(F_temp_df['F'] > 0) & (F_temp_df['F'] < 5)]

F_to_plot = F_df['F'].values
Flon_to_plot = F_df['lon'].values
Flat_to_plot = F_df['lat'].values

F_depths = [25 for x in Flon_to_plot]

print(rvi_fluoro)

map_plot.set_facecolor('#DDF7F9')

nowcast_lon = nowcast.xu_ocean
nowcast_lat = nowcast.yu_ocean
nowcast_usurf = nowcast.usurf[0, :, :]
nowcast_vsurf = nowcast.vsurf[0, :, :]
nowcast_sst = nowcast.sst[0, :, :]

ss_temp = map_plot.contourf(nowcast_lon, nowcast_lat, nowcast_sst, levels=25, cmap = 'bwr', alpha=0.7)
map_plot.quiver(nowcast_lon, nowcast_lat, nowcast_usurf, nowcast_vsurf, alpha=0.7, scale = 15)

sst_cb = plt.colorbar(ss_temp, ax=map_plot)
sst_cb.set_label('Sea Surface Temperature')
sst_cb.set_alpha(1)
sst_cb.draw_all()

for i, x in enumerate(mooring_labels):
    map_plot.plot(mooring_sites[i][1], mooring_sites[i][0], marker='o', color='#E6EB58', lw=0)
    map_plot.annotate(x, (mooring_sites[i][1], mooring_sites[i][0]))

map_plot.plot(rvi_lon, rvi_lat, lw=1.5, linestyle='--', color='black')
map_plot.grid(alpha=0.5, zorder=0)

nut_map.plot(rvi_lon, rvi_lat, lw=0.75, linestyle='--', color='black')

nut_time = nuts_uwy.time.values

nut_start_index = np.where(nut_time > triaxus_start_time)

nut_lat = nuts_uwy.latitude[nut_start_index[0][0]:]
nut_lon = nuts_uwy.longitude[nut_start_index[0][0]:]

nut_nit = nuts_uwy.nitrate[nut_start_index[0][0]:]


Flat_to_plot = Flat_to_plot +0.04
flr = nut_map.scatter(Flon_to_plot[:-5000], Flat_to_plot[:-5000], c=F_to_plot[:-5000], zorder= 4, cmap='winter', alpha=0.5, s=14)
nts = nut_map.scatter(nut_lon, nut_lat, c=nut_nit, zorder=4)

nut_cb = plt.colorbar(nts, ax=nut_map)
nut_cb.set_label('Nitrate (uM)')

nut_map.set_facecolor('#DDF7F9')

#for i, x in enumerate(mooring_labels):
#    nut_map.plot(mooring_sites[i][1], mooring_sites[i][0], marker='o', color='#E6EB58', lw=0)
#    nut_map.annotate(x, (mooring_sites[i][1], mooring_sites[i][0]))

nut_map.grid(alpha=0.5, zorder=0)

adcp_time = adcp.time.values
adcp_time_epoch = (adcp_time.astype('uint64') / 1e9).astype('uint32')


adcp_start_index = np.where(adcp_time_epoch > triaxus_start_time)

adcp_lon = adcp.lon[adcp_start_index[0][0]:].values
adcp_lat = adcp.lat[adcp_start_index[0][0]:].values
adcp_depth = adcp.depth[0, :]


adcp_v = adcp.v[adcp_start_index[0][0]:, :].values
adcp_u = adcp.u[adcp_start_index[0][0]:, :].values


adcp_v_surf = adcp.v[adcp_start_index[0][0]:, 0].values
adcp_u_surf = adcp.u[adcp_start_index[0][0]:, 0].values

qc_dataframe = pd.DataFrame(list(zip(adcp_lon, adcp_lat, adcp_v_surf, adcp_u_surf)), columns=['lon', 'lat', 'v', 'u'])

print(qc_dataframe.head())

qc_dataframe = qc_dataframe.loc[(qc_dataframe['v'] >= -1.44) & (qc_dataframe['v'] <= 1.57)]
qc_dataframe = qc_dataframe.loc[(qc_dataframe['u'] >= -0.72) & (qc_dataframe['u'] <= 1.22)]

adcp_lon_surf = qc_dataframe['lon'].values
adcp_lat_surf = qc_dataframe['lat'].values
adcp_u_surf = qc_dataframe['u'].values
adcp_v_surf = qc_dataframe['v'].values

map_plot.quiver(adcp_lon_surf, adcp_lat_surf, adcp_u_surf, adcp_v_surf, zorder=5, alpha=0.9)
nut_map.quiver(adcp_lon_surf, adcp_lat_surf, adcp_u_surf, adcp_v_surf)

v = np.linspace(-.73, 1.21, 15, endpoint=True)

u_plot = adcp_u_plot.contourf(adcp_lon, adcp_depth, adcp_u.T, v)

adcp_u_plot.set_title('ADCP U Component (Positive = magnitude East)')
adcp_u_cb = plt.colorbar(u_plot, ax=adcp_u_plot)
adcp_u_cb.set_label('Current speed (m/s)')
adcp_u_plot.invert_yaxis()
adcp_u_plot.set_ylim(300, 0)
adcp_u_plot.xaxis.grid(alpha=0.3)
adcp_u_plot.set_xlim(153.8, 155)

depth_gen = [13 for x in nut_lon]
adcp_u_plot.scatter(nut_lon, depth_gen, c=nut_nit, s=30)
v = np.linspace(-1.44, 1.57, 15, endpoint=True)

av = adcp_v_plot.contourf(adcp_lon, adcp_depth, adcp_v.T, v)

adcp_v_plot.set_title('ADCP V Component (Positive = magnitude North)')
av_cb = plt.colorbar(av, ax=adcp_v_plot)
av_cb.set_label('Current speed (m/s)')
adcp_v_plot.invert_yaxis()
adcp_v_plot.set_ylim(300, 0)
adcp_v_plot.scatter(nut_lon, depth_gen, c=nut_nit, s=30)
adcp_v_plot.xaxis.grid(alpha=0.3)
adcp_v_plot.set_xlim(153.8, 155)

triaxus_salt.set_title('Triaxus Salinity')
ts = triaxus_salt.tricontourf(triaxus.LONGITUDE, triaxus.PRES, triaxus.PSAL, levels=15, cmap='plasma')
triaxus_salt_cb = plt.colorbar(ts, ax=triaxus_salt)
triaxus_salt_cb.set_label('Salinity')
triaxus_salt.invert_yaxis()
triaxus_salt.scatter(nut_lon, depth_gen, c=nut_nit, s=30)
#triaxus_salt.scatter(Flon_to_plot, F_depths, c=F_to_plot, s=20)
triaxus_salt.set_ylim(300, 0)
triaxus_salt.xaxis.grid(alpha=0.3)
#ts2 = triaxus_salt.contour(triaxus.LONGITUDE, triaxus.PRES, triaxus.PSAL, levels=[35.5, 35.60, 35.70], colors='black', linewidths=0.5)
triaxus_salt.set_xlim(153.8, 155)

triaxus_temp.set_title('Triaxus Temperature')
tt = triaxus_temp.tricontourf(triaxus.LONGITUDE, triaxus.PRES, triaxus.TEMP, levels=15, cmap='coolwarm')
triaxus_temp_cb = plt.colorbar(tt, ax=triaxus_temp)
triaxus_temp_cb.set_label('Temperature (degC)')
triaxus_temp.invert_yaxis()
triaxus_temp.scatter(nut_lon, depth_gen, c=nut_nit, s=30)
triaxus_temp.set_ylim(300, 0)
triaxus_temp.set_xlabel('Longitude')
triaxus_temp.xaxis.grid(alpha=0.3)
triaxus_temp.set_xlim(153.8, 155)
#triaxus_chl.tricontourf(triaxus.LONGITUDE, triaxus.PRES, triaxus.CNDC, levels=20)
#triaxus_chl.invert_yaxis()

#map_plot.plot([154.6, 154.6], [-26.60, -28.00], color='#E4C83D', linestyle='--', lw=1)
#adcp_u_plot.plot([154.6, 154.6], [300, 0], color='#E4C83D', linestyle='--', lw=1)
#adcp_v_plot.plot([154.6, 154.6], [300, 0], color='#E4C83D', linestyle='--', lw=1)
#triaxus_temp.plot([154.6, 154.6], [300, 0], color='#E4C83D', linestyle='--', lw=1)
#triaxus_salt.plot([154.6, 154.6], [300, 0], color='#E4C83D', linestyle='--', lw=1)

map_plot.set_title('Ship track with ADCP over Nowcast SST filled contour')
nut_map.set_title('Underway Nitrate with ADCP next to underway Fluorescence')
fig.set_tight_layout(tight=True)

#plt.suptitle('Triaxus tow: 18/09/2019')

plt.savefig('C:/Users/she384/Documents/in2019_v05/Exploratory/Plots/autosaves/' + str(time.time()) + '.png', dpi=350,
            bbox_inches="tight")

plt.show()

