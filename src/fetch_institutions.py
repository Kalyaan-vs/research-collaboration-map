import json
import os
import requests
import time

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COLLAB_PATH = os.path.join(BASE_DIR, "data", "processed", "collaborations.json")
OUTPUT_PATH = os.path.join(BASE_DIR, "data", "processed", "institutions.json")

HEADERS = {
    "User-Agent": "ResearchCollaborationMap/1.0 (academic project)"
}

TIMEOUT = 10
RETRY_DELAY = 2
MAX_RETRIES = 3

with open(COLLAB_PATH, "r", encoding="utf-8") as f:
    collaborations = json.load(f)

institution_ids = sorted(
    {c["institution_1"] for c in collaborations}
    | {c["institution_2"] for c in collaborations}
)

print("Fetching metadata for", len(institution_ids), "institutions")

institutions = {}

def fetch_institution(inst_id):
    url = f"https://api.openalex.org/institutions/{inst_id}"
    for attempt in range(MAX_RETRIES):
        try:
            r = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
            if r.status_code == 200:
                return r.json()
            else:
                print(f"HTTP {r.status_code} for {inst_id}")
        except requests.exceptions.RequestException:
            print(f"Retry {attempt+1} for {inst_id}")
            time.sleep(RETRY_DELAY)
    return None

for inst_id in institution_ids:
    data = fetch_institution(inst_id)
    if data:
        institutions[inst_id] = {
            "id": inst_id,
            "name": data.get("display_name"),
            "country": data.get("country_code"),
            "latitude": data.get("geo", {}).get("latitude"),
            "longitude": data.get("geo", {}).get("longitude")
        }
    time.sleep(0.3)  # polite delay

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(institutions, f, indent=2)

print("Saved institution metadata for", len(institutions), "institutions")
