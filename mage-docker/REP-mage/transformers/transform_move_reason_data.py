if "transformer" not in globals():
    from mage_ai.data_preparation.decorators import transformer
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(cps_move_reason_df, *args, **kwargs):
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
    data_movers_only = cps_move_reason_df[
        (cps_move_reason_df["WHYMOVE"] != 0)  # remove NIU cases
        & (cps_move_reason_df["MIGRATE1"] == 5)  # filter for movers between states only
        & ~(
            cps_move_reason_df["MIGSTA1"].isin([91, 99])
        )  # remove NIU and Same house cases
    ]

    # print(data_movers_only.head())

    # recode values for WHYMOVE and MIGSTA1
    reason_for_moving_dict = {
        0: "NIU",
        1: "Change in marital status",
        2: "To establish own household",
        3: "Other family reason",
        4: "New job or job transfer",
        5: "To look for work or lost job",
        6: "For easier commute",
        7: "Retired",
        8: "Other job-related reason",
        9: "Wanted to own home, not rent",
        10: "Wanted new or better housing",
        11: "Wanted better neighborhood",
        12: "For cheaper housing",
        13: "Other housing reason",
        14: "Attend/leave college",
        15: "Change of climate",
        16: "Health reasons",
        17: "Other reasons",
        18: "Natural disaster",
        19: "Foreclosure or eviction",
        20: "Relationship with unmarried partner",
    }

    # Create a dictionary for "State of residence 1 year ago"
    state_residence_dict = {
        0: "NIU",
        1: "Alabama",
        2: "Alaska",
        4: "Arizona",
        5: "Arkansas",
        6: "California",
        8: "Colorado",
        9: "Connecticut",
        10: "Delaware",
        11: "District of Columbia",
        12: "Florida",
        13: "Georgia",
        15: "Hawaii",
        16: "Idaho",
        17: "Illinois",
        18: "Indiana",
        19: "Iowa",
        20: "Kansas",
        21: "Kentucky",
        22: "Louisiana",
        23: "Maine",
        24: "Maryland",
        25: "Massachusetts",
        26: "Michigan",
        27: "Minnesota",
        28: "Mississippi",
        29: "Missouri",
        30: "Montana",
        31: "Nebraska",
        32: "Nevada",
        33: "New Hampshire",
        34: "New Jersey",
        35: "New Mexico",
        36: "New York",
        37: "North Carolina",
        38: "North Dakota",
        39: "Ohio",
        40: "Oklahoma",
        41: "Oregon",
        42: "Pennsylvania",
        44: "Rhode Island",
        45: "South Carolina",
        46: "South Dakota",
        47: "Tennessee",
        48: "Texas",
        49: "Utah",
        50: "Vermont",
        51: "Virginia",
        53: "Washington",
        54: "West Virginia",
        55: "Wisconsin",
        56: "Wyoming",
        91: "Abroad",
        99: "Same house",
    }

    data_movers_only["WHYMOVE"] = data_movers_only["WHYMOVE"].map(
        reason_for_moving_dict
    )
    data_movers_only["MIGSTA1"] = data_movers_only["MIGSTA1"].map(state_residence_dict)

    movers_weighted = (
        data_movers_only.groupby(["YEAR", "WHYMOVE", "MIGSTA1"])["ASECWT"]
        .sum()
        .reset_index(name="count")
    )

    # rename the columns
    # YEAR -> year_surveyed
    # WHYMOVE -> move_reason
    # MIGSTA1 -> state_of_residence
    movers_weighted = movers_weighted.rename(
        columns={
            "YEAR": "year_surveyed",
            "WHYMOVE": "move_reason",
            "MIGSTA1": "state_of_residence"
        }
    )

    # print(movers_weighted.head())

    # add a column year_moved = year - 1
    movers_weighted["year_moved"] = movers_weighted["year_surveyed"] - 1

    # print(movers_weighted["year_surveyed"].unique())

    # reorder columns; year, year_moved, move_reason, state_of_residence, count
    movers_weighted = movers_weighted[
        ["year_surveyed", "year_moved", "move_reason", "state_of_residence", "count"]
    ]


    # remove records with year_moved = 2016, because we only have data for 2017, 2018, 2019, 2021,2022
    movers_weighted = movers_weighted[movers_weighted["year_moved"] != 2016]


    # add suffix ", USA" to state_of_residence
    movers_weighted["state_of_residence"] = movers_weighted["state_of_residence"].apply(
        lambda x: str(x) + ", USA"
    )

    # in state_of_residence, replace "New York, USA" with "NY, USA"
    movers_weighted["state_of_residence"] = movers_weighted[
        "state_of_residence"
    ].replace("New York, USA", "NY, USA")

    # remove index column
    movers_weighted.reset_index(drop=True, inplace=True)

    # print(movers_weighted["year_surveyed"].unique())

    return movers_weighted


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, "The output is undefined"
    # check if column year_surveyed has values 2017, 2018, 2019, 2021, 2022
    assert set(output["year_moved"].unique()) == {2017, 2018, 2019, 2021, 2022}, "The output does not have data for all 5 years"
