import csv
import json
import os

"""
IEEE TABLE II
Comparison of Publication Count and Collaboration Centrality

INPUT:
data/processed/publication_vs_collaboration.csv
data/processed/institutions.json

OUTPUT:
data/processed/TABLE_II_pub_vs_collab_ieee.csv
"""

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

COMPARISON_PATH = os.path.join(
    BASE_DIR, "data", "processed", "publication_vs_collaboration.csv"
)

INSTITUTIONS_PATH = os.path.join(
    BASE_DIR, "data", "processed", "institutions.json"
)

OUTPUT_PATH = os.path.join(
    BASE_DIR, "data", "processed", "TABLE_II_pub_vs_collab_ieee.csv"
)

# --------------------------------------------------
# Load institutions metadata (robust)
# --------------------------------------------------
with open(INSTITUTIONS_PATH, "r", encoding="utf-8") as f:
    institutions = json.load(f)

# Build ID -> Name mapping
if isinstance(institutions, dict):
    id_to_name = {
        inst_id: inst_data.get("display_name", inst_id)
        for inst_id, inst_data in institutions.items()
    }
else:
    id_to_name = {
        inst["id"]: inst["display_name"]
        for inst in institutions
    }

# --------------------------------------------------
# Load comparison CSV
# --------------------------------------------------
with open(COMPARISON_PATH, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    rows = list(reader)

if not rows:
    raise ValueError("publication_vs_collaboration.csv is empty")

# --------------------------------------------------
# Prepare percentile classification
# --------------------------------------------------
pub_values = [int(r["total_publications"]) for r in rows]
cent_values = [int(r["weighted_degree_centrality"]) for r in rows]

def percentile_classify(values, value):
    sorted_vals = sorted(values)
    n = len(sorted_vals)

    if n == 0:
        return "Low"

    rank = sorted_vals.index(value) / n

    if rank >= 0.66:
        return "High"
    elif rank >= 0.33:
        return "Medium"
    else:
        return "Low"

# --------------------------------------------------
# Build IEEE Table II (TOP 10)
# --------------------------------------------------
output_rows = []

for row in rows[:10]:
    inst_raw = row["institution"]

    # ✅ FINAL FIX: resolve name correctly
    if inst_raw.startswith("https://openalex.org/"):
        institution_name = id_to_name.get(inst_raw, "Unknown Institution")
    else:
        institution_name = inst_raw

    output_rows.append({
        "Institution Name": institution_name,
        "Publication Count": percentile_classify(
            pub_values, int(row["total_publications"])
        ),
        "Weighted Degree Centrality": percentile_classify(
            cent_values, int(row["weighted_degree_centrality"])
        )
    })

# --------------------------------------------------
# Write IEEE CSV
# --------------------------------------------------
with open(OUTPUT_PATH, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=[
            "Institution Name",
            "Publication Count",
            "Weighted Degree Centrality"
        ]
    )
    writer.writeheader()
    writer.writerows(output_rows)

print("✅ IEEE TABLE II generated successfully")
print("📄 Saved at:", OUTPUT_PATH)
