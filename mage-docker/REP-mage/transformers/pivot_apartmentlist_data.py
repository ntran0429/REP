if "transformer" not in globals():
    from mage_ai.data_preparation.decorators import transformer
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test

import pandas as pd
import re


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

    # print(data[0])

    # Define the regex pattern for columns that match the format "YYYY_MM"
    pattern = re.compile(r"^\d{4}_\d{2}$")
    # Filter columns that do not match the pattern
    id_vars = [col for col in data[0].columns if not pattern.match(col)]

    print(id_vars)

    # Extract the distinct value from the 'file_name' column
    value_name = data[0]["file_name"].unique()[0].replace(".parquet", "")
    print(value_name)

    # id_vars: Specifies the column(s) to keep as identifier variables.
    # var_name: Specifies the name for the variable column.
    # value_name: Specifies the name for the value column.
    df_vancancy_index_melted = pd.melt(
        data[0],
        id_vars=id_vars,
        var_name="month_of_measurement",
        value_name=value_name,  # rent_estimates, rent_growth_mom, rent_growth_yoy, vacancy_rate
    )

    return df_vancancy_index_melted


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, "The output is undefined"
