if "data_loader" not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test


from typing import Dict, List
from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
import gcsfs
import pandas as pd
from os import path


# from mage_ai.io.google_cloud_storage import GoogleCloudStorage
# from google.cloud import storage
# import pyarrow.parquet as pq


@data_loader
def load_from_google_cloud_storage(data: Dict, *args, **kwargs):
    """
    Template for loading data from a Google Cloud Storage bucket.
    Specify your configuration settings in 'io_config.yaml'.

    Docs: https://docs.mage.ai/design/data-loading#googlecloudstorage
    """
    config_path = path.join(get_repo_path(), "io_config.yaml")
    config_profile = "default"

    bucket_name = "rep-bucket1"
    object_key = f"raw/{data['name']}"

    print(object_key)


    df = pd.read_parquet(
        f'gs://{bucket_name}/{object_key}',
        storage_options={"token": "/home/src/REP_my_creds.json"})



    df["file_name"] = data["name"]



    return df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, "The output is undefined"
