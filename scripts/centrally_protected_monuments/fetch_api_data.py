import requests
import os
from dotenv import load_dotenv
import json

# Load API key from .env
load_dotenv()
API_KEY = os.getenv("DATA_GOV_API_KEY")

# Resource ID for the dataset
RESOURCE_ID = "/resource/62498cb9-f17e-4afd-ad4e-b2d6c8ff0768"

# Initialize
i = 0
flag = True
all_records = []

# Create destination directory if not exists
output_path = "data/centrally_protected_monuments/raw"
os.makedirs(output_path, exist_ok=True)

# Fetch paginated data
while flag:
    url = f"https://api.data.gov.in{RESOURCE_ID}?api-key={API_KEY}&format=json&limit=100&offset={i}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        records = data.get('records', [])
        count = len(records)

        print(f"Fetched {count} records at offset {i}.")
        i += 100

        if count == 0:
            flag = False
        else:
            all_records.extend(records)

    else:
        print(f"Failed to fetch data: {response.status_code}")
        break

# Save the complete records list
output_file = os.path.join(output_path, "visitors_to_cpm_1996-2018.json")
with open(output_file, "w") as f:
    json.dump(all_records, f, indent=4)

print(f"\nSaved {len(all_records)} records to '{output_file}'")
