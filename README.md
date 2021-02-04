# MiscellaneousScripts

Random scripts that have served their purpose for meanial tasks but are interesting to keep nonetheless

Some scripts below generate plots, I have put the plots in a pdf for viewing [here](https://github.com/kendall-s/MiscellaneousScripts/blob/main/Various_Plots_and_Charts.pdf)

## Contents:

- AODN_Checker: Used to compare the finalised data in HyLIMS with the data that was been scraped and pulled across into the AODN database. 

- CTD_Trace_Plots: Simple script to produce line plots of the temperature and salinity from the raw CTD files

- HyLIMS_Scraping: This script pulls down the data from the Hydrochemistry database and formats the data into a meaningful way for Hydrochemistry team members to use

- INIV_Locations_World_Map: Basic world map showing the locations of participants for the INIV2022 voyage. Generates locations from csv with header fmt ['Long', 'Lat', 'EOI resp']

- Mac_Harbour_Microbial: Needed to generate high resolution of map of Macquarie Harbour to show where microbial grab samples were taken and to contrast the water temperature between the two depths

- Phosphate_Data_Corrections: Programmatically fix all the incorrect values in a NetCDF file using a user correct .CSV file

- Pull_MATLAB_Figure_Data: Use this when all you have is a .fig file. A .fig file contains the original data and can be extracted programatically and with Python 😎

- SR03_Stations-Cartopy: When plotting large distances on a map things can become skewed or look off if not using a projection transform. Using cartopy to create a PlateCarree map the station map looks much more like it should

- Salinity_to_Conductivity: Used to convert data measured on a salinometer from practical salinity units to conductivity

- T_S_Plots: Script to generate TS signature plots from the CTD output netcdf 

- XML_Dep_Log_Read: Used to read out the data from a deployment log XML file and convert it to a much more friendly csv file for Hydrochemistry team members

- in2019_v05_Transect_Overview: Multi pane chart that provides a comprehensive overview of a transect that includes triaxus data, uses data from 9 sources
