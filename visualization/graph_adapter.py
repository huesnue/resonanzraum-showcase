import networkx as nx


def build_graph_for_plot(nodes, edges):
    """
    Adapter zwischen Simulation (nodes/edges) und Plot (network_plot.py)

    Ziel:
    - kompatibel mit plot_network(G, node_load, edge_state)
    - berücksichtigt FAILED nodes/edges
    - robust gegen fehlende Werte
    """

    G = nx.Graph()
    node_load = {}
    edge_state = {}

    # ------------------------------------------
    # NODES
    # ------------------------------------------
    for node_id, data in nodes.items():

        # FAILED Nodes werden NICHT angezeigt
        if data.get("status") == "failed":
            continue

        G.add_node(node_id)

        # Stress → Farbwert (Load)
        node_load[node_id] = data.get("stress", 0.0)

    # ------------------------------------------
    # EDGES
    # ------------------------------------------
    for e in edges:

        # FAILED Edges nicht anzeigen
        if e.get("status") == "failed":
            continue

        u = e["source"]
        v = e["target"]

        # Wenn Node fehlt (failed), skip
        if u not in G.nodes or v not in G.nodes:
            continue

        G.add_edge(u, v)

        key = tuple(sorted((u, v)))

        flow = e.get("flow", 0.0)
        capacity = e.get("capacity", 1.0)

        # --------------------------------------
        # EDGE STATE (Visualisierung)
        # --------------------------------------
        if flow > capacity:
            edge_state[key] = "weak"     # überlastet → rot
        elif flow > 0:
            edge_state[key] = "strong"   # aktiv → grau
        else:
            edge_state[key] = "new"      # ungenutzt → blau

    return G, node_load, edge_state