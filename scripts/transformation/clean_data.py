import os
import json
import pandas as pd
import numpy as np
import hashlib

root_dir = 'data/bronze'
dfs_dict = {}

for dirpath, dirnames, filenames in os.walk(root_dir):
    for filename in filenames:
        if filename.lower().endswith(".json"):
            full_path = os.path.join(dirpath, filename)
            try:
                with open(full_path, "r") as f:
                    content = json.load(f)

                    if isinstance(content, list):
                        df = pd.DataFrame(content)
                    elif isinstance(content, dict):
                        df = pd.DataFrame([content])
                    else:
                        print(f"Unsupported format: {full_path}")
                        continue

                    rel_path_key = os.path.relpath(full_path, root_dir).replace(os.sep, "_").replace(".json", "")
                    dfs_dict[rel_path_key] = df

            except Exception as e:
                print(f"Error processing {full_path}: {e}")

output_dir = "local_output/bronze/"
os.makedirs(output_dir, exist_ok=True)

for table_name, df in dfs_dict.items():
    clean_name = table_name.lower().replace("-", "_").replace(" ", "_")

    short_hash = hashlib.md5(clean_name.encode()).hexdigest()
    clean_name = clean_name[:80] + "_" + short_hash[:8]

    output_path = os.path.join(output_dir, f"{clean_name}.csv")

    df.to_csv(output_path, index=False)
    print(f"✅ Saved: {output_path}")                

row_wise_normailze = []
def transform_dataframe(df, fill_median_axis='column'):
    """
    Transform a DataFrame:
    - Replaces common missing values
    - Drops all-NaN columns
    - Fills remaining NaNs with row-wise or column-wise median
    Args:
        df (pd.DataFrame): Input dataframe
        fill_median_axis (str): 'column' or 'row' for median fill direction
    Returns:
        pd.DataFrame: Cleaned dataframe
    """

    df = df.applymap(lambda x: str(x).strip() if pd.notnull(x) else x)

    df.replace(["NA", "na", "Na", "N/A", "null", "Null", "none", "None", ""], np.nan, inplace=True)

    df.dropna(axis=1, how='all', inplace=True)

    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='ignore')

    if fill_median_axis == 'column':
        for col in df.select_dtypes(include=[np.number]).columns:
            if df[col].isnull().any():
                df[col].fillna(df[col].median(), inplace=True)
    elif fill_median_axis == 'row':
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for index, row in df[numeric_cols].iterrows():
            row_median = row.median(skipna=True)
            df.loc[index, numeric_cols] = row.fillna(row_median)
    else:
        raise ValueError("fill_median_axis must be either 'row' or 'column'")

    return df    

df_dict_transformed = {}
for name, df in dfs_dict.items():
    if name in row_wise_normailze:
        df_dict_transformed[name] = transform_dataframe(df.copy(), fill_median_axis='row')
    else:
        df_dict_transformed[name] = transform_dataframe(df.copy(), fill_median_axis='column')

output_dir = "local_output/silver/"
os.makedirs(output_dir, exist_ok=True)

for table_name, df in df_dict_transformed.items():
    clean_name = table_name.lower().replace("-", "_").replace(" ", "_")

    short_hash = hashlib.md5(clean_name.encode()).hexdigest()
    clean_name = clean_name[:80] + "_" + short_hash[:8]

    output_path = os.path.join(output_dir, f"{clean_name}.csv")

    df.to_csv(output_path, index=False)
    print(f"✅ Saved: {output_path}")

output_base_folder = "data/silver"
os.makedirs(output_base_folder, exist_ok=True)

for name, df in df_dict_transformed.items():
    # Clean the dataframe name for folder and file usage
    clean_name = name.lower().replace("-", "_").replace(" ", "_")
    # Hash the cleaned name to ensure uniqueness & limit length
    short_hash = hashlib.md5(clean_name.encode()).hexdigest()[:8]
    # Limit length and append hash
    folder_name = clean_name[:80] + "_" + short_hash
    
    # Create subfolder for this dataframe
    output_folder = os.path.join(output_base_folder, folder_name)
    os.makedirs(output_folder, exist_ok=True)
    
    # Save parquet file inside this subfolder, named the same
    file_path = os.path.join(output_folder, f"{folder_name}.parquet")
    df.to_parquet(file_path, index=False)
    
    print(f"✅ Saved dataframe '{name}' to '{file_path}'")
