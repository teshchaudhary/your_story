import requests
import os
from dotenv import load_dotenv
import json
import time

load_dotenv()

resources_files = {
    "Year_wise_Details_of_Funds_Allocated_by_the_Archaeological_Survey_of_India_(ASI)_for_Cultural_Heritage_Centers_and_other_Places_of_Heritage_Importance_Identified_from_2019-20_to_2022-23": "/resource/03d57ebd-7271-4a37-8204-6309719b8d67", 
    "Inbound Tourism Foreign Tourist Arrivals, Arrivals of Non-Resident Indians and International Tourist Arrivals 1981-2020": "/resource/5015c014-507e-4ddf-8051-2c92dd426d38",
    "Month wise break up of Non Residents Indians arrivals 2018-2020": "/resource/8db754ef-1776-416a-bfbd-bc5696e31492", 
}

for dataset_name, resource in resources_files.items():
    API_KEY = os.getenv("API_KEY")
    base_url = f"https://api.data.gov.in{resource}?api-key={API_KEY}&format=json&limit=100&offset="
    offset=0
    row_exists = True
    dataset = []
    while row_exists:
        url = f"{base_url}{offset}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            records = data.get('records', [])
            count = len(records)
            if count == 0:
                row_exists = False
                continue
            dataset.extend(records)    
            print(f"Fetched {count} records at offset {offset}.")
            offset += 100
        else:
            print(f"Failed to fetch {dataset_name} data: {response.status_code}")
            row_exists = False

    time.sleep(1)    
    os.makedirs(f"data/{dataset_name}/raw", exist_ok=True)

    with open(f"data/{dataset_name}/raw/{dataset_name}.json", "w") as dataset_records:
        json.dump(dataset, dataset_records, indent=4)
    print(f"Dumped {dataset_name} data: {response.status_code}\n")

