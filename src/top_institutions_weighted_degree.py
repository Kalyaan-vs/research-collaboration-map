import json
import os
from collections import defaultdict

"""
INPUT:
data/processed/final_collaboration_network.json

OUTPUT:
data/processed/top_institutions_weighted_degree.json
"""

# Get project root directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Input file (final collaboration edges)
INPUT_PATH = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "final_collaboration_network.json"
)

# Output file (ranked institutions)
OUTPUT_PATH = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "top_institutions_weighted_degree.json"
)

# Load collaboration data
with open(INPUT_PATH, "r", encoding="utf-8") as f:
    collaborations = json.load(f)

# Calculate weighted degree centrality
weighted_degree = defaultdict(int)

for edge in collaborations:
    inst1 = edge["institution_1"]
    inst2 = edge["institution_2"]
    weight = edge["joint_publications"]

    weighted_degree[inst1] += weight
    weighted_degree[inst2] += weight

# Rank institutions by weighted degree
ranked_institutions = sorted(
    [
        {
            "institution": inst,
            "weighted_degree_centrality": score
        }
        for inst, score in weighted_degree.items()
    ],
    key=lambda x: x["weighted_degree_centrality"],
    reverse=True
)

# Keep top N institutions
TOP_N = 20
ranked_institutions = ranked_institutions[:TOP_N]

# Save results
with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(ranked_institutions, f, indent=2)

print("✅ Top institutions ranked by weighted degree centrality generated")
print(f"📄 Output saved to: {OUTPUT_PATH}")
