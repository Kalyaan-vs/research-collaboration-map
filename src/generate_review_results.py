import json
import os

"""
Generate review-ready results by extracting the
top institutional collaborations based on joint publications.
"""

# Resolve project root directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Input: final merged collaboration network
DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "final_collaboration_network.json"
)

# Output: review-friendly top collaborations
OUTPUT_PATH = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "top_collaborations_review.json"
)

# Load final collaboration data
with open(DATA_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

if not data:
    raise ValueError("Final collaboration dataset is empty.")

# Sort collaborations by strength (descending)
data_sorted = sorted(
    data,
    key=lambda x: x["joint_publications"],
    reverse=True
)

# Select top N collaborations for review
TOP_N = 20
top_results = data_sorted[:TOP_N]

# Save review results
with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(top_results, f, indent=2)

print("✅ Review-ready collaboration results generated")
print(f"📄 Top {TOP_N} collaborations saved to:")
print(OUTPUT_PATH)
