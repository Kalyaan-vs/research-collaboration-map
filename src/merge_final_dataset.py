import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

COLLAB_PATH = os.path.join(BASE_DIR, "data", "processed", "collaborations.json")
INST_PATH = os.path.join(BASE_DIR, "data", "processed", "institutions.json")
OUTPUT_PATH = os.path.join(BASE_DIR, "data", "processed", "final_collaboration_network.json")

with open(COLLAB_PATH, "r", encoding="utf-8") as f:
    collaborations = json.load(f)

with open(INST_PATH, "r", encoding="utf-8") as f:
    institutions = json.load(f)

final_data = []

for c in collaborations:
    i1 = institutions.get(c["institution_1"])
    i2 = institutions.get(c["institution_2"])

    if not i1 or not i2:
        continue

    final_data.append({
        "institution_1": i1["name"],
        "country_1": i1["country"],
        "lat_1": i1["latitude"],
        "lon_1": i1["longitude"],
        "institution_2": i2["name"],
        "country_2": i2["country"],
        "lat_2": i2["latitude"],
        "lon_2": i2["longitude"],
        "joint_publications": c["joint_publications"]
    })

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(final_data, f, indent=2)

print("Final collaboration dataset created with", len(final_data), "edges")
print("Saved to:", OUTPUT_PATH)
