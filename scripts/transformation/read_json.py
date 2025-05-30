import json
import pandas as pd
import os
import hashlib

dfs_dict = {}
root_dir = "data"
# Walk through all directories and files under root_dir
for dirpath, dirnames, filenames in os.walk(root_dir):
    for filename in filenames:
        if filename.lower().endswith(".json"):
            full_path = os.path.join(dirpath, filename)
            try:
                with open(full_path, "r") as f:
                    content = json.load(f)

                    # Create DataFrame
                    if isinstance(content, list):
                        df = pd.DataFrame(content)
                    elif isinstance(content, dict):
                        df = pd.DataFrame([content])
                    else:
                        print(f"Unsupported format: {full_path}")
                        continue

                    # Optional: create a unique key using relative path
                    rel_path_key = os.path.relpath(full_path, root_dir).replace(os.sep, "_").replace(".json", "")
                    dfs_dict[rel_path_key] = df

            except Exception as e:
                print(f"Error processing {full_path}: {e}")


# Example: Access individual DataFrame
for key, df in dfs_dict.items():
    print(f"\nDataFrame for '{key}':")
    # print(df.head())
print(dfs_dict['Inbound Tourism Foreign Tourist Arrivals, Arrivals of Non-Resident Indians and International Tourist Arrivals 1981-2020_raw_Inbound Tourism Foreign Tourist Arrivals, Arrivals of Non-Resident Indians and International Tourist Arrivals 1981-2020'].head())

output_dir = "local_output"
os.makedirs(output_dir, exist_ok=True)

for table_name, df in dfs_dict.items():
    clean_name = table_name.lower().replace("-", "_").replace(" ", "_")

    short_hash = hashlib.md5(clean_name.encode()).hexdigest()
    clean_name = clean_name[:80] + "_" + short_hash[:8]

    output_path = os.path.join(output_dir, f"{clean_name}.csv")

    df.to_csv(output_path, index=False)
    print(f"✅ Saved: {output_path}")