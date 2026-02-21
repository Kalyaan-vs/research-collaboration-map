import json
import os
import csv
from collections import defaultdict

"""
INPUT:
data/processed/final_collaboration_network.json

OUTPUT:
data/processed/top_institutions_weighted_degree.csv
"""

# Project root directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Input and output paths
INPUT_PATH = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "final_collaboration_network.json"
)

OUTPUT_PATH = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "top_institutions_weighted_degree.csv"
)

# Load collaboration network
with open(INPUT_PATH, "r", encoding="utf-8") as f:
    collaborations = json.load(f)

# Compute weighted degree centrality
weighted_degree = defaultdict(int)

for edge in collaborations:
    inst1 = edge["institution_1"]
    inst2 = edge["institution_2"]
    weight = edge["joint_publications"]

    weighted_degree[inst1] += weight
    weighted_degree[inst2] += weight

# Rank institutions
ranked = sorted(
    weighted_degree.items(),
    key=lambda x: x[1],
    reverse=True
)

# Limit to top N
TOP_N = 20
ranked = ranked[:TOP_N]

# Write CSV
with open(OUTPUT_PATH, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["rank", "institution", "weighted_degree_centrality"])

    for idx, (inst, score) in enumerate(ranked, start=1):
        writer.writerow([idx, inst, score])

print("✅ CSV table generated successfully")
print(f"📄 File saved at: {OUTPUT_PATH}")
