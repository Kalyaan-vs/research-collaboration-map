import requests
import json
import os

# Get absolute path of project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Data directory outside src
RAW_DATA_DIR = os.path.join(BASE_DIR, "data", "raw")
os.makedirs(RAW_DATA_DIR, exist_ok=True)

# OpenAlex Works API
URL = "https://api.openalex.org/works"

PARAMS = {
    "filter": "publication_year:2022,authorships.institutions.country_code:IN",
    "per-page": 200
}

response = requests.get(URL, params=PARAMS)
response.raise_for_status()

data = response.json()

# Save file to project-level data folder
output_path = os.path.join(RAW_DATA_DIR, "works.json")
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print("Fetched", len(data["results"]), "works")
print("Saved to:", output_path)
