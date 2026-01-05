import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

RAW_PATH = os.path.join(BASE_DIR, "data", "raw", "works.json")
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
os.makedirs(PROCESSED_DIR, exist_ok=True)

with open(RAW_PATH, "r", encoding="utf-8") as f:
    works = json.load(f)["results"]

extracted = []

for work in works:
    institutions = set()
    for author in work.get("authorships", []):
        for inst in author.get("institutions", []):
            if inst.get("id"):
                institutions.add(inst["id"])

    extracted.append({
        "work_id": work.get("id"),
        "year": work.get("publication_year"),
        "institutions": list(institutions)
    })

output_file = os.path.join(PROCESSED_DIR, "works_institutions.json")
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(extracted, f, indent=2)

print("Saved processed data to:", output_file)
