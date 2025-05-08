import requests
import os
from dotenv import load_dotenv
import json

load_dotenv()

API_KEY = os.getenv("DATA_GOV_API_KEY")

# Dataset Resource IDs
RESOURCE_ID_FTA = "/resource/5015c014-507e-4ddf-8051-2c92dd426d38"
RESOURCE_ID_NRI = "/resource/8db754ef-1776-416a-bfbd-bc5696e31492"

# API URLs for both datasets
url_fta = f"https://api.data.gov.in{RESOURCE_ID_FTA}?api-key={API_KEY}&format=json&limit=100"
url_nri = f"https://api.data.gov.in{RESOURCE_ID_NRI}?api-key={API_KEY}&format=json&limit=100"

# Fetching Foreign Tourist Arrivals (FTA) data
response_fta = requests.get(url_fta)

# Fetching Non-Resident Indians (NRI) arrivals data
response_nri = requests.get(url_nri)

# Check if both requests were successful
if response_fta.status_code == 200 and response_nri.status_code == 200:
    data_fta = response_fta.json()
    data_nri = response_nri.json()

    # Print the number of records fetched
    print(f"Fetched {len(data_fta['records'])} records for FTA.")
    print(f"Fetched {len(data_nri['records'])} records for NRI.")

    # Save data to JSON files
    with open("data/raw/fta_data.json", "w") as f_fta:
        json.dump(data_fta, f_fta, indent=4)

    with open("data/raw/nri_data.json", "w") as f_nri:
        json.dump(data_nri, f_nri, indent=4)

else:
    print(f"Failed to fetch FTA data: {response_fta.status_code}")
    print(f"Failed to fetch NRI data: {response_nri.status_code}")
