import pyarrow as pa
import pyarrow.parquet as pq
import os

if "data_exporter" not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/src/REP_my_creds.json"

bucket_name = "rep-bucket1"
project_id = "real-estate-project-430020"

folder_name = "cleansed"

file_name = "realtor_residential_data_msa_level.parquet"

file_path = f"{bucket_name}/{folder_name}/{file_name}"


@data_exporter
def export_data(data, *args, **kwargs):
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

    # What is a schema?
    # A named collection of types a.k.a schema.
    # A schema defines the column names and types in a record batch or table data structure.
    # They also contain metadata about the columns.

    # Define the schema
    # schema = pa.schema(
    #     [
    #         # ('name', pa.string()),
    #         # ('month_of_measurement', pa.string()),
    #         # ('unemployment_rate', pa.float64())
    #     ]
    # )

    # or infer the schema with pa.Schema.from_pandas method
    # https://arrow.apache.org/docs/python/generated/pyarrow.Schema.html#pyarrow.Schema.from_pandas
    schema = pa.Schema.from_pandas(data, preserve_index=False)
    print(schema)

    # Convert DataFrame to Parquet format with the specified schema
    table = pa.Table.from_pandas(data, schema=schema)

    # let pyarrow know what our file system is
    # in this case, it's a gcs file system object
    gcs = pa.fs.GcsFileSystem()

    # Write the table to Google Cloud Storage with the specified filename
    with gcs.open_output_stream(file_path) as out:
        # https://arrow.apache.org/docs/python/generated/pyarrow.parquet.write_table.html
        pq.write_table(table, where=out)
