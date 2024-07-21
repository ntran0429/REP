import pandas as pd
import numpy as np
import math
import glob
import re
import os
from os import path
import io
import requests
from google.cloud import storage

if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test



def upload_to_gcs(bucket, object_name, local_file):
    """
    Ref: https://cloud.google.com/storage/docs/uploading-objects#storage-upload-object-python
    """
    # # WORKAROUND to prevent timeout for files > 6 MB on 800 kbps upload speed.
    # # (Ref: https://github.com/googleapis/python-storage/issues/74)
    # storage.blob._MAX_MULTIPART_SIZE = 5 * 1024 * 1024  # 5 MB
    # storage.blob._DEFAULT_CHUNKSIZE = 5 * 1024 * 1024  # 5 MB

    client = storage.Client.from_service_account_json('/home/src/REP_my_creds.json')

    # client = storage.Client()
    bucket = client.bucket(bucket)
    blob = bucket.blob(object_name)
    blob.upload_from_filename(local_file)


def transform_files(final_file_name):
    # Import all migration data
    path = r'/home/src/'
    all_files = glob.glob(path + '/*.xlsx')

    li = []

    for filename in all_files:
        df = pd.read_excel(filename,na_values=['(NA)'], header = 6).fillna(0)
        
        # Remove all the MOE columns and the Footnotes which are from row 70 to 76 for all the data files
        df = df.loc[:70,(df != 'MOE').all()]

        # Adjust the column names
        df.rename(columns=
                {df.columns[0]: 'destination_state',
                df.columns[1]: 'population',
                df.columns[2]: 'same_house',
                df.columns[3]: 'same_state',
                df.columns[4]: 'from_different_state_Total',
                df.columns[-4]: 'abroad_Total',
                df.columns[-3]: 'abroad_PuertoRico',
                df.columns[-2]: 'abroad_USIslandArea',
                df.columns[-1]: 'abroad_ForeignCountry'
                }, inplace = True)

        #for i in range(4,56):
        #    df.rename(columns = {df.columns[i]:'from_state_' + df.columns[i]}, inplace = True)

        # Remove NA rows and duplicate columns
        df = df[df['destination_state'] != 0]
        df = df[df.columns.drop(list(df.filter(regex='Unnamed:')))]
        df = df.drop([2])
        df = df.drop([37])

        # Rename the first element and set the first column as index
        # df.values[0][0] = 'United States'
        
        # Change all columns to integer
        for col in df.columns[1:]:
            df[col] = df[col].astype('int64')
            
        # Create a column to store the year based on the Excel file name
        df['year'] = re.findall('\d+', os.path.basename(filename))[0]
        
        # Reset index
        df.reset_index(drop = True, inplace = True)
            
        li.append(df)

    
    
    migration_df = pd.concat(li)

    id_var = ['destination_state','year', 'population','same_house', 'same_state','from_different_state_Total','abroad_Total']
    id_values = [col for col in migration_df.columns if col not in id_var]
    df_long = pd.melt( migration_df, id_var , id_values, 'from', 'number_of_people' )


    df_long.to_csv(final_file_name, index=False)
    print(f"Saved locally: {final_file_name}")

    return df_long


@custom
def load_raw_migration_data_to_gsc(*args, **kwargs):
    """
    args: The output from any upstream parent blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your custom logic here

    years = [2017, 2018, 2019, 2021, 2022]
    base_url = 'https://www2.census.gov/programs-surveys/demo/tables/geographic-mobility/'

    bucket_name = 'rep-bucket1'

    for year in years:
        if year != 2022:
            download_url = base_url + f'{year}/state-to-state-migration/State_to_State_Migrations_Table_{year}.xls'
        else:
            download_url = base_url + '2022/state-to-state-migration/State_to_State_Migration_Table_2022_T13_updated_2024_06_27.xlsx'
        
        r = requests.get(download_url)

        if year != 2022:
            file_name = f'state-to-state-migration-{year}.xls'
        else:
            file_name = f'state-to-state-migration-{year}.xlsx'

        open(file_name, 'wb').write(r.content)
        print(f"Saved locally: {file_name}")
        
        upload_to_gcs(bucket_name, f"raw/state-to-state-migratioWn-{year}", file_name)
        print(f"Uploaded raw files to GCS: {file_name}")
        



    transformed_file_name = 'migration_2017-2022.csv'
    # tidy all files, combine into one file, save file locally
    migration_df = transform_files(transformed_file_name)

    upload_to_gcs(bucket_name, f"cleansed/migration_2017-2022", transformed_file_name)
    print(f"Uploaded transformed files to GCS: {transformed_file_name}")

    


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
