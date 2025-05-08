import requests
import os
from dotenv import load_dotenv
import json
import time

load_dotenv()

API_KEY = os.getenv("DATA_GOV_API_KEY")

# Dataset Resource IDs
RESOURCE_ID_FTA = "/resource/5015c014-507e-4ddf-8051-2c92dd426d38"
RESOURCE_ID_NRI = "/resource/8db754ef-1776-416a-bfbd-bc5696e31492"

# API URLs for both datasets
url_fta_base = f"https://api.data.gov.in{RESOURCE_ID_FTA}?api-key={API_KEY}&format=json&limit=100&offset="
url_nri_base = f"https://api.data.gov.in{RESOURCE_ID_NRI}?api-key={API_KEY}&format=json&limit=100&offset="

i_fta = 0
i_nri = 0
flag_fta = True
flag_nri = True

fta_records = []
nri_records = []

while flag_fta or flag_nri:

    # Fetching FTA data
    if flag_fta:
        url_fta = f"{url_fta_base}{i_fta}"
        response_fta = requests.get(url_fta)

        if response_fta.status_code == 200:
            data_fta = response_fta.json()
            records = data_fta.get('records', [])
            count_fta = len(records)

            print(f"Fetched {count_fta} FTA records at offset {i_fta}.")
            i_fta += 100

            if count_fta == 0:
                flag_fta = False
            else:
                fta_records.extend(records)
        else:
            print(f"Failed to fetch FTA data: {response_fta.status_code}")
            flag_fta = False  # Prevent infinite loop on failure

    # Fetching NRI data
    if flag_nri:
        url_nri = f"{url_nri_base}{i_nri}"
        response_nri = requests.get(url_nri)

        if response_nri.status_code == 200:
            data_nri = response_nri.json()
            records = data_nri.get('records', [])
            count_nri = len(records)

            print(f"Fetched {count_nri} NRI records at offset {i_nri}.")
            i_nri += 100

            if count_nri == 0:
                flag_nri = False
            else:
                nri_records.extend(records)
        else:
            print(f"Failed to fetch NRI data: {response_nri.status_code}")
            flag_nri = False  # Prevent infinite loop on failure

    time.sleep(1)  # Respect rate limits

# Save only the combined records to JSON
os.makedirs("data/tourism_statistics/raw", exist_ok=True)

with open("data/tourism_statistics/raw/fta_data.json", "w") as f_fta:
    json.dump(fta_records, f_fta, indent=4)

with open("data/tourism_statistics/raw/nri_data.json", "w") as f_nri:
    json.dump(nri_records, f_nri, indent=4)

print("Data fetching complete.")
