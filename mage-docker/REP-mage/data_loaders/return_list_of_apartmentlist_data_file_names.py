from typing import Dict, List


@data_loader
def load_data(*args, **kwargs) -> List[List[Dict]]:

    apartmentlist_file_names = [
        'monthly_rent_estimates.parquet',
        'monthly_rent_growth_mom.parquet',
        'monthly_rent_growth_yoy.parquet',
        'monthly_vacancy_index.parquet'
        ]

    apartmentlist_data = []
    metadata = []

    i = 0
    for file in apartmentlist_file_names:
        i += 1
        apartmentlist_data.append(dict(id=i, name=f'{file}'))
        metadata.append(dict(block_uuid=f'for_data_{i}'))

    return [
        apartmentlist_data,
        metadata, # optional
    ]
