import json
import os
from collections import defaultdict

"""
INPUT:
data/processed/final_collaboration_network.json

OUTPUT:
data/processed/institution_weighted_centrality.json
"""

# Project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Input & Output paths
INPUT_PATH = os.path.join(
    BASE_DIR, "data", "processed", "final_collaboration_network.json"
)
OUTPUT_PATH = os.path.join(
    BASE_DIR, "data", "processed", "institution_weighted_centrality.json"
)

# Load final collaboration network
with open(INPUT_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

# Compute weighted degree centrality
weighted_degree = defaultdict(int)

for edge in data:
    inst1 = edge["institution_1"]
    inst2 = edge["institution_2"]
    weight = edge["joint_publications"]

    weighted_degree[inst1] += weight
    weighted_degree[inst2] += weight

# Sort by weighted degree
results = sorted(
    [
        {"institution": inst, "weighted_degree": score}
        for inst, score in weighted_degree.items()
    ],
    key=lambda x: x["weighted_degree"],
    reverse=True
)

# Keep top institutions only
TOP_N = 15
results = results[:TOP_N]

# Save output
with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)

print("✅ Weighted centrality analysis completed")
print("📄 Output saved to:", OUTPUT_PATH)
