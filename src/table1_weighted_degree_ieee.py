import csv
import json
import os

"""
INPUT:
data/processed/top_institutions_weighted_degree.csv
data/processed/institutions.json

OUTPUT:
data/processed/TABLE_I_weighted_degree_named.csv
"""

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CENTRALITY_PATH = os.path.join(
    BASE_DIR, "data", "processed", "top_institutions_weighted_degree.csv"
)

INSTITUTIONS_PATH = os.path.join(
    BASE_DIR, "data", "processed", "institutions.json"
)

OUTPUT_PATH = os.path.join(
    BASE_DIR, "data", "processed", "TABLE_I_weighted_degree_named.csv"
)

# -------------------------
# Load institution names
# -------------------------
with open(INSTITUTIONS_PATH, "r", encoding="utf-8") as f:
    institutions = json.load(f)

id_to_name = {
    inst["id"]: inst["display_name"]
    for inst in institutions
}

# -------------------------
# Load weighted centrality CSV
# -------------------------
rows = []
with open(CENTRALITY_PATH, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        rows.append(row)

# -------------------------
# Build IEEE-style table
# -------------------------
output_rows = []

for idx, row in enumerate(rows, start=1):
    inst_id = row["institution"]
    inst_name = id_to_name.get(inst_id, "Unknown Institution")

    output_rows.append({
        "Rank": idx,
        "Institution Name": inst_name,
        "Weighted Degree Centrality": row["weighted_degree_centrality"]
    })

# -------------------------
# Write output CSV
# -------------------------
with open(OUTPUT_PATH, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=[
            "Rank",
            "Institution Name",
            "Weighted Degree Centrality"
        ]
    )
    writer.writeheader()
    writer.writerows(output_rows)

print("✅ TABLE I with institution names generated")
print("📄 Saved to:", OUTPUT_PATH)
