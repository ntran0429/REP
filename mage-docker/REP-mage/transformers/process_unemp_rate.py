if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import datacommons_pandas as dc
import pandas as pd
from datetime import datetime



def add_name_col(df) -> pd.DataFrame:
  # Add a new column called name, where each value is the name for the place dcid in the index.
  df['name'] = df.index.map(dc.get_property_values(df.index, 'name'))
  
  # Keep just the first name, instead of a list of all names.
  df['name'] = df['name'].str[0]

  return df



@transformer
def transform(data, *args, **kwargs):
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your transformation logic here
    df_unemp_state = add_name_col(data)
    
    # set name column as first column
    cols = df_unemp_state.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    df_unemp_state = df_unemp_state[cols]



    # filter for months from 2017-01 to 2024-06
    current_year = datetime.now().year
    current_month = datetime.now().month

    # Calculate the previous month
    if current_month == 1:
        previous_month_year = current_year - 1
        previous_month = 12
    else:
        previous_month_year = current_year
        previous_month = current_month - 1

    date_range = pd.date_range(start='2017-01', end=f'{previous_month_year}-{previous_month}', freq='MS').strftime('%Y-%m').tolist()
    filtered_cols = ['name'] + [col for col in df_unemp_state.columns if col in date_range]
    df_unemp_state_filtered = df_unemp_state[filtered_cols]


    # pivot the table so that each row represents the unemployment rate for a state for a given month

    # id_vars=['name']: Specifies the column(s) to keep as identifier variables.
    # var_name='month_of_measurement': Specifies the name for the variable column.
    # value_name='unemployment_rate': Specifies the name for the value column.
    df_unemp_state_melted = pd.melt(
        df_unemp_state_filtered,
        id_vars=['name'],
        var_name='month_of_measurement',
        value_name='unemployment_rate'
        )



    return df_unemp_state_melted


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
