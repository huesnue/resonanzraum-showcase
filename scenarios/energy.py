from data_loader import load_nodes_csv, load_edges_csv

# This module defines a function to load the energy crisis scenario by reading nodes and edges from CSV files.
def load_scenario():
    # Load nodes and edges from CSV files
    nodes = load_nodes_csv("data/nodes.csv")
    edges = load_edges_csv("data/edges.csv")
    
    # Add any additional processing or transformations here if needed
    return {
        "nodes": nodes,
        "edges": edges,
        "type": "energy"
    }