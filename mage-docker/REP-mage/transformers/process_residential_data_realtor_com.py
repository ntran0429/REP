from mage_ai.data_cleaner.transformer_actions.base import BaseAction
from mage_ai.data_cleaner.transformer_actions.constants import ActionType, Axis
from mage_ai.data_cleaner.transformer_actions.utils import build_transformer_action
from pandas import DataFrame

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def execute_transformer_action(df: DataFrame, *args, **kwargs) -> DataFrame:
    """
    Execute Transformer Action: ActionType.CLEAN_COLUMN_NAME

    Docs: https://docs.mage.ai/guides/transformer-blocks#clean-column-names
    """
    action = build_transformer_action(
        df,
        action_type=ActionType.CLEAN_COLUMN_NAME,
        arguments=df.columns,
        axis=Axis.COLUMN,
    )



    # choose relevant columns for 'Housing' report page
    # month_date_yyyymm	cbsa_code	cbsa_title	HouseholdRank	median_listing_price	
    # median_listing_price_mm	median_listing_price_yy	active_listing_count	
    # active_listing_count_mm	active_listing_count_yy	median_days_on_market	
    # median_days_on_market_mm
    # median_days_on_market_yy	new_listing_count	new_listing_count_mm	
    # new_listing_count_yy	price_increased_count	price_increased_count_mm	
    # price_increased_count_yy	price_reduced_count	price_reduced_count_mm	
    # price_reduced_count_yy	pending_listing_count	pending_listing_count_mm	
    # pending_listing_count_yy	median_listing_price_per_square_foot	
    # median_listing_price_per_square_foot_mm	median_listing_price_per_square_foot_yy	
    # median_square_feet	median_square_feet_mm	median_square_feet_yy	
    # average_listing_price	average_listing_price_mm	average_listing_price_yy	
    # total_listing_count	total_listing_count_mm	total_listing_count_yy	pending_ratio	
    # pending_ratio_mm	pending_ratio_yy	quality_flag



    return BaseAction(action).execute(df)


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'