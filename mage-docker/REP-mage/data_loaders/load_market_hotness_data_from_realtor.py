import io
import pandas as pd
import requests
from typing import Dict, List
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_api(data: Dict, *args, **kwargs):
    """
    Template for loading data from API
    """
    url = data['url']
    response = requests.get(url)

    # print(data['name'])

    df = pd.read_csv(io.StringIO(response.text), sep=',')

    df['data_level'] = data['name']

    df.drop(df.index[-1], inplace=True)

    return df
    


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'