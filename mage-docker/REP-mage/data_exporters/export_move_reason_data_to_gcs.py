import pyarrow as pa
import pyarrow.parquet as pq
import os

if "data_exporter" not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = (
    "/home/src/REP_my_creds.json"
)

bucket_name = "rep-bucket1"
project_id = "real-estate-project-430020"

folder_name = "cleansed"

file_name = "move_reason_by_state_weighted.parquet"

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
    
    # Define the schema
    schema = pa.schema([
        ('year_surveyed', pa.int32()),
        ('year_moved', pa.int32()),
        ('move_reason', pa.string()),
        ('state_of_residence', pa.string()),
        ('count', pa.float64())
    ])

    # Convert DataFrame to Parquet format with the specified schema
    table = pa.Table.from_pandas(data, schema=schema)

    # let pyarrow know what our file system is
    # in this case, it's a gcs file system object
    gcs = pa.fs.GcsFileSystem()

    # Write the table to Google Cloud Storage with the specified filename
    with gcs.open_output_stream(file_path) as out:
        # https://arrow.apache.org/docs/python/generated/pyarrow.parquet.write_table.html
        pq.write_table(table, where=out)
