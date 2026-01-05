import json
import os
import matplotlib.pyplot as plt

"""
INPUT:
data/processed/institution_weighted_centrality.json

OUTPUT:
data/processed/central_institutions.png
"""

# Project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Input & Output paths
INPUT_PATH = os.path.join(
    BASE_DIR, "data", "processed", "institution_weighted_centrality.json"
)
OUTPUT_PATH = os.path.join(
    BASE_DIR, "data", "processed", "central_institutions.png"
)

# Load data
with open(INPUT_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

labels = [d["institution"] for d in data]
values = [d["weighted_degree"] for d in data]

# Plot
plt.figure(figsize=(10, 6))
plt.barh(labels, values)
plt.xlabel("Weighted Degree Centrality")
plt.title("Top Central Institutions by Collaboration Strength")
plt.gca().invert_yaxis()
plt.tight_layout()

# Save plot
plt.savefig(OUTPUT_PATH)
plt.close()

print("✅ Central institutions plot created")
print("📊 Output saved to:", OUTPUT_PATH)
