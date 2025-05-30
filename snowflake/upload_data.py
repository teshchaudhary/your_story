import os
import snowflake.connector
from dotenv import load_dotenv
load_dotenv()

conn = snowflake.connector.connect(
    user=os.getenv('SNOWFLAKE_USER'),
    password=os.getenv('SNOWFLAKE_PASSWORD'),
    account=os.getenv('SNOWFLAKE_ACCOUNT'),
    warehouse=os.getenv('SNOWFLAKE_WAREHOUSE'),
    database=os.getenv('SNOWFLAKE_DATABASE'),
    schema=os.getenv('SNOWFLAKE_SCHEMA'),
    role=os.getenv('SNOWFLAKE_ROLE')
)

def upload_parquet_folder_to_snowflake(base_folder="data/silver"):
    cs = conn.cursor()
    try:
        # List all subfolders (each corresponds to a table)
        for table_name in os.listdir(base_folder):
            table_folder = os.path.join(base_folder, table_name)
            if not os.path.isdir(table_folder):
                continue  # skip files, only folders
                
            print(f"\nUploading parquet files in folder '{table_name}' to Snowflake table '{table_name}'")

            parquet_files = [f for f in os.listdir(table_folder) if f.endswith('.parquet')]
            if not parquet_files:
                print(f"No parquet files found in {table_folder}, skipping.")
                continue

            for file in parquet_files:
                local_file_path = os.path.join(table_folder, file)
                stage_name = f"@%{table_name}"  # table stage for the table

                # PUT file to stage
                put_cmd = f"PUT file://{local_file_path} {stage_name} AUTO_COMPRESS=FALSE"
                print(f"Uploading file {file} to stage {stage_name}...")
                cs.execute(put_cmd)

                # COPY INTO table from stage file
                copy_cmd = f"""
                COPY INTO {table_name}
                FROM {stage_name}/{file}
                FILE_FORMAT = (TYPE = 'PARQUET')
                PURGE = TRUE
                """
                print(f"Loading data from {file} into Snowflake table {table_name}...")
                cs.execute(copy_cmd)

                print(f"✅ Uploaded and loaded file '{file}' into table '{table_name}'")
    finally:
        cs.close()
        conn.close()

# Run upload for all folders in data/silver
upload_parquet_folder_to_snowflake()
