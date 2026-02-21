import json
import networkx as nx
import pandas as pd

# =====================================================
# ABSOLUTE PATH CONFIGURATION (EDIT ONLY IF FOLDER MOVES)
# =====================================================

BASE_PATH = "C:/Python/Major/ResearchColabMap/research-collaboration-map/data/processed/"

INPUT_JSON = BASE_PATH + "final_collaboration_network.json"

# Output files
WD_CSV = BASE_PATH + "institution_weighted_degree_centrality.csv"
WD_JSON = BASE_PATH + "institution_weighted_degree_centrality.json"

BET_CSV = BASE_PATH + "institution_betweenness_centrality.csv"
BET_JSON = BASE_PATH + "institution_betweenness_centrality.json"

COMM_CSV = BASE_PATH + "institution_communities.csv"
COMM_JSON = BASE_PATH + "institution_communities.json"

# =====================================================
# Load Collaboration Graph
# =====================================================

with open(INPUT_JSON, "r", encoding="utf-8") as f:
    edges = json.load(f)   # list of collaboration records

G = nx.Graph()

for edge in edges:
    inst1 = edge["institution_1"]
    inst2 = edge["institution_2"]
    weight = edge.get("joint_publications", 1)

    G.add_edge(inst1, inst2, weight=weight)

print("Graph loaded successfully")
print("Institutions:", G.number_of_nodes())
print("Collaborations:", G.number_of_edges())

# =====================================================
# Weighted Degree Centrality
# =====================================================

weighted_degree = {
    node: G.degree(node, weight="weight")
    for node in G.nodes()
}

wd_df = pd.DataFrame(
    weighted_degree.items(),
    columns=["institution", "weighted_degree_centrality"]
).sort_values(
    by="weighted_degree_centrality",
    ascending=False
)

wd_df.to_csv(WD_CSV, index=False)
wd_df.to_json(WD_JSON, orient="records", indent=2)

print("Weighted degree centrality computed and saved")

# =====================================================
# Betweenness Centrality
# =====================================================

betweenness = nx.betweenness_centrality(
    G,
    weight="weight",
    normalized=True
)

bet_df = pd.DataFrame(
    betweenness.items(),
    columns=["institution", "betweenness_centrality"]
).sort_values(
    by="betweenness_centrality",
    ascending=False
)

bet_df.to_csv(BET_CSV, index=False)
bet_df.to_json(BET_JSON, orient="records", indent=2)

print("Betweenness centrality computed and saved")

# =====================================================
# Filter Weak Edges (For Fast & Meaningful Communities)
# =====================================================

G_filtered = nx.Graph()

for u, v, d in G.edges(data=True):
    if d["weight"] >= 2:   # meaningful collaborations only
        G_filtered.add_edge(u, v, weight=d["weight"])

print("Filtered graph created")
print("Filtered Institutions:", G_filtered.number_of_nodes())
print("Filtered Collaborations:", G_filtered.number_of_edges())

# =====================================================
# Community Detection (Louvain)
# =====================================================

import community as community_louvain

communities = community_louvain.best_partition(
    G_filtered,
    weight="weight"
)

community_df = pd.DataFrame(
    communities.items(),
    columns=["institution", "community_id"]
)

community_df.to_csv(COMM_CSV, index=False)
community_df.to_json(COMM_JSON, orient="records", indent=2)

print("Community detection completed")
print("Number of communities:", community_df["community_id"].nunique())

print(
    community_df.groupby("community_id")
    .size()
    .sort_values(ascending=False)
    .head(5)
)