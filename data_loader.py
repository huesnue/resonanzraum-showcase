import csv

# This module provides functions to load nodes and edges from CSV files for different scenarios.

def load_nodes_csv(path):
    nodes = {}

    with open(path, newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            node_id = str(row["id"])

            # Robust parsing with fallback
            def to_float(value, default=0.0):
                try:
                    return float(value)
                except (ValueError, TypeError):
                    return default

            nodes[node_id] = {
                "id": node_id,
                "type": row.get("type", "unknown"),
                "cluster": row.get("cluster", "default"),
                "supply": to_float(row.get("supply")),
                "demand": to_float(row.get("demand")),
                "capacity": to_float(row.get("capacity")),
                "received": 0.0,
                "stress": 0.0,
                "status": "active"
            }

    return nodes


def load_edges_csv(path):
    edges = []

    with open(path, newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:

            def to_float(value, default=0.0):
                try:
                    return float(value)
                except (ValueError, TypeError):
                    return default

            edges.append({
                "source": str(row["source"]),
                "target": str(row["target"]),
                "capacity": to_float(row.get("capacity")),
                "strength": to_float(row.get("strength")),
                "type": row.get("type", "default"),
                "flow": 0.0,
                "status": "active"
            })

    return edges