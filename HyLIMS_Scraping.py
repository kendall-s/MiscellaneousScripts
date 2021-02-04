""" Used to pull down all of the data in HyLIMS and format it in a meaningful way for Hydrochemistry team members """

import requests
import json
import pandas as pd
from pandas.io.json import json_normalize

# ******* USER UNIQUE VARIABLES - CHANGE TO SUIT (dont commit your password to a repo!) *******
CSIRO_IDENT = 'she384'
CSIRO_PW = ''
OUTPUT_PATH = 'C:/Users/she384/Documents/collated_results_csv_June.csv'

# Log in to HyLIMS
session = requests.Session()
session.post('http://www.cmar.csiro.au/data/hylims/login.cfm', data={"j_username": CSIRO_IDENT, "j_password": CSIRO_PW})

# To start, get all the results in HyLIMS, including nutrients, oxygen and salinity (ignoring Alkalinity rn)
salinity_request = session.get('http://www.cmar.csiro.au/data/hylims/results/details/json/?result_type_id=2&&sort=bottle_number&order=asc&offset=0&limit=50')
salinity_data = json.loads(salinity_request.text)
salinity_df = json_normalize(salinity_data)
salinity_df = salinity_df.dropna(subset=['lab_number'])

oxygen_request = session.get('http://www.cmar.csiro.au/data/hylims/results/details/json/?result_type_id=3&&sort=bottle_number&order=asc&offset=0&limit=500')
oxygen_data = json.loads(oxygen_request.text)
oxygen_df = json_normalize(oxygen_data)
oxygen_df = oxygen_df.dropna(subset=['lab_number'])

nutrient_request = session.get('http://www.cmar.csiro.au/data/hylims/results/details/json/?result_type_id=4&&sort=bottle_number&order=asc&offset=0&limit=500')
nutrient_data = json.loads(nutrient_request.text)
nutrient_df = json_normalize(nutrient_data)
nutrient_df = nutrient_df.dropna(subset=['lab_number'])

# Get all the batches in HyLIMS
batches_request = session.get('http://www.cmar.csiro.au/data/hylims/batches/json/?&sort=batch_id&order=desc&offset=0&limit=50&location_id=2&received_from=&received_to=')
batches_data = json.loads(batches_request.text)

# Make results dataframe
collated_results_df = pd.DataFrame(columns=['batch_number', 'batch_reference', 'date_received',
                                            'salinity_label', 'salinity_result', 'salinity_comment',
                                            'oxygen_label', 'oxygen_result', 'nutrient_label', 'nox_result',
                                            'nitrite_result', 'phosphate_result', 'silicate_result', 'ammonia_result',
                                            'site_id'])

# Get data from specific batches and organise data
# Iterate through each created batch
for row in batches_data:
    batch_id = row['batch_id']
    print(f'Reading batch: {batch_id}')
    # Grab the data for the specific batch, which includes site id and date collected values
    specific_batch_request = session.get(f'http://www.cmar.csiro.au/data/hylims/batches/details/json/?batch_id={batch_id}&order=asc&offset=0&limit=100')
    specific_batch_data = json.loads(specific_batch_request.text)
    # Iterate through each sample in the batch
    for sample in specific_batch_data:
        salinity_result = salinity_df.loc[salinity_df['lab_number'].astype('int32') == int(sample['lab_number'])]
        oxygen_result = oxygen_df.loc[oxygen_df['lab_number'].astype('int32') == int(sample['lab_number'])]
        nutrient_result = nutrient_df.loc[nutrient_df['lab_number'].astype('int32') == int(sample['lab_number'])]

        # Currently skips a batch if the reference field was left empty....
        if 'reference' in row:
            batch_reference = row['reference']
        else:
            break
        if 'reference' in sample:
            site_id = sample['reference']
        else:
            site_id = ""

        batch_number = batch_id
        date_recieved = row['date_received']
        if len(salinity_result) > 0:
            salinity_label = sample['salinity_bottle']
            salinity_value = salinity_result['calc_salinity'].values[0]
            if 'comments' in salinity_result:
                salinity_comment = salinity_result['comments'].values[0]
            else:
                salinity_comment = ""
        else:
            salinity_label = ""
            salinity_value = ""
            salinity_comment = ""

        if len(oxygen_result) > 0:
            oxygen_label = sample['oxygen_bottle']
            oxygen_value = oxygen_result['o2_ml_per_l'].values[0]
        else:
            oxygen_label = ""
            oxygen_value = ""

        if len(nutrient_result) > 0:
            nutrient_label = sample['nutrient_tube']

            nox_value = nutrient_result['nox_proc_value'].values[0]
            phosphate_value = nutrient_result['phosphate_proc_value'].values[0]
            nitrite_value = nutrient_result['nitrite_proc_value'].values[0]
            silicate_value = nutrient_result['silicate_proc_value'].values[0]
            ammonia_value = nutrient_result['ammonia_proc_value'].values[0]
        else:
            nutrient_label = ""
            nox_value = ""
            phosphate_value = ""
            nitrite_value = ""
            silicate_value = ""
            ammonia_value = ""

        to_append = {'batch_number': batch_number, 'batch_reference': batch_reference, 'date_received': date_recieved,
                     'salinity_label': salinity_label, 'salinity_result': salinity_value,
                     'salinity_comment': salinity_comment, 'oxygen_label': oxygen_label, 'oxygen_result': oxygen_value,
                     'nutrient_label': nutrient_label, 'nox_result': nox_value,
                     'nitrite_result': nitrite_value, 'phosphate_result': phosphate_value,
                     'silicate_result': silicate_value, 'ammonia_result': ammonia_value, 'site_id': site_id}

        collated_results_df = collated_results_df.append(to_append, ignore_index=True)

# Save to a CSV
collated_results_df.to_csv(OUTPUT_PATH)
print('Successfully completed.')