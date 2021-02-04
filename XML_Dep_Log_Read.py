""" Script to generate a more human readable output from the deployment log XML files """

import xml.etree.ElementTree as ET
import csv

tree = ET.parse('C:/Users/she384/Documents/Tests/in2019_v01005.xml')
root = tree.getroot()
count = 0
for i, child in enumerate(root):
    # print(child)
    count = i

line = []
for x in range(count):
    #print(root[x].tag)
    current_arr = []
    for y in root[x]:
        if len(y) > 0:
            line = []
            for v in y:
                line.append(v.text)
            print(line)
        current_arr.append(line)
    if root[x].tag == 'bottleData':
        bottle_data = current_arr
    if root[x].tag == 'ctdData':
        ctd_data = current_arr
    if root[x].tag == 'firingData':
        firing_data = current_arr
    if root[x].tag == 'firingPositionData':
        position_data = current_arr
    if root[x].tag == 'sampleData':
        sample_data = current_arr
    if root[x].tag == 'doTempData':
        do_temp_data = current_arr

filebuffer = open('test_xml_output.csv', 'w', newline='')
writer = csv.writer(filebuffer, delimiter=',')
writer.writerow([
    'RP', 'RP', 'NA', 'Depth', 'Temperature', 'Salinity', 'Oxygen', 'Date', 'RPFired', 'Longitude',
    'Latitude', 'Salinity Bottle', 'Oxygen Bottle', 'Nutrient Bottle', 'Draw Temp', 'RP'])
for i, x in enumerate(bottle_data):
    writer.writerow([x[0], x[1], x[2], ctd_data[i][0], ctd_data[i][1], ctd_data[i][2], ctd_data[i][3],
                    firing_data[i][0], firing_data[i][1], position_data[i][0], position_data[i][1], sample_data[i][0],
                    sample_data[i][1], sample_data[i][2], do_temp_data[i][0], do_temp_data[i][1]])

filebuffer.close()
