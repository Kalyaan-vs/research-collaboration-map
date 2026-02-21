import json
import pandas as pd
from collections import defaultdict

# =====================================================
# ABSOLUTE PATH CONFIGURATION
# =====================================================

BASE_PATH = "C:/Python/Major/ResearchColabMap/research-collaboration-map/"

WORKS_FILE = BASE_PATH + "data/raw/works.json"
INSTITUTIONS_FILE = BASE_PATH + "data/processed/institutions.json"

OUTPUT_CSV = BASE_PATH + "data/processed/true_publication_counts.csv"
OUTPUT_JSON = BASE_PATH + "data/processed/true_publication_counts.json"

# =====================================================
# LOAD INSTITUTION METADATA
# =====================================================

with open(INSTITUTIONS_FILE, "r", encoding="utf-8") as f:
    institutions = json.load(f)

valid_institution_ids = set(institutions.keys())
print("Loaded institutions:", len(valid_institution_ids))

# =====================================================
# LOAD OPENALEX WORKS (API FORMAT)
# =====================================================

with open(WORKS_FILE, "r", encoding="utf-8") as f:
    works_data = json.load(f)

# IMPORTANT FIX: actual works are inside "results"
works = works_data.get("results", [])
print("Loaded works:", len(works))

if not works:
    raise ValueError("No works found in OpenAlex JSON (results is empty)")

# =====================================================
# COMPUTE TRUE PUBLICATION COUNTS
# =====================================================
# Count each institution ONCE per work

publication_count = defaultdict(int)

for work in works:
    seen_institutions = set()

    authorships = work.get("authorships", [])
    for author in authorships:
        for inst in author.get("institutions", []):
            inst_id = inst.get("id")
            if inst_id and inst_id in valid_institution_ids:
                seen_institutions.add(inst_id)

    for inst_id in seen_institutions:
        publication_count[inst_id] += 1

print("Computed publication counts for institutions:", len(publication_count))

# =====================================================
# SAVE RESULTS
# =====================================================

pub_df = pd.DataFrame(
    publication_count.items(),
    columns=["institution_id", "publication_count"]
).sort_values(
    by="publication_count",
    ascending=False
)

pub_df.to_csv(OUTPUT_CSV, index=False)
pub_df.to_json(OUTPUT_JSON, orient="records", indent=2)

print("True publication counts saved successfully")
print(pub_df.head(10))