"""
This script will check what hydrology data is missing from an AODN NRS salinity, carbon, alkalinity, oxygen, nutrient
data file. It will then cross reference the missing samples to the HyLIMS database and determine if data is in HyLIMS
but not yet in the AODN or if the data is missing also from HyLIMS. It outputs two CSV files. The bulk of the script
is just writing it all to CSVs
"""

from selenium import webdriver
import csv
import pandas as pd
from time import sleep

# Your ident and password to login to hylims
IDENT = 'she384'
PASSWORD = 'hunter1'

# Need to download a web browser dirver for selenium to work, download chrome one here
# http://chromedriver.chromium.org/downloads --- unzip and copy the path to the .exe
WEBDRIVER_PATH = "C:/Users/she384/Downloads/chromedriver_win32/chromedriver.exe"

# This csv output file will include a detailed list of all salt, oxy and nut samples missing from the AODN data file
MISSING_AODN_FILES_OUTPUT_PATH = 'C:/Users/she384/Documents/missing_files_from_aodn.csv'

# This csv output file will say the status of data in hylims, if it was missing from the AODN data file
MISSING_AODN_HYLIMS_OUTPUT_PATH = 'C:/Users/she384/Documents/match_aodn_to_hylims.csv'

# Path to the downloaded AODN NRS data file
AODN_NRS_DATA_PATH = 'C:/Users/she384/Downloads/IMOS_National_Reference_Station_(NRS)_-_Salinity,_Carbon,_Alkalinity,_Oxygen_and_Nutrients_(Silicate,_Ammonium,_Nitrite_Nitrate,_Phosphate) (3).csv'
df = pd.read_csv(AODN_NRS_DATA_PATH, skiprows=68)

salinity_missing = []
oxygen_missing = []
nitrate_missing = []
phosphate_missing = []
silicate_missing = []
ammonia_missing = []

for i, x in enumerate(df['NRS_SAMPLE_CODE']):
    if pd.isna(df['SALINITY'].iloc[i]):
        salinity_missing.append(x)
    if pd.isna(df['OXYGEN_UMOL_PER_L'].iloc[i]) and (df['STATION_NAME'].iloc[i] == 'Maria Island' or df['STATION_NAME'].iloc[i] == 'Rottnest Island'):
        oxygen_missing.append(x)
    if  pd.isna(df['NITRATE_UMOL_PER_L'].iloc[i]):
       nitrate_missing.append(x)
    if pd.isna(df['PHOSPHATE_UMOL_PER_L'].iloc[i]):
        phosphate_missing.append(x)
    if pd.isna(df['SILICATE_UMOL_PER_L'].iloc[i]):
        silicate_missing.append(x)
    if pd.isna(df['AMMONIUM_UMOL_PER_L'].iloc[i]):
        ammonia_missing.append(x)

salinity_batches_missing = []
oxygen_batches_missing = []
nitrate_batches_missing = []

with open(MISSING_AODN_FILES_OUTPUT_PATH, 'w+', newline='') as file:
    write = csv.writer(file)
    write_buffer = []
    write.writerow(['Missing Salinities'])
    for x in salinity_missing:
        write_buffer.append(x)
        if write_buffer[0][6:12] == write_buffer[-1][6:12]:
            pass
        else:
            write.writerow([write_buffer[0][3:12]])
            for x in write_buffer[:-1]:
                write.writerow([x])
            write.writerow('')
            salinity_batches_missing.append(write_buffer[0][3:14])
            write_buffer = []
    write.writerow([''])
    write.writerow(['Missing Oxygens'])
    for x in oxygen_missing:
        write_buffer.append(x)
        if write_buffer[0][6:12] == write_buffer[-1][6:12]:
            pass
        else:
            write.writerow([write_buffer[0][3:12]])
            for x in write_buffer[:-1]:
                write.writerow([x])
            write.writerow('')
            oxygen_batches_missing.append(write_buffer[0][3:14])
            write_buffer = []

    write.writerow([''])
    write.writerow(['Missing Nitrate'])
    for x in nitrate_missing:
        write_buffer.append(x)
        if write_buffer[0][6:12] == write_buffer[-1][6:12]:
            pass
        else:
            write.writerow([write_buffer[0][3:12]])
            for x in write_buffer[:-1]:
                write.writerow([x])
            write.writerow('')
            nitrate_batches_missing.append(write_buffer[0][3:14])
            write_buffer = []
    write.writerow([''])
    write.writerow(['Missing Phosphate'])
    for x in phosphate_missing:
        write_buffer.append(x)
        if write_buffer[0][6:12] == write_buffer[-1][6:12]:
            pass
        else:
            write.writerow([write_buffer[0][3:12]])
            for x in write_buffer[:-1]:
                write.writerow([x])
            write.writerow('')
            write_buffer = []
    write.writerow([''])
    write.writerow(['Missing Silicate'])
    for x in silicate_missing:
        write_buffer.append(x)
        if write_buffer[0][6:12] == write_buffer[-1][6:12]:
            pass
        else:
            write.writerow([write_buffer[0][3:12]])
            for x in write_buffer[:-1]:
                write.writerow([x])
            write.writerow('')
            write_buffer = []
    write.writerow([''])
    write.writerow(['Missing Ammonia'])
    for x in ammonia_missing:
        write_buffer.append(x)
        if write_buffer[0][6:12] == write_buffer[-1][6:12]:
            pass
        else:
            write.writerow([write_buffer[0][3:12]])
            for x in write_buffer[:-1]:
                write.writerow([x])
            write.writerow('')
            write_buffer = []

browser = webdriver.Chrome(WEBDRIVER_PATH)

browser.get('http://www.cmar.csiro.au/data/hylims/login.cfm')

username = browser.find_element_by_xpath('//*[@id="username"]')
username.send_keys(IDENT)

password = browser.find_element_by_xpath('//*[@id="password"]')
password.send_keys(PASSWORD)

login = browser.find_element_by_xpath('/html/body/div[2]/form/button')
login.click()

browser.get('http://www.cmar.csiro.au/data/hylims/batches/')

search = browser.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[1]/div[1]/div[3]/input')

with open(MISSING_AODN_HYLIMS_OUTPUT_PATH, 'w+', newline='') as file:
    write = csv.writer(file)
    write.writerow(['Salinity samples \n'])
    for x in salinity_batches_missing:
        search.send_keys(x)
        sleep(10)
        try:
            salinity_samples = browser.find_element_by_xpath('//*[@id="batch-table"]/tbody/tr/td[13]')
            print(salinity_samples.text)
            search.clear()
            slash_pos = salinity_samples.text.find('/')

            try:
                completed_samples = int(salinity_samples.text[0:slash_pos])
                expected_samples = int(salinity_samples.text[slash_pos+1:])
            except ValueError:
                completed_samples = 1
                expected_samples = -1

            if completed_samples == expected_samples:
                write.writerow([x])
                #write.writerow([salinity_samples.text])
                write.writerow(['In HyLIMS not in AODN'])
                #print('All Salinity data in HyLIMS')
            else:
                write.writerow([x])
                #write.writerow([salinity_samples.text])
                write.writerow(['Missing results from HyLIMS'])
                #print('Salinity data missing from HyLIMS')

        except Exception:
            write.writerow([x])
            write.writerow(['No entry in database at all'])
            search.clear()

        write.writerow(['\n'])

    write.writerow(['Oxygen samples \n'])
    for x in oxygen_batches_missing:
        search.send_keys(x)
        sleep(5)
        try:
            oxygen_samples = browser.find_element_by_xpath('//*[@id="batch-table"]/tbody/tr/td[12]')
            print(oxygen_samples.text)
            search.clear()
            slash_pos = oxygen_samples.text.find('/')

            try:
                completed_samples = int(oxygen_samples.text[0:slash_pos])
                expected_samples = int(oxygen_samples.text[slash_pos + 1:])
            except ValueError:
                completed_samples = 1
                expected_samples = -1

            if completed_samples == expected_samples:
                write.writerow([x])
                write.writerow(['In HyLIMS, not in AODN'])
                # print('All oxygen data in HyLIMS')
            else:
                write.writerow([x])
                write.writerow(['Missing results from HyLIMS'])
                # print('oxygen data missing from HyLIMS')

        except Exception:
            write.writerow([x])
            write.writerow(['No entry in database at all'])
            search.clear()

        write.writerow(['\n'])

    write.writerow(['Nitrate samples \n'])
    for x in nitrate_batches_missing:
        search.send_keys(x)
        sleep(5)
        try:
            nitrate_samples = browser.find_element_by_xpath('//*[@id="batch-table"]/tbody/tr/td[11]')
            print(nitrate_samples.text)
            search.clear()
            slash_pos = nitrate_samples.text.find('/')

            try:
                completed_samples = int(nitrate_samples.text[0:slash_pos])
                expected_samples = int(nitrate_samples.text[slash_pos + 1:])
            except ValueError:
                completed_samples = 1
                expected_samples = -1

            if completed_samples == expected_samples:
                write.writerow([x])
                write.writerow(['In HyLIMS, not in AODN'])
                # print('All nitrate data in HyLIMS')
            else:
                write.writerow([x])
                write.writerow(['Missing results from HyLIMS'])
                # print('nitrate data missing from HyLIMS')

        except Exception:
            write.writerow([x])
            write.writerow(['No entry in database at all'])
            search.clear()

        write.writerow(['\n'])

browser.close()

