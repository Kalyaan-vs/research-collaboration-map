import json
import os
from collections import defaultdict

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "final_collaboration_network.json"
)

OUTPUT_PATH = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "institution_centrality.json"
)

# Load final collaboration network
with open(DATA_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

# Compute degree centrality
degree = defaultdict(int)

for edge in data:
    inst1 = edge["institution_1"]
    inst2 = edge["institution_2"]

    degree[inst1] += 1
    degree[inst2] += 1

# Convert to sorted list
centrality_results = sorted(
    [
        {
            "institution": inst,
            "degree_centrality": count
        }
        for inst, count in degree.items()
    ],
    key=lambda x: x["degree_centrality"],
    reverse=True
)

# Take top institutions only (paper-ready)
TOP_N = 15
centrality_results = centrality_results[:TOP_N]

# Save results
with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(centrality_results, f, indent=2)

print("Institution centrality analysis completed")
print(f"Top {TOP_N} central institutions saved to:")
print(OUTPUT_PATH)
