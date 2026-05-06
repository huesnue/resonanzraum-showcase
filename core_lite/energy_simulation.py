import networkx as nx
from scenarios.energy_events import EVENTS
import random
import math


def compute_system_health(nodes):

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

    raw = satisfied / total_demand

    # Minimum floor to prevent complete collapse in visualization
    health = max(0.05, raw)

    return health


def run_energy_simulation(nodes, edges, steps=10, month_to_step=None):

    history = []

    for step in range(steps):

        # ------------------------------------------
        # RESET received + flow
        # ------------------------------------------
        for n in nodes.values():
            n["received"] = 0.0

        for e in edges:
            e["flow"] = 0.0

        # ------------------------------------------
        # Store initial supply on first step
        # ------------------------------------------
        if step == 0:
            for n in nodes.values():
                n["initial_supply"] = n["supply"]

        # Restore supply for active nodes each step
        for n in nodes.values():
            if "initial_supply" in n and n["status"] != "failed":
                n["supply"] = n["initial_supply"]

        # ------------------------------------------
        # Decay stress before applying new events
        # Prevents unbounded stress accumulation
        # ------------------------------------------
        for n in nodes.values():
            if n["status"] != "failed":
                n["stress"] = n.get("stress", 0) * 0.5

        # ------------------------------------------
        # APPLY EVENTS
        # ------------------------------------------
        for event in EVENTS:
            event_step = event.get("step")

            if "month" in event and month_to_step:
                event_month = event["month"]

                if event_month not in month_to_step:
                    continue

                event_step = month_to_step[event_month]

            duration = event.get("duration", 1)
            plateau = event.get("plateau", 0)
            decay = event.get("decay", 0.5)

            if step < event_step or step >= event_step + duration:
                continue

            relative_t = step - event_step

            # Intensity with plateau and decay
            if relative_t < plateau:
                intensity = 1.0
            else:
                intensity = math.exp(-decay * (relative_t - plateau))

            event_strength = 1.5
            effective_factor = 1 + (event["factor"] - 1) * (0.5 + 0.5 * intensity) * event_strength

            if event["type"] == "capacity_shock":
                for e in edges:
                    if e.get("type") == event.get("target"):
                        e["capacity"] *= effective_factor

            elif event["type"] == "supply_shock":
                for n in nodes.values():
                    if n.get("cluster") == event.get("cluster") and n["type"] == "producer":
                        n["supply"] *= effective_factor

            elif event["type"] == "demand_shock":
                for n in nodes.values():
                    if n.get("cluster") == event.get("cluster") and n["type"] == "consumer":
                        n["demand"] *= effective_factor

            elif event["type"] == "capacity_increase":
                for n in nodes.values():
                    if n.get("cluster") == event.get("cluster"):
                        n["capacity"] *= effective_factor

            elif event["type"] == "coupling_shift":
                for e in edges:
                    e["strength"] *= min(1.0, effective_factor + 0.02)

            elif event["type"] == "uncertainty_shock":
                for n in nodes.values():
                    n["stress"] *= effective_factor

            elif event["type"] == "variability_shock":
                for n in nodes.values():
                    if n["type"] == "producer":
                        n["supply"] *= (1 + random.uniform(-0.1, 0.1))

        # ------------------------------------------
        # GLOBAL EVENT STRESS BOOST (capped)
        # ------------------------------------------
        active_intensity = 0.0

        for event in EVENTS:

            event_step = event.get("step")

            if "month" in event and month_to_step:
                event_month = event["month"]
                if event_month not in month_to_step:
                    continue
                event_step = month_to_step[event_month]

            duration = event.get("duration", 1)
            plateau = event.get("plateau", 0)
            decay = event.get("decay", 0.5)

            if step < event_step or step >= event_step + duration:
                continue

            relative_t = step - event_step

            if relative_t < plateau:
                intensity = 1.0
            else:
                intensity = math.exp(-decay * (relative_t - plateau))

            active_intensity += intensity

        # Hard cap on stress boost per tick
        if active_intensity > 0:
            for n in nodes.values():
                if n["status"] != "failed":
                    boost = min(10.0, 2.0 * active_intensity)
                    n["stress"] = n.get("stress", 0) + boost

        # ------------------------------------------
        # BUILD GRAPH
        # ------------------------------------------
        G = nx.Graph()
        edge_map = {}

        for node_id, node_data in nodes.items():
            G.add_node(node_id, **node_data)

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
        # PRODUCERS / CONSUMERS
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
        # MARKET LOGIC
        # ------------------------------------------
        for consumer in consumers:

            demand = nodes[consumer]["demand"]

            if demand <= 0:
                continue

            best_path = None
            best_score = 0

            for producer in producers:

                try:
                    paths = list(nx.all_simple_paths(G, producer, consumer, cutoff=4))
                except Exception:
                    continue

                for path in paths:

                    capacities = []

                    for i in range(len(path) - 1):
                        e = edge_map.get((path[i], path[i + 1]))

                        if not e or e["status"] == "failed":
                            capacities = []
                            break

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
                if best_score > 0.05:
                    flow = min(0.1, best_score)
                else:
                    continue

            for i in range(len(best_path) - 1):
                e = edge_map[(best_path[i], best_path[i + 1])]
                e["flow"] += flow

            nodes[producer]["supply"] -= flow
            nodes[consumer]["received"] += flow

        # ------------------------------------------
        # EDGE DYNAMICS
        # ------------------------------------------
        for e in edges:

            if e["status"] == "failed":
                continue

            flow = e["flow"]
            capacity = e["capacity"]

            if capacity <= 0:
                continue

            flow_ratio = (flow / capacity) * e["strength"]

            # Hard overload → failure
            if flow_ratio > 1.5:
                e["status"] = "failed"
                e["strength"] = max(0.1, e["strength"] * 0.2)

            # High load → structural weakening
            elif flow_ratio > 1.0:
                e["strength"] = max(0.2, e["strength"] * 0.7)

            elif flow_ratio > 0.7:
                e["strength"] = max(0.4, e["strength"] * 0.85)

            # Low load → recovery
            else:
                e["strength"] = min(1.0, e["strength"] * 1.02)

        # ------------------------------------------
        # EDGE RECOVERY (stress-dependent probability)
        # ------------------------------------------
        for e in edges:

            if e["status"] != "failed":
                continue

            u = e["source"]
            v = e["target"]

            if nodes[u]["status"] == "failed" or nodes[v]["status"] == "failed":
                continue

            avg_stress = (nodes[u].get("stress", 0) + nodes[v].get("stress", 0)) / 2.0
            recovery_prob = max(0.02, 0.2 * math.exp(-avg_stress / 30.0))

            if random.random() < recovery_prob:
                e["status"] = "active"
                e["strength"] = 0.3

        # ------------------------------------------
        # Rebuild graph after edge recovery
        # ------------------------------------------
        G = nx.Graph()
        edge_map = {}

        for node_id, node_data in nodes.items():
            G.add_node(node_id, **node_data)

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
        # CONNECTIVITY SAFEGUARD
        # ------------------------------------------
        active_edges = sum(1 for e in edges if e["status"] == "active")
        active_nodes = sum(1 for n in nodes.values() if n["status"] != "failed")

        if active_nodes > 0 and active_edges < active_nodes * 0.3:
            for e in edges:
                if e["status"] == "failed":
                    u = e["source"]
                    v = e["target"]
                    if nodes[u]["status"] != "failed" or nodes[v]["status"] != "failed":
                        e["status"] = "active"
                        e["strength"] = 0.2

        # ------------------------------------------
        # STRESS PROPAGATION
        # ------------------------------------------

        # Phase 1: External stress (undersupply)
        for node_id, n in nodes.items():

            if n["status"] == "failed":
                n["stress"] = 100.0
                continue

            external_stress = max(0.0, n["demand"] - n["received"])
            n["stress"] = 0.7 * n.get("stress", 0) + external_stress

        # Phase 2: Stress propagation through neighbors
        for node_id, n in nodes.items():

            if n["status"] == "failed":
                continue

            neighbors = list(G.neighbors(node_id))

            if not neighbors:
                continue

            neighbor_stress = sum(nodes[nb]["stress"] for nb in neighbors) / len(neighbors)
            propagated = 0.3 * neighbor_stress
            n["stress"] += propagated

        # ------------------------------------------
        # NODE FAILURE
        # ------------------------------------------
        for n in nodes.values():

            if n["status"] == "failed":
                continue

            if n["stress"] > 60:
                n["status"] = "failed"

            elif n["stress"] > 30:
                n["supply"] *= 0.7

            elif n["stress"] > 15:
                n["supply"] *= 0.9

        # ------------------------------------------
        # NODE RECOVERY
        # ------------------------------------------
        for node_id, n in nodes.items():

            if n["status"] != "failed":
                continue

            current_stress = n.get("stress", 100.0)

            if current_stress < 20.0:
                recovery_prob = 0.15 * math.exp(-current_stress / 20.0)

                if random.random() < recovery_prob:
                    n["status"] = "active"
                    n["supply"] = n.get("initial_supply", 1.0) * 0.3
                    n["stress"] = 15.0

        # ------------------------------------------
        # SYSTEM HEALTH
        # ------------------------------------------
        system_health = compute_system_health(nodes)

        # ------------------------------------------
        # EDGE STATE SNAPSHOT
        # ------------------------------------------
        edge_state = {}

        for e in edges:
            u = e["source"]
            v = e["target"]

            key = tuple(sorted((u, v)))

            flow = e.get("flow", 0.0)
            capacity = e.get("capacity", 1.0)
            status = e.get("status", "active")

            if status == "failed":
                edge_state[key] = "weak"
            elif flow > capacity:
                edge_state[key] = "weak"
            elif flow > 0:
                edge_state[key] = "strong"
            else:
                edge_state[key] = "new"

        # ------------------------------------------
        # SNAPSHOT
        # ------------------------------------------
        history.append({
            "graph": G,
            "nodes": {k: v.copy() for k, v in nodes.items()},
            "edges": edge_state,
            "system_health": system_health,
            "load": {k: nodes[k]["stress"] for k in nodes}
        })

    return history
