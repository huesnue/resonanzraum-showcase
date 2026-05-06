import streamlit as st
import plotly.graph_objects as go

from core_lite.simulation import run_simulation
from core_lite.energy_simulation import run_energy_simulation
from visualization.network_plot import plot_network

from scenarios.basic import load_scenario as load_basic
from scenarios.energy import load_scenario as load_energy
from scenarios.energy_events import EVENTS


from datetime import datetime
from dateutil.relativedelta import relativedelta
import math

# ------------------------------------------
# Helper Function: Generate Month Labels
# ------------------------------------------
def generate_months(start="2021-01", steps=48):
    months = []
    current = datetime.strptime(start, "%Y-%m")

    for _ in range(steps):
        months.append(current.strftime("%b %Y"))
        current += relativedelta(months=1)

    return months

MONTHS = generate_months(start="2021-01", steps=48)
MONTH_TO_STEP = {m: i for i, m in enumerate(MONTHS)}

# ------------------------------------------
# BASIC DEMO
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
    fig.add_trace(go.Scatter(
        y=data,
        mode="lines"
    ))
    fig.update_layout(title=title, height=250, margin=dict(l=20, r=20, t=40, b=20))
    return fig


# ------------------------------------------
# UI CONFIG
# ------------------------------------------
st.set_page_config(layout="wide")

st.title("Why systems fail before they break")

st.markdown("""
Most systems don't collapse suddenly.

They start to **erode structurally** long before anything becomes visible.

This demo shows two signals that emerge **before** the system breaks:

- a **Structural Drift** signal — detects early change in system behavior
- an **Early Warning** signal — confirms structural weakening
- while the system still appears **stable on the surface**
""")


# ------------------------------------------
# SESSION STATE INIT
# ------------------------------------------
if "mode" not in st.session_state:
    st.session_state["mode"] = "manual"

if "step" not in st.session_state:
    st.session_state["step"] = 0


# ------------------------------------------
# SCENARIO SELECTION
# ------------------------------------------
scenario_name = st.selectbox(
    "Select a scenario",
    options=["Basic Demo", "Energy Crisis"]
)

scenario = load_basic() if scenario_name == "Basic Demo" else load_energy()


# ------------------------------------------
# SCENARIO RESET
# ------------------------------------------
if "last_scenario" not in st.session_state:
    st.session_state["last_scenario"] = scenario_name

if st.session_state["last_scenario"] != scenario_name:
    st.session_state.pop("energy_history", None)
    st.session_state["last_scenario"] = scenario_name
    st.session_state["step"] = 0
    st.session_state["mode"] = "manual"


# ------------------------------------------
# RUN BUTTON
# ------------------------------------------
run_clicked = st.button("▶ Run Simulation")


# ==========================================
# BASIC SCENARIO
# ==========================================
if scenario["type"] == "basic":

    if run_clicked:
        st.session_state["basic_data"] = (
            *run_stable(),
            *run_collapse()
        )

    if "basic_data" in st.session_state:

        G1, hist_stable, load1, edges1, G2, hist_collapse, load2, edges2 = st.session_state["basic_data"]

        st.divider()
        st.subheader("System Structure")

        col1_es, col2_es = st.columns(2)
        col1_es.plotly_chart(plot_network(G1, load1, edges1), use_container_width=True)
        col2_es.plotly_chart(plot_network(G2, load2, edges2), use_container_width=True)

        st.subheader("Early Signals")

        col1, col2 = st.columns(2)
        col1.plotly_chart(plot_series(hist_stable["drift_signal"], "Structural Drift – System A"), use_container_width=True)
        col2.plotly_chart(plot_series(hist_collapse["drift_signal"], "Structural Drift – System B"), use_container_width=True)


# ==========================================
# ENERGY SCENARIO
# ==========================================
elif scenario["type"] == "energy":

    nodes = scenario["nodes"]
    edges = scenario["edges"]

    if run_clicked:
        st.session_state["energy_history"] = run_energy_simulation(nodes, edges, steps=48, month_to_step=MONTH_TO_STEP)
        st.session_state["step"] = 0
        st.session_state["mode"] = "manual"

    if "energy_history" not in st.session_state:
        st.info("Press 'Run Simulation' to start.")
        st.stop()

    history = st.session_state["energy_history"]
    max_step = len(history) - 1

    st.divider()
    st.subheader("Energy Network Simulation")

    run_every = 1.0 if st.session_state["mode"] == "playback" else None

    @st.fragment(run_every=run_every)
    def playback_panel(history, max_step):

        is_playing = st.session_state["mode"] == "playback"

        # ------------------------------------------
        # Auto-advance step during playback
        # ------------------------------------------
        if is_playing:
            current_step = st.session_state["step"]
            if current_step < max_step:
                st.session_state["step"] = current_step + 1
            else:
                st.session_state["mode"] = "manual"
                st.rerun()

        # ------------------------------------------
        # EVENT INTENSITY SERIES
        # ------------------------------------------
        event_intensity_series = []

        for step_idx in range(len(history)):

            total_intensity = 0.0

            for event in EVENTS:

                event_step = event.get("step")

                if "month" in event and event["month"] in MONTH_TO_STEP:
                    event_step = MONTH_TO_STEP[event["month"]]
                else:
                    continue

                duration = event.get("duration", 1)
                plateau = event.get("plateau", 0)
                decay = event.get("decay", 0.5)

                if step_idx < event_step or step_idx >= event_step + duration:
                    continue

                relative_t = step_idx - event_step

                if relative_t < plateau:
                    intensity = 1.0
                else:
                    intensity = math.exp(-decay * (relative_t - plateau))

                total_intensity += intensity

            event_intensity_series.append(total_intensity)

        # ------------------------------------------
        # Layout
        # ------------------------------------------
        col_left, col_right = st.columns([1, 2])

        with col_left:

            col_b1, col_b2 = st.columns(2)

            with col_b1:
                if st.button("▶ Start Playback", disabled=is_playing):
                    st.session_state["mode"] = "playback"
                    st.session_state["step"] = 0
                    st.rerun()

            with col_b2:
                if st.button("⏸ Step Mode", disabled=not is_playing):
                    st.session_state["mode"] = "manual"
                    st.rerun()

            if "simulation_step" not in st.session_state:
                st.session_state["simulation_step"] = st.session_state["step"]

            if is_playing:
                st.session_state["simulation_step"] = st.session_state["step"]

            step = st.slider(
                "Simulation Step",
                min_value=0,
                max_value=max_step,
                key="simulation_step",
                disabled=is_playing,
            )

            if not is_playing:
                st.session_state["step"] = step

            # ------------------------------------------
            # Metrics & Chart
            # ------------------------------------------
            current = history[st.session_state["step"]]

            st.write(f"📅 {MONTHS[st.session_state['step']]}")
            st.metric("System Health", f"{current['system_health']:.2f}")

            health_series = [h["system_health"] for h in history]

            # ------------------------------------------
            # Early Warning: rate of change in system health
            # A rising value signals structural weakening
            # ------------------------------------------
            early_warning_series = []

            for i in range(len(health_series)):
                if i == 0:
                    early_warning_series.append(0)
                else:
                    delta = health_series[i] - health_series[i - 1]
                    early_warning_series.append(-delta)

            # ------------------------------------------
            # Stability: combined structural signal
            # ------------------------------------------
            stability_series = [
                h["system_health"] * (1 - (sum(h["load"].values()) / len(h["load"])))
                for h in history
            ]

            fig = go.Figure()

            fig.add_trace(go.Scatter(
                y=event_intensity_series,
                mode="lines",
                name="Event Pressure",
                line=dict(dash="dot")
            ))

            fig.add_trace(go.Scatter(
                y=early_warning_series,
                mode="lines",
                name="Early Warning"
            ))

            fig.add_trace(go.Scatter(
                y=stability_series,
                mode="lines",
                name="Stability"
            ))

            fig.update_layout(
                height=300,
                margin=dict(l=20, r=20, t=40, b=60),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.3,
                    xanchor="center",
                    x=0.5
                )
            )

            st.plotly_chart(fig, use_container_width=True)

        # ------------------------------------------
        # Network Plot
        # ------------------------------------------
        with col_right:

            highlight_nodes = set()
            highlight_edges = set()

            current_step = st.session_state["step"]

            active_events = []

            for event in EVENTS:

                event_step = event.get("step")

                if "month" in event and event["month"] in MONTH_TO_STEP:
                    event_step = MONTH_TO_STEP[event["month"]]
                else:
                    continue

                duration = event.get("duration", 1)

                if current_step >= event_step and current_step < event_step + duration:
                    active_events.append(event)

            for event in active_events:
                if event.get("target") == "pipeline":
                    for edge_key in current["edges"]:
                        highlight_edges.add(edge_key)

                if "cluster" in event:
                    for node, data in current["nodes"].items():
                        if data.get("cluster") == event["cluster"]:
                            highlight_nodes.add(node)

            st.plotly_chart(
                plot_network(
                    current["graph"],
                    current["load"],
                    current["edges"],
                    highlight_nodes=highlight_nodes,
                    highlight_edges=highlight_edges
                ),
                use_container_width=True
            )

            for event in active_events:
                st.warning(f"⚠️ {event['name']}")

    # Run fragment
    playback_panel(history, max_step)
