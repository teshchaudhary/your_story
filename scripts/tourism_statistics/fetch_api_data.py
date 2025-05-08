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

while flag_fta or flag_nri:

    # Fetching Foreign Tourist Arrivals (FTA) data
    url_fta = f"{url_fta_base}{i_fta}"
    response_fta = requests.get(url_fta)

    # Fetching Non-Resident Indians (NRI) arrivals data
    url_nri = f"{url_nri_base}{i_nri}"
    response_nri = requests.get(url_nri)

    if response_fta.status_code == 200:
        data_fta = response_fta.json()
        count_fta = len(data_fta['records'])

        print(f"Fetched {count_fta} records for FTA.")
        i_fta += 100  # Move to the next batch of records

        if count_fta == 0:
            flag_fta = False  # Exit loop when no more records for FTA

        with open("data/tourism_statistics/raw/fta_data.json", "a") as f_fta:
            json.dump(data_fta, f_fta, indent=4)

    else:
        print(f"Failed to fetch FTA data: {response_fta.status_code}")

    if response_nri.status_code == 200:
        data_nri = response_nri.json()
        count_nri = len(data_nri['records'])

        print(f"Fetched {count_nri} records for NRI.")
        i_nri += 100  # Move to the next batch of records

        if count_nri == 0:
            flag_nri = False  # Exit loop when no more records for NRI

        with open("data/tourism_statistics/raw/nri_data.json", "a") as f_nri:
            json.dump(data_nri, f_nri, indent=4)

    else:
        print(f"Failed to fetch NRI data: {response_nri.status_code}")

    # Wait for 1 second before making the next API call
    time.sleep(1)
