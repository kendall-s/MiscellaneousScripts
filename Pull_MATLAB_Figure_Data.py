from scipy.io import loadmat
import pandas as pd

'''
Script that extracts the X & Y data for lines plotted on Matlab figure which is saved as the .fig format

This scipt will grab all plotted data on a figure and output each to a CSV file. There is no way to really identify
each line - so you will have to open up the resultant files and plot them to figure out what is what... 

Change the SAVE_FOLDER_PATH and FIGURE_FILE_PATH to match your setup

'''

# Variables for the user to change
SAVE_FOLDER_PATH = 'C:/Users/she384/Documents/'
FIGURE_FILE_PATH = 'C:/Users/she384/Desktop/untitled.fig'

fig_file = loadmat(FIGURE_FILE_PATH, squeeze_me=True, struct_as_record=False)

# Don't have a clue why the data is under this key, but it works..
figure_data = fig_file['hgS_070000']

figure_data_children = figure_data.children

# Pull out the axes data, the other child is the legend but we don't want that
axes = [x for x in figure_data_children if x.type == 'axes']

# Now, typically there will only be 1 axes, but there is the possibility there could be 2 (param/param plot)
# so iterate through the axes list and then look at the children of that axis. The children will contain the
# Line and Text objects. Lines will be plotted data, Text will be annotations or Labels.
# Any line on the plot will be here, so a threshold line, e.g. in the RMNS plots, will have data points listed...

for ax_number, ax in enumerate(axes):
    ax_kids = ax.children
    for kid_number, kid in enumerate(ax_kids):
        # Check if the child is a Line object, not Text. If it is a line, get the X & Y data from it
        if kid.type == 'line':
            x_dat = kid.properties.XData
            y_dat = kid.properties.YData

            # Make dataframe from data and save it to CSV, drop NANs because MATLAB loves them....
            dat_df = pd.DataFrame(data={'x_data': x_dat, 'y_data': y_dat})
            dat_df = dat_df.dropna()
            dat_df.to_csv(f'{SAVE_FOLDER_PATH}axes_{ax_number}_line_{kid_number}.csv')

print('Completed, yay')
