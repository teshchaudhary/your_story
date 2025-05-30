import os
import pandas as pd
import numpy as np
import hashlib

root_dir = 'data/bronze'
dfs_dict = {}

# Step 1: Read all CSVs under the bronze directory
for dirpath, dirnames, filenames in os.walk(root_dir):
    for filename in filenames:
        if filename.lower().endswith(".csv"):
            full_path = os.path.join(dirpath, filename)
            try:
                df = pd.read_csv(full_path)

                file_stem = os.path.splitext(filename)[0]
                dfs_dict[file_stem] = df

            except Exception as e:
                print(f"Error processing {full_path}: {e}")

# Step 2: Clean and transform data
row_wise_normailze = []

def transform_dataframe(df, fill_median_axis='column'):
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

# Step 3: Save cleaned data as Parquet under data/silver/
output_base_folder = "data/silver"
os.makedirs(output_base_folder, exist_ok=True)

for name, df in df_dict_transformed.items():
    clean_name = name.lower().replace("-", "_").replace(" ", "_")
    short_hash = hashlib.md5(clean_name.encode()).hexdigest()[:8]
    folder_name = clean_name[:80] + "_" + short_hash

    output_folder = os.path.join(output_base_folder, folder_name)
    os.makedirs(output_folder, exist_ok=True)

    file_path = os.path.join(output_folder, f"{folder_name}.parquet")
    df.to_parquet(file_path, index=False)
    print(f"✅ Saved dataframe '{name}' to '{file_path}'")
