import json
import os
from itertools import combinations
from collections import defaultdict

# Resolve project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INPUT_PATH = os.path.join(BASE_DIR, "data", "processed", "works_institutions.json")
OUTPUT_DIR = os.path.join(BASE_DIR, "data", "processed")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load extracted institution data
with open(INPUT_PATH, "r", encoding="utf-8") as f:
    works = json.load(f)

collaboration_counts = defaultdict(int)

for work in works:
    institutions = work.get("institutions", [])

    # Only papers with >=2 institutions form collaborations
    if len(institutions) >= 2:
        for pair in combinations(sorted(institutions), 2):
            collaboration_counts[pair] += 1

# Convert to list
collaborations = [
    {
        "institution_1": pair[0],
        "institution_2": pair[1],
        "joint_publications": count
    }
    for pair, count in collaboration_counts.items()
]

# Save collaboration graph
output_path = os.path.join(OUTPUT_DIR, "collaborations.json")
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(collaborations, f, indent=2)

print("Total collaboration links:", len(collaborations))
print("Saved to:", output_path)
