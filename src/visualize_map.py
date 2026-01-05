import json
import os
import networkx as nx
from pyvis.network import Network

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "final_collaboration_network.json"
)

# Load data
with open(DATA_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

# 🔑 Filter strong collaborations only
MIN_COLLAB = 3
data = [d for d in data if d["joint_publications"] >= MIN_COLLAB]

# Build graph
G = nx.Graph()

for d in data:
    i1 = d["institution_1"]
    i2 = d["institution_2"]
    w = d["joint_publications"]

    G.add_node(i1)
    G.add_node(i2)
    G.add_edge(i1, i2, weight=w)

# Create interactive network
net = Network(
    height="750px",
    width="100%",
    bgcolor="#ffffff",
    font_color="black"
)

net.from_nx(G)

# Improve layout
net.force_atlas_2based(
    gravity=-50,
    central_gravity=0.01,
    spring_length=200,
    spring_strength=0.08
)

# Save output
output_path = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "collaboration_network.html"
)

net.save_graph(output_path)

print("Network visualization created:")
print(output_path)
