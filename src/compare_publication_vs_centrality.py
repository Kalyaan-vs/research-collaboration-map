import json
import pandas as pd
from scipy.stats import spearmanr

# =====================================================
# ABSOLUTE PATH CONFIGURATION
# =====================================================

BASE_PATH = "C:/Python/Major/ResearchColabMap/research-collaboration-map/"

PUBLICATION_FILE = BASE_PATH + "data/processed/true_publication_counts.csv"
CENTRALITY_FILE = BASE_PATH + "data/processed/institution_weighted_degree_centrality.json"
INSTITUTIONS_FILE = BASE_PATH + "data/processed/institutions.json"

OUTPUT_CSV = BASE_PATH + "data/processed/publication_vs_centrality_analysis.csv"
OUTPUT_JSON = BASE_PATH + "data/processed/publication_vs_centrality_analysis.json"

# =====================================================
# LOAD INSTITUTION METADATA (ID → NAME)
# =====================================================

with open(INSTITUTIONS_FILE, "r", encoding="utf-8") as f:
    institutions = json.load(f)

id_to_name = {
    inst_id: inst_data["name"]
    for inst_id, inst_data in institutions.items()
}

print("Loaded institution mappings:", len(id_to_name))

# =====================================================
# LOAD TRUE PUBLICATION COUNTS (ID-BASED)
# =====================================================

pub_df = pd.read_csv(PUBLICATION_FILE)
print("Loaded publication counts:", len(pub_df))

# Map IDs to names
pub_df["institution"] = pub_df["institution_id"].map(id_to_name)

# Drop institutions without name mapping
pub_df = pub_df.dropna(subset=["institution"])

print("Publication records after ID→name mapping:", len(pub_df))

# =====================================================
# LOAD CENTRALITY DATA (NAME-BASED)
# =====================================================

with open(CENTRALITY_FILE, "r", encoding="utf-8") as f:
    centrality_data = json.load(f)

cent_df = pd.DataFrame(centrality_data)
print("Loaded centrality records:", len(cent_df))

# Columns: institution, weighted_degree_centrality

# =====================================================
# NORMALIZE NAMES (IMPORTANT)
# =====================================================

pub_df["institution"] = pub_df["institution"].str.strip().str.lower()
cent_df["institution"] = cent_df["institution"].str.strip().str.lower()

# =====================================================
# MERGE DATASETS (NAME-BASED)
# =====================================================

merged_df = pub_df.merge(
    cent_df,
    on="institution",
    how="inner"
)

print("Merged records:", len(merged_df))

if merged_df.empty:
    raise ValueError("Merge failed — check institution name normalization")

# =====================================================
# SPEARMAN CORRELATION
# =====================================================

corr, p_value = spearmanr(
    merged_df["publication_count"],
    merged_df["weighted_degree_centrality"]
)

print("Spearman correlation:", corr)
print("p-value:", p_value)

# =====================================================
# SURPRISE INDEX
# =====================================================

merged_df["surprise_index"] = (
    merged_df["weighted_degree_centrality"] /
    merged_df["publication_count"]
)

merged_df = merged_df.sort_values(
    by="surprise_index",
    ascending=False
)

# =====================================================
# SAVE RESULTS
# =====================================================

merged_df.to_csv(OUTPUT_CSV, index=False)
merged_df.to_json(OUTPUT_JSON, orient="records", indent=2)

print("Analysis saved successfully")
print("\nTop surprising institutions:")
print(
    merged_df[
        ["institution", "publication_count",
         "weighted_degree_centrality", "surprise_index"]
    ].head(10)
)