import networkx as nx
import plotly.graph_objects as go
import streamlit as st


def plot_network(G, node_load, edge_state, highlight_nodes=None, highlight_edges=None):

    # ------------------------------------------
    # Fallbacks
    # ------------------------------------------
    if node_load is None:
        node_load = {n: 0.1 for n in G.nodes()}

    if edge_state is None:
        edge_state = {tuple(sorted(e)): "strong" for e in G.edges()}

    if highlight_nodes is None:
        highlight_nodes = set()

    if highlight_edges is None:
        highlight_edges = set()

    # ------------------------------------------
    # Reuse layout if node set is unchanged
    # ------------------------------------------
    nodes_key = tuple(sorted(G.nodes()))

    if "pos_cache" not in st.session_state:
        st.session_state["pos_cache"] = {}

    if nodes_key not in st.session_state["pos_cache"]:
        st.session_state["pos_cache"][nodes_key] = nx.spring_layout(G, seed=42, k=0.3)

    pos = st.session_state["pos_cache"][nodes_key]

    # ------------------------------------------
    # EDGES
    # ------------------------------------------
    edge_traces = []

    color_map = {
        "strong": "#aaaaaa",
        "weak": "#ff3b3b",
        "new": "#0077ff"
    }

    width_map = {
        "strong": 2.0,
        "weak": 0.5,
        "new": 4.5
    }

    for (u, v) in G.edges():
        key = tuple(sorted((u, v)))
        state = edge_state.get(key, "strong")

        x0, y0 = pos[u]
        x1, y1 = pos[v]

        if key in highlight_edges:
            color = "#00cfff"
            width = 4.5
        else:
            color = color_map[state]
            width = width_map[state]

        edge_traces.append(go.Scatter(
            x=[x0, x1, None],
            y=[y0, y1, None],
            mode="lines",
            line=dict(width=width, color=color),
            hoverinfo="none"
        ))

        if key in highlight_edges:
            edge_traces.append(go.Scatter(
                x=[x0, x1, None],
                y=[y0, y1, None],
                mode="lines",
                line=dict(width=width_map[state] + 2, color="purple"),
                opacity=0.6,
                hoverinfo="none"
            ))

    # ------------------------------------------
    # NODES
    # ------------------------------------------
    max_load = max(node_load.values()) if node_load else 1

    capacity_values = [v for v in nx.get_node_attributes(G, "capacity").values() if v is not None]
    has_capacity = len(capacity_values) > 0
    max_capacity = max(capacity_values) if has_capacity else 1

    # Degree-based cluster detection for graphs without capacity attributes
    degrees = dict(G.degree())
    max_degree = max(degrees.values()) if degrees else 1
    degree_threshold = max_degree * 0.6

    node_x, node_y, node_colors, node_sizes = [], [], [], []

    for node in G.nodes():

        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)

        if has_capacity:
            # Energy scenario: size based on capacity
            capacity = G.nodes[node].get("capacity", 1.0) or 1.0
            norm_capacity = capacity / max_capacity if max_capacity > 0 else 0
            size = 8 + (norm_capacity ** 1.5) * 30
        else:
            # Basic scenario: cluster nodes (high degree) larger, regular nodes smaller
            degree = degrees.get(node, 0)
            if degree >= degree_threshold:
                size = 14
            else:
                size = 7

        # Color based on load (with highlight override)
        load = node_load.get(node, 0.1)
        normalized_load = load / max_load if max_load > 0 else 0

        if node in highlight_nodes:
            node_colors.append("purple")
            node_sizes.append(size * 1.5)
        else:
            if normalized_load > 0.7:
                node_colors.append("#ff3b3b")
            elif normalized_load > 0.4:
                node_colors.append("#ff9c3b")
            else:
                node_colors.append("#6bd96b")
            node_sizes.append(size)

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers",
        text=[str(n) for n in G.nodes()],
        hoverinfo="text",
        marker=dict(
            size=node_sizes,
            color=node_colors,
            showscale=False,
            opacity=1.0,
            line=dict(width=1.5, color="#111")
        )
    )

    fig = go.Figure(data=edge_traces + [node_trace])

    fig.update_layout(
        showlegend=False,
        margin=dict(l=0, r=0, t=20, b=0),
        xaxis=dict(showgrid=False, zeroline=False, visible=False),
        yaxis=dict(showgrid=False, zeroline=False, visible=False)
    )

    return fig
