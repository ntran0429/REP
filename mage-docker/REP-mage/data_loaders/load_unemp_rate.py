if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


# Install datacommons_pandas
# !pip install datacommons_pandas --upgrade --quiet
# Import Data Commons
import datacommons_pandas as dc

# Import other required libraries
# import matplotlib.pyplot as plt
# import matplotlib.patches as mpatches
import pandas as pd
import json
import io
import requests

@data_loader
def load_data_from_api(*args, **kwargs):
    """
    Loading data from Data Commons API

    Google Colab Notebook to query data from Data Commons API
    https://colab.research.google.com/github/datacommonsorg/api-python/blob/master/notebooks/analyzing_census_data.ipynb#scrollTo=PJQ1kDAhEc2d

    Other links to understand how to query the data:
    https://github.com/datacommonsorg/data/blob/master/docs/representing_statistics.md
    https://datacommons.org/tools/statvar
    """


    usa = 'country/USA'

    # Get lists of states, counties, and cities within the United States, respectively.
    states = dc.get_places_in([usa], 'State')[usa]
    counties = dc.get_places_in([usa], 'County')[usa]
    cities = dc.get_places_in([usa], 'City')[usa]


    print(states[:10])
    print(counties[:10])
    print(cities[:10])



    # datacommons_pandas.build_multivariate_dataframe(places, stat_vars)
    # Returns a pandas.DataFrame with places as index and stat_vars as columns,
    # where each cell is latest observed statistic for its Place and StatisticalVariable.

    # UnemploymentRate_Person: Unemployment Rate of a Population; Monthly

    # Get unemployment rate for states.
    df_state = dc.build_time_series_dataframe(states, 'UnemploymentRate_Person', desc_col=True)

    # # Get StatVarObservations for counties.
    # df_county = dc.build_multivariate_dataframe(counties, ['Count_Person', 'UnemploymentRate_Person'])
    # # Get StatVarObservations for cities.
    # df_city = dc.build_multivariate_dataframe(cities, ['Count_Person', 'UnemploymentRate_Person'])


    return df_state


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
