import json
import os
import matplotlib.pyplot as plt

"""
INPUT:
data/processed/top_collaborations_review.json

OUTPUT:
data/processed/top_collaborations.png
"""

# Project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Input & Output paths
INPUT_PATH = os.path.join(
    BASE_DIR, "data", "processed", "top_collaborations_review.json"
)
OUTPUT_PATH = os.path.join(
    BASE_DIR, "data", "processed", "top_collaborations.png"
)

# Load data
with open(INPUT_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

labels = [
    f"{d['institution_1']} ↔ {d['institution_2']}"
    for d in data
]
values = [d["joint_publications"] for d in data]

# Plot
plt.figure(figsize=(10, 6))
plt.barh(labels, values)
plt.xlabel("Joint Publications")
plt.title("Top Institutional Collaborations")
plt.gca().invert_yaxis()
plt.tight_layout()

# Save plot
plt.savefig(OUTPUT_PATH)
plt.close()

print("✅ Top collaborations plot created")
print("📊 Output saved to:", OUTPUT_PATH)
