import streamlit as st
import plotly.graph_objects as go

from core_lite.simulation import run_simulation
from core_lite.energy_simulation import run_energy_simulation

from visualization.network_plot import plot_network
from visualization.graph_adapter import build_graph_for_plot

from scenarios.basic import load_scenario as load_basic
from scenarios.energy import load_scenario as load_energy


# ------------------------------------------
# BASIC DEMO (bestehend)
# ------------------------------------------
def run_stable():
    return run_simulation(
        steps=15,
        n_nodes=50,
        connection_prob=0.2,
        stress_mode="constant",
        stress=0.15,
        potential=0.2
    )


def run_collapse():
    return run_simulation(
        steps=15,
        n_nodes=50,
        connection_prob=0.2,
        stress_mode="increasing",
        stress=0.2,
        potential=0.25
    )


# ------------------------------------------
# Helper Plot
# ------------------------------------------
def plot_series(data, title):
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=data, mode="lines"))
    fig.update_layout(title=title, height=250, margin=dict(l=20, r=20, t=40, b=20))
    return fig


# ------------------------------------------
# UI CONFIG
# ------------------------------------------
st.set_page_config(layout="wide")

st.title("Why systems fail before they break")

st.markdown(
"""
Most systems don't collapse suddenly.

They start to **erode structurally** long before anything becomes visible.

This demo shows:

- an **early signal (dE/dt)**
- a **structural confirmation (W_grad)**
- while the system still appears **stable**
"""
)


# ------------------------------------------
# SCENARIO SELECTION
# ------------------------------------------
scenario_name = st.selectbox(
    "Select a scenario",
    options=["Basic Demo", "Energy Crisis"]
)

if scenario_name == "Basic Demo":
    scenario = load_basic()
else:
    scenario = load_energy()


# ------------------------------------------
# SCENARIO CHANGE DETECTION (FIX)
# ------------------------------------------
if "last_scenario" not in st.session_state:
    st.session_state["last_scenario"] = scenario_name

if st.session_state["last_scenario"] != scenario_name:
    st.session_state.pop("energy_history", None)
    st.session_state["last_scenario"] = scenario_name


# ------------------------------------------
# RUN BUTTON (GLOBAL FIX)
# ------------------------------------------
run_clicked = st.button("▶ Run Simulation", key="run_simulation")


# ------------------------------------------
# INFO
# ------------------------------------------
if scenario["type"] == "basic":
    st.warning(
        "This is a basic demo with synthetic data. "
        "For a more realistic scenario, select 'Energy Crisis'."
    )


# ==========================================
# BASIC SCENARIO
# ==========================================
if scenario["type"] == "basic":

    if run_clicked:
        G1, hist_stable, load1, edges1 = run_stable()
        G2, hist_collapse, load2, edges2 = run_collapse()

        st.session_state["basic_data"] = (G1, hist_stable, load1, edges1,
                                         G2, hist_collapse, load2, edges2)

    if "basic_data" in st.session_state:

        G1, hist_stable, load1, edges1, G2, hist_collapse, load2, edges2 = st.session_state["basic_data"]

        st.divider()

        st.subheader("System Structure")

        st.markdown("""
### 🔎 How to read this visualization

**Nodes**
- 🟡 → 🔴 Stress level  
- ⭕ Small → Large = structural importance  

**Edges**
- ⚪ Stable  
- 🔴 Weak  
- 🔵 New  

---

**Interpretation**

- A stable system maintains **strong connectivity and central structure**
- A collapsing system shows **fragmentation and loss of structure**
- Early signals appear **before visible breakdown**
""")

        col1_es, col2_es = st.columns(2)

        col1_es.markdown("**System A (Stable)**")
        col1_es.plotly_chart(
            plot_network(G1, load1, edges1),
            use_container_width=True
        )

        col2_es.markdown("**System B (Collapse)**")
        col2_es.plotly_chart(
            plot_network(G2, load2, edges2),
            use_container_width=True
        )

        st.subheader("Early Signals")

        col1, col2 = st.columns(2)

        col1.plotly_chart(
            plot_series(hist_stable["dE_dt"], "dE/dt A"),
            use_container_width=True
        )

        col2.plotly_chart(
            plot_series(hist_collapse["dE_dt"], "dE/dt B"),
            use_container_width=True
        )

        st.subheader("Structural Change (W_grad)")

        col1, col2 = st.columns(2)

        col1.plotly_chart(
            plot_series(hist_stable["W_grad"], "W_grad A"),
            use_container_width=True
        )

        col2.plotly_chart(
            plot_series(hist_collapse["W_grad"], "W_grad B"),
            use_container_width=True
        )

        st.subheader("System Stability")

        col1, col2 = st.columns(2)

        col1.plotly_chart(
            plot_series(hist_stable["stability"], "Stability A"),
            use_container_width=True
        )

        col2.plotly_chart(
            plot_series(hist_collapse["stability"], "Stability B"),
            use_container_width=True
        )


# ==========================================
# ENERGY SCENARIO
# ==========================================
elif scenario["type"] == "energy":

    nodes = scenario["nodes"]
    edges = scenario["edges"]

    if run_clicked:
        history = run_energy_simulation(nodes, edges, steps=10)
        st.session_state["energy_history"] = history

    if "energy_history" in st.session_state:

        history = st.session_state["energy_history"]

        # ------------------------------------------
        # TIME CONTROL + COMPACT LAYOUT (FIX)
        # ------------------------------------------
        st.divider()
        st.subheader("Energy Network Simulation")

        st.markdown("""
        This scenario shows a simplified but realistic energy network:

        - Producers (Russia, Norway, Middle East)
        - Transit hubs (Ukraine, Turkey, Balkans)
        - Demand centers (Germany, Italy, France)

        The system evolves dynamically based on demand, flow, and structural constraints.
        """)

        col_left, col_right = st.columns([1, 2])

        # ------------------------------------------
        # LEFT: CONTROL + METRICS
        # ------------------------------------------
        with col_left:
            step = st.slider(
                "Simulation Step",
                min_value=0,
                max_value=len(history) - 1,
                value=len(history) - 1,
                key="energy_slider"
            )

            st.write(f"Current Step: {step}")

            current = history[step]

            # ------------------------------------------
            # COHERENCE DISPLAY
            # ------------------------------------------
            K = current["coherence"]

            st.metric("System Coherence (K)", f"{K:.2f}")
            
            if K > 0.8:
                st.success("System stable")
            elif K > 0.6:
                st.warning("Early signs of stress")
            elif K > 0.4:
                st.warning("Critical state")
            else:
                st.error("System unstable")

            # ------------------------------------------
            # COHERENCE OVER TIME
            # ------------------------------------------
            coherence_series = [h["coherence"] for h in history]
            st.line_chart(coherence_series, height=150)

        # ------------------------------------------
        # RIGHT: NETWORK (VISIBLE WITHOUT SCROLL)
        # ------------------------------------------
        with col_right:
            G_plot, node_load, edge_state = build_graph_for_plot(
                current["nodes"],
                current["edges"]
            )

            st.plotly_chart(
                plot_network(G_plot, node_load, edge_state),
                use_container_width=True
            )