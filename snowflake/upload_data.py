import os
import hashlib
import snowflake.connector
import sys
from dotenv import load_dotenv
import pyarrow.parquet as pq

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.snowflake_config import *
load_dotenv()

conn = snowflake.connector.connect(
    user=SNOWFLAKE_USER,
    password=SNOWFLAKE_PASSWORD,
    account=SNOWFLAKE_ACCOUNT,
    warehouse=SNOWFLAKE_WAREHOUSE,
    database=SNOWFLAKE_DATABASE,
    schema=SNOWFLAKE_SCHEMA,
    role=SNOWFLAKE_ROLE
)
cursor = conn.cursor()

def sanitize_table_name(name):
    name = name.lower().replace(" ", "_").replace("-", "_").replace(",", "_")
    short_hash = hashlib.md5(name.encode()).hexdigest()[:8]
    return f"{name[:72]}_{short_hash}"

def map_dtype_arrow_to_snowflake(pa_type):
    pa_type = str(pa_type).lower()
    if "int" in pa_type:
        return "NUMBER"
    elif "float" in pa_type or "double" in pa_type:
        return "FLOAT"
    elif "string" in pa_type or "binary" in pa_type or "largeutf8" in pa_type:
        return "STRING"
    elif "timestamp" in pa_type:
        return "TIMESTAMP_NTZ"
    elif "bool" in pa_type or "boolean" in pa_type:
        return "BOOLEAN"
    else:
        return "STRING"

def create_table_from_parquet(cursor, table_name, parquet_file_path):
    table_name_clean = table_name.lower()
    parquet_schema = pq.read_schema(parquet_file_path)

    column_defs = ",\n    ".join([
        f'"{field.name}" {map_dtype_arrow_to_snowflake(field.type)}'
        for field in parquet_schema
    ])

    create_stmt = f"""
    CREATE TABLE IF NOT EXISTS "{table_name_clean}" (
        {column_defs}
    );
    """
    print(f"🛠️ Creating table if not exists: {table_name_clean}")
    cursor.execute(create_stmt)

def upload_parquet_to_snowflake(base_folder="data/silver"):
    try:
        for original_table_name in os.listdir(base_folder):
            table_path = os.path.join(base_folder, original_table_name)
            if not os.path.isdir(table_path):
                continue

            sanitized_table = sanitize_table_name(original_table_name)
            parquet_files = [f for f in os.listdir(table_path) if f.endswith('.parquet')]
            if not parquet_files:
                print(f"❌ No parquet files in {table_path}, skipping.")
                continue

            for file in parquet_files:
                local_file_path = os.path.abspath(os.path.join(table_path, file))

                # Create table based on parquet schema
                create_table_from_parquet(cursor, sanitized_table, local_file_path)

                # Create a temporary stage
                stage_name = f"staging_{sanitized_table}"
                cursor.execute(f"CREATE OR REPLACE TEMPORARY STAGE {stage_name}")
                stage_path = f"@{stage_name}"

                # PUT command to upload parquet to stage
                put_command = f"PUT 'file://{local_file_path}' {stage_path} AUTO_COMPRESS=TRUE"
                print(f"🔼 PUT: {put_command}")
                cursor.execute(put_command)

                # COPY INTO command
                copy_command = f"""
                    COPY INTO "{sanitized_table}"
                    FROM {stage_path}
                    FILE_FORMAT = (TYPE = PARQUET)
                    MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE
                    PURGE = TRUE
                """
                print(f"📥 COPY INTO: {copy_command.strip()}")
                cursor.execute(copy_command)

                print(f"✅ Loaded '{file}' into Snowflake table '{sanitized_table}'")
    finally:
        cursor.close()
        conn.close()

upload_parquet_to_snowflake()
