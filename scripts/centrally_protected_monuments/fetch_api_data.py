import requests
import os
from dotenv import load_dotenv
import json

load_dotenv()

API_KEY = os.getenv("DATA_GOV_API_KEY")

RESOURCE_ID = "/resource/62498cb9-f17e-4afd-ad4e-b2d6c8ff0768"

i = 0
flag = True
while flag:

    url = f"https://api.data.gov.in{RESOURCE_ID}?api-key={API_KEY}&format=json&limit=100&offset={i}"

    response = requests.get(url)


    if response.status_code == 200:
        data = response.json()
        count = len(data['records'])

        print(f"Fetched {count} records.")
        i += 1
        if count == 0:
            flag = False

        with open("data/centrally_protected_monuments/raw/visitors_to_cpm_1996-2018.json", "a") as f:
            json.dump(data, f, indent=4)

    else:
        print(f"Failed to fetch FTA data: {response.status_code}")
