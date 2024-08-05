import pyarrow as pa
import pyarrow.parquet as pq
import os

if "data_exporter" not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = (
    "/home/src/REP_my_creds.json"
)


@data_exporter
def export_data(inputs, *args, **kwargs) -> None:
    """
    Exports data to some source.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Output (optional):
        Optionally return any object and it'll be logged and
        displayed when inspecting the block run.
    """
    # Specify your data exporting logic here

    data_1 = inputs[0]
    config_1 = inputs[1]

    # print(data.head())

    # print("\n \n")

    data_2 = args[0][0]
    config_2 = args[0][1]

    data_3 = args[1][0]
    config_3 = args[1][1]

    data_4 = args[2][0]
    config_4 = args[2][1]



    print(config_1)
    print(config_2)
    print(config_3)
    print(config_4)


    iterate_list = [
        (data_1, config_1),
        (data_2, config_2),
        (data_3, config_3),
        (data_4, config_4)
    ]



    bucket_name = "rep-bucket1"
    project_id = "real-estate-project-430020"

    folder_name = "raw"


    for data, config in iterate_list: 
        file_name = f"{config.get('file_name')}.parquet"

        file_path = f"{bucket_name}/{folder_name}/{file_name}"


        
        # Define the schema
        # schema = pa.schema([
        #     ('year_surveyed', pa.int32()),
        # ])

        # or infer the schema with pa.Schema.from_pandas method
        # https://arrow.apache.org/docs/python/generated/pyarrow.Schema.html#pyarrow.Schema.from_pandas
        schema = pa.Schema.from_pandas(data, preserve_index=False)
        # print(schema)

        # Convert DataFrame to Parquet format with the specified schema
        table = pa.Table.from_pandas(data, schema=schema)

        # let pyarrow know what our file system is
        # in this case, it's a gcs file system object
        gcs = pa.fs.GcsFileSystem()

        # Write the table to Google Cloud Storage with the specified filename
        with gcs.open_output_stream(file_path) as out:
            # https://arrow.apache.org/docs/python/generated/pyarrow.parquet.write_table.html
            pq.write_table(table, where=out)