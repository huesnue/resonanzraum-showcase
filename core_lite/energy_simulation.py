import networkx as nx

def compute_coherence(nodes):

    total_demand = 0.0
    satisfied = 0.0

    for n in nodes.values():

        if n["type"] != "consumer":
            continue

        demand = n["demand"]
        received = n.get("received", 0.0)

        total_demand += demand
        satisfied += min(demand, received)

    if total_demand == 0:
        return 1.0

    return satisfied / total_demand

def run_energy_simulation(nodes, edges, steps=10):

    history = []

    for step in range(steps):

        # ------------------------------------------
        # RESET (pro Tick)
        # ------------------------------------------
        for n in nodes.values():
            n["received"] = 0.0

        for e in edges:
            e["flow"] = 0.0

        # ------------------------------------------
        # GRAPH (nur aktive Struktur!)
        # ------------------------------------------
        G = nx.Graph()
        edge_map = {}

        for e in edges:

            if e["status"] == "failed":
                continue

            u = e["source"]
            v = e["target"]

            if nodes[u]["status"] == "failed" or nodes[v]["status"] == "failed":
                continue

            G.add_edge(u, v)

            edge_map[(u, v)] = e
            edge_map[(v, u)] = e

        # ------------------------------------------
        # PRODUCERS / CONSUMERS (nur aktive!)
        # ------------------------------------------
        producers = [
            n for n in nodes
            if nodes[n]["type"] == "producer" and nodes[n]["status"] != "failed"
        ]

        consumers = [
            n for n in nodes
            if nodes[n]["type"] == "consumer" and nodes[n]["status"] != "failed"
        ]

        # ------------------------------------------
        # MARKET LOGIC (Demand-driven)
        # ------------------------------------------
        for consumer in consumers:

            demand = nodes[consumer]["demand"]

            if demand <= 0:
                continue

            best_path = None
            best_score = 0

            for producer in producers:

                try:
                    path = nx.shortest_path(G, producer, consumer)
                except:
                    continue

                capacities = []

                for i in range(len(path) - 1):
                    e = edge_map[(path[i], path[i+1])]
                    capacities.append(e["capacity"] * e["strength"])

                if not capacities:
                    continue

                score = min(capacities)

                if score > best_score:
                    best_score = score
                    best_path = path

            if best_path is None:
                continue

            producer = best_path[0]
            available = nodes[producer]["supply"]

            flow = min(demand, available, best_score)

            if flow <= 0:
                continue

            # Apply flow
            for i in range(len(best_path) - 1):
                e = edge_map[(best_path[i], best_path[i+1])]
                e["flow"] += flow

            nodes[producer]["supply"] -= flow
            nodes[consumer]["received"] += flow

        # ------------------------------------------
        # EDGE FAILURE / DEGRADATION
        # ------------------------------------------
        for e in edges:

            if e["status"] == "failed":
                continue

            flow = e["flow"]
            capacity = e["capacity"]

            if flow > capacity * 1.5:
                e["status"] = "failed"
                e["strength"] = max(0.1, e["strength"] * 0.2)

            elif flow > capacity:
                e["strength"] = max(0.3, e["strength"] * 0.7)

        # ------------------------------------------
        # STRESS
        # ------------------------------------------
        for n in nodes.values():

            if n["status"] == "failed":
                n["stress"] = 100.0
                continue

            stress = max(0.0, n["demand"] - n["received"])
            n["stress"] = stress

        # ------------------------------------------
        # NODE FAILURE
        # ------------------------------------------
        for n in nodes.values():

            if n["status"] == "failed":
                continue

            if n["stress"] > 60:
                n["status"] = "failed"
                n["supply"] = 0.0

            elif n["stress"] > 25:
                n["supply"] *= 0.6
                
        # ------------------------------------------
        # COHERENCE
        # ------------------------------------------
        K = compute_coherence(nodes)

        # ------------------------------------------
        # SNAPSHOT
        # ------------------------------------------
        history.append({
            "nodes": {k: v.copy() for k, v in nodes.items()},
            "edges": [e.copy() for e in edges],
            "coherence": K
        })

    return history