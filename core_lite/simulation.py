import networkx as nx
import random


def run_simulation(
    steps=15,
    n_nodes=50,
    connection_prob=0.15,
    stress_mode="constant",
    stress=0.15,
    potential=0.2,
    scenario=None,
    external_features=None,
    initial_graph=None
):
    # -----------------------------
    # Graph
    # -----------------------------
    if initial_graph is not None:
        G = initial_graph.copy()
    else:
        if stress_mode == "increasing":
            G = nx.erdos_renyi_graph(n_nodes, connection_prob * 0.7)
        else:
            G = nx.erdos_renyi_graph(n_nodes, connection_prob)

    history = {
        "drift_signal": [],
        "graphs": [],
        "early_warning": [],
        "stability": []
    }

    erosion = 0.0

    node_load = {n: 0.1 for n in G.nodes()}
    edge_state = {tuple(sorted(e)): "strong" for e in G.edges()}

    for t in range(steps):

        # -----------------------------
        # Stress
        # -----------------------------
        if stress_mode == "increasing":
            current_stress = 0.03 + stress * (t / steps)
        else:
            current_stress = stress * 0.3

        # -----------------------------
        # Structural erosion accumulation
        # -----------------------------
        noise = random.uniform(0, 0.002)
        erosion += (current_stress + potential * 0.05) * 0.1 + noise

        drift_signal = erosion

        # -----------------------------
        # Node Load
        # -----------------------------
        for n in G.nodes():
            node_load[n] = min(1.0, node_load[n] + current_stress * 0.05)

        # -----------------------------
        # Edge Removal
        # -----------------------------
        edges_to_remove = []

        for u, v in list(G.edges()):
            prob = erosion * 0.3
            if random.random() < prob:
                edges_to_remove.append((u, v))
                edge_state[tuple(sorted((u, v)))] = "weak"

        G.remove_edges_from(edges_to_remove)

        # -----------------------------
        # Recoupling (stable system only)
        # -----------------------------
        if stress_mode == "constant":
            for _ in range(2):
                u = random.choice(list(G.nodes()))
                v = random.choice(list(G.nodes()))
                if u != v and not G.has_edge(u, v):
                    G.add_edge(u, v)
                    edge_state[tuple(sorted((u, v)))] = "new"

        # -----------------------------
        # Signals
        # -----------------------------
        early_warning = max(0, erosion - 0.02)
        stability = max(0, 1.0 - erosion)

        history["drift_signal"].append(drift_signal)
        history["graphs"].append(G.copy())
        history["early_warning"].append(early_warning)
        history["stability"].append(stability)

    return G, history, node_load, edge_state
