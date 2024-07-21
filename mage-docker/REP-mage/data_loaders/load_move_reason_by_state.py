import os
from ipumspy import IpumsApiClient, MicrodataExtract, readers

from mage_ai.data_preparation.shared.secrets import get_secret_value

if "data_loader" not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data(*args, **kwargs):
    """
    ipumspy docs: https://ipumspy.readthedocs.io/en/latest/index.html
    extract example: https://blog.popdata.org/automating-monthly-workflows-using-cps-microdata-extract-api/

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your data loading logic here

    # delete files /home/src/cps_*
    files = os.listdir("/home/src")
    for file in files:
        if "cps_" in file:
            os.remove(os.path.join("/home/src", file))

    ipums = IpumsApiClient(get_secret_value("IPUMS_API_KEY"))

    cps_move_reason = MicrodataExtract(
        description="reason for moving to another state extract",
        collection="cps",
        samples=[
            "cps2017_03s",
            "cps2018_03s",
            "cps2019_03s",
            "cps2020_03s",
            "cps2022_03s",
            "cps2023_03s",
        ],
        variables=["WHYMOVE", "MIGSTA1", "MIGRATE1"],
        data_structure={"rectangular": {"on": "P"}},
        data_format="csv",
        case_select_who="individuals",
    )

    ipums.submit_extract(cps_move_reason)
    print(
        f"{cps_move_reason.collection} extract number {cps_move_reason.extract_id} has been submitted!"
    )
    ipums.wait_for_extract(cps_move_reason)
    print(
        f"{cps_move_reason.collection} extract number {cps_move_reason.extract_id} is complete!"
    )
    ipums.download_extract(cps_move_reason)

    filename = (
        f"{cps_move_reason.collection}_{str(cps_move_reason.extract_id).zfill(5)}"
    )
    cps_move_reason_ddi = readers.read_ipums_ddi(f"/home/src/{filename}.xml")
    cps_move_reason_df = readers.read_microdata(
        cps_move_reason_ddi, f"{filename}.csv.gz"
    )
    cps_move_reason_df.head()
    # print(cps_move_reason_df.info)

    return cps_move_reason_df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, "The output is undefined"
