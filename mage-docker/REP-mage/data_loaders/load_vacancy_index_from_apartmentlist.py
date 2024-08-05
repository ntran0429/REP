from datetime import datetime
from dateutil.relativedelta import relativedelta
import io
import pandas as pd
import requests
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_api(*args, **kwargs):
    """
    data source page:
    https://www.apartmentlist.com/research/category/data-rent-estimates
    """

    config = {
        'file_name': 'monthly_vacancy_index'
    }

    # Get the current date and subtract one month
    current_date = datetime.now()
    previous_date = current_date - relativedelta(months=1)
    previous_year = previous_date.year
    previous_month = previous_date.strftime("%m")

    # Parameterize the URL with the previous month and year
    url = (
        f"https://assets.ctfassets.net/jeox55pd4d8n/"
        f"57AxCwpMEvVk0Nq3P5eJCk/"
        f"c17a8929f764d99a81db262bc137247e/"
        f"Apartment_List_Vacancy_Index_{previous_year}_{previous_month}.csv"
    )


    response = requests.get(url)

    return [pd.read_csv(io.StringIO(response.text), sep=','), config]



@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'