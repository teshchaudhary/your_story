import pandas as pd
import json
import os

def clean_data(raw_data_path, cleaned_data_path, numeric_columns=None):
    """
    Clean the raw data and save the cleaned data to a CSV file.
    
    Parameters:
    - raw_data_path (str): Path to the raw JSON data file.
    - cleaned_data_path (str): Path where the cleaned CSV data should be saved.
    - numeric_columns (list): List of columns that need to be converted to numeric values.
    """
    # Load the raw data
    with open(raw_data_path, 'r') as file:
        raw_data = json.load(file)

    # Check if the data is a list of records or a dictionary with "records"
    if isinstance(raw_data, dict):
        records = raw_data.get("records", [])
    elif isinstance(raw_data, list):
        records = raw_data
    else:
        print(f"Unexpected data format in {raw_data_path}")
        return

    # Prepare the cleaned data
    cleaned_data = []

    for record in records:
        row = {}  # Start with an empty dictionary for each row

        # Extract values for all columns (even if they are missing)
        for key in record.keys():
            row[key] = record.get(key, 0)  # Use 0 for missing values
        
        # Handle 'NA' or invalid values for growth percentages and numeric columns
        for key in numeric_columns:
            if key in row:  # Ensure the column exists before attempting to process it
                if row.get(key) == "NA":
                    row[key] = None
                else:
                    try:
                        row[key] = float(row[key])
                    except (ValueError, TypeError):
                        row[key] = None
            else:
                # If the key is missing, print a message and skip
                print(f"Warning: Key '{key}' not found in the record. Skipping.")
        
        cleaned_data.append(row)
    
    # Convert the cleaned data to a pandas DataFrame
    df = pd.DataFrame(cleaned_data)

    # Print column names after processing
    print("Columns after processing:", df.columns.tolist())

    # Save the cleaned data to a new CSV file
    df.to_csv(cleaned_data_path, index=False)
    print(f"Data cleaned and saved to '{cleaned_data_path}'")

# Define the directory to save the cleaned data
processed_dir = 'data/centrally_protected_monuments/processed'
if not os.path.exists(processed_dir):
    os.makedirs(processed_dir)

# Clean the CPM data with the corrected numeric columns
clean_data(
    raw_data_path='data/centrally_protected_monuments/raw/visitors_to_cpm_1996-2018.json',
    cleaned_data_path=os.path.join(processed_dir, 'visitors_to_cpm_cleaned.csv'),
    numeric_columns=[
        'no__of_visitors___domestic',
        'no__of_visitors___foreign',
        'no__of_visitors___total',
        'annual_growth_rate___domestic',
        'annual_growth_rate___foreign',
        'annual_growth_rate___total'
    ]
)
