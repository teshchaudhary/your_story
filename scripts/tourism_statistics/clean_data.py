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

    # Extract relevant records
    records = raw_data


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
processed_dir = 'data/tourism_statistics/processed'
if not os.path.exists(processed_dir):
    os.makedirs(processed_dir)

# Clean the FTA data
clean_data(
    raw_data_path='data/tourism_statistics/raw/fta_data.json',
    cleaned_data_path=os.path.join(processed_dir, 'fta_data_cleaned.csv'),
    numeric_columns=[
        'ftas_in_india_in_million_',
        'percentage_change_over_previous_year',
        'nris_arrivals_in_india_in_million_',
        'ercentage_change_over_the_previous_year',
        'international_tourist_arrivals_in_india_in_million_',
        'percentage_change_over_the_previous_year'
    ]
)


# Clean the NRI data
clean_data(
    raw_data_path='data/tourism_statistics/raw/nri_data.json',
    cleaned_data_path=os.path.join(processed_dir, 'nri_data_cleaned.csv'),
    numeric_columns=[
        '_2018',
        '_2019',
        '_2020',
        'growth_2019_18_',
        'growth_2020_19_'
    ]
)
