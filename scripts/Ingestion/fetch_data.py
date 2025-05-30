import requests
import os
import csv
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()
API_KEY = os.getenv("API_KEY")

if not API_KEY:
    raise ValueError("Missing API_KEY. Please set it in your .env file.")

# Dataset Name -> Resource Path
resources_files = {
    # 1. Tourism Statistics
    "foreign_tourist_arrivals_1981_2020": "/resource/5015c014-507e-4ddf-8051-2c92dd426d38",
    "foreign_tourist_arrivals_2021_2022": "/resource/2063d4c9-4372-49d1-a7cc-c009733d0c7f",
    "domestic_tour_travels_2018_2022": "/resource/bbcf183e-5fb4-4eb0-a9ea-055e5b3cb89d",
    "foreign_exchange_earnings_1991_2020": "/resource/3a71af26-18fd-4038-9972-1f7147ca8a29",
    "foreign_exchange_earnings_2010_2022": "/resource/7675d57c-b057-41c3-84dc-1ee343a590d4",
    "foreign_exchange_earnings_monthly_2022_2024": "/resource/18638069-3d66-463d-b336-fe74e4ac9e92",

    # 2. Cultural & Heritage Sites
    "monuments_under_encroachment": "/resource/a382148f-d172-46b1-9b23-f5c48b6ca3f7",
    "monuments_funding_2016_2021": "/resource/ff3acf06-138b-4978-85d2-46d1a83faf6e",
    "state_fairs_festivals_2014_2021": "/resource/16d88df4-4fb8-4f7d-8198-8eec3eb20925",

    # 3. Supporting & Contextual Data
    "eco_sensitive_zones_2015": "/resource/001baa3b-3c68-4ee5-9eb9-89e0a052beba",
    "eco_sensitive_kailam_villages": "/resource/bca58b01-acfc-4d8a-bf47-720889a6d896",
    "seasonal_temperature_1901_2019": "/resource/e95bbab3-5fdb-4300-b9e8-15a328d90e6d"
}

# Loop through all datasets
for dataset_name, resource_path in resources_files.items():
    print(f"\n📥 Fetching data for: {dataset_name}")
    offset = 0
    limit = 100
    all_records = []
    row_exists = True
    base_url = f"https://api.data.gov.in{resource_path}?api-key={API_KEY}&format=json&limit={limit}&offset="

    while row_exists:
        url = f"{base_url}{offset}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            records = data.get("records", [])
            if not records:
                row_exists = False
                break

            all_records.extend(records)
            print(f"✅ Fetched {len(records)} records at offset {offset}")
            offset += limit
            time.sleep(1)

        except requests.RequestException as e:
            print(f"❌ Error fetching {dataset_name}: {e}")
            break

    if not all_records:
        print(f"⚠️ No records found for {dataset_name}")
        continue

    # Write to CSV
    output_dir = os.path.join("data", "bronze", dataset_name)
    os.makedirs(output_dir, exist_ok=True)
    output_file_path = os.path.join(output_dir, f"{dataset_name}.csv")

    with open(output_file_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=all_records[0].keys())
        writer.writeheader()
        writer.writerows(all_records)

    print(f"💾 Saved {len(all_records)} rows to {output_file_path}")
