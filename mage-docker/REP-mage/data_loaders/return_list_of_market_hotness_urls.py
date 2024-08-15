from typing import Dict, List


@data_loader
def load_data(*args, **kwargs) -> List[List[Dict]]:

    urls = [
        "https://econdata.s3-us-west-2.amazonaws.com/Reports/Hotness/RDC_Inventory_Hotness_Metrics_Metro_History.csv",
        "https://econdata.s3-us-west-2.amazonaws.com/Reports/Hotness/RDC_Inventory_Hotness_Metrics_County_History.csv",
    ]

    hotness_data = []
    metadata = []

    i = 0
    for u in urls:
        i += 1
        if "Metro" in u:
            name = "metro"
        else:
            name = "county"

        hotness_data.append(dict(id=i, name=name, url=f"{u}"))
        metadata.append(dict(block_uuid=f"for_data_{i}"))

    return [
        hotness_data,
        metadata,  # optional
    ]
