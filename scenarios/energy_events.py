"""
Event Timeline 2021-2025 for Energy System Simulation

Each event represents a real-world geopolitical or structural change.

Event types:
- supply_shock       -> production drops or rises for a cluster
- demand_shock       -> consumption increases or decreases for a cluster
- capacity_shock     -> infrastructure degradation (pipelines, shipping)
- capacity_increase  -> infrastructure expansion
- coupling_shift     -> global trade route reconfiguration
- alliance_shift     -> bilateral affinity change between two clusters
- uncertainty_shock  -> system-wide stress amplification
- variability_shock  -> volatility in supply
"""

EVENTS = [

    # -----------------------------
    # 2021 - PRE-STRESS
    # -----------------------------
    {
        "month": "Feb 2021",
        "type": "supply_shock",
        "cluster": "US",
        "factor": 0.7,
        "duration": 3,
        "plateau": 1,
        "decay": 0.4,
        "name": "Texas Freeze Power Crisis"
    },
    {
        "month": "Apr 2021",
        "type": "uncertainty_shock",
        "cluster": "EU",
        "factor": 1.05,
        "duration": 4,
        "plateau": 1,
        "decay": 0.4,
        "name": "EU Gas Storage Deficit"
    },
    {
        "month": "Oct 2021",
        "type": "demand_shock",
        "cluster": "ASIA",
        "factor": 1.1,
        "duration": 4,
        "plateau": 1,
        "decay": 0.3,
        "name": "China Energy Crisis"
    },
    {
        "month": "Nov 2021",
        "type": "demand_shock",
        "cluster": "EU",
        "factor": 1.05,
        "duration": 4,
        "plateau": 1,
        "decay": 0.3,
        "name": "EU Gas Price Surge"
    },

    # -----------------------------
    # 2022 - SYSTEM SHOCK
    # -----------------------------
    {
        "month": "Feb 2022",
        "type": "supply_shock",
        "cluster": "RUSSIA",
        "factor": 0.5,
        "duration": 12,
        "plateau": 6,
        "decay": 0.1,
        "name": "Ukraine War Begins"
    },
    {
        "month": "Feb 2022",
        "type": "alliance_shift",
        "source_cluster": "RUSSIA",
        "target_cluster": "EU_CENTRAL",
        "affinity_delta": -0.6,
        "duration": 36,
        "plateau": 12,
        "decay": 0.05,
        "name": "Russia-EU Decoupling"
    },
    {
        "month": "Feb 2022",
        "type": "capacity_shock",
        "target": "pipeline",
        "factor": 0.5,
        "duration": 12,
        "plateau": 6,
        "decay": 0.1,
        "name": "Nord Stream 2 Halt"
    },
    {
        "month": "Jun 2022",
        "type": "capacity_shock",
        "target": "pipeline",
        "factor": 0.7,
        "duration": 6,
        "plateau": 2,
        "decay": 0.3,
        "name": "Nord Stream 1 Reduction"
    },
    {
        "month": "Jun 2022",
        "type": "supply_shock",
        "cluster": "US",
        "factor": 0.8,
        "duration": 4,
        "plateau": 1,
        "decay": 0.3,
        "name": "Freeport LNG Outage"
    },
    {
        "month": "Sep 2022",
        "type": "capacity_shock",
        "target": "pipeline",
        "factor": 0.2,
        "duration": 6,
        "plateau": 2,
        "decay": 0.3,
        "name": "Nord Stream Sabotage"
    },
    {
        "month": "Oct 2022",
        "type": "demand_shock",
        "cluster": "EU_CENTRAL",
        "factor": 0.95,
        "duration": 5,
        "plateau": 2,
        "decay": 0.2,
        "name": "EU Demand Reduction Policy"
    },

    # -----------------------------
    # 2023 - RESTRUCTURING
    # -----------------------------
    {
        "month": "Jan 2023",
        "type": "coupling_shift",
        "factor": 1.2,
        "duration": 12,
        "plateau": 6,
        "decay": 0.2,
        "name": "LNG Shift to Europe"
    },
    {
        "month": "Jan 2023",
        "type": "alliance_shift",
        "source_cluster": "EU_NORTH",
        "target_cluster": "EU_CENTRAL",
        "affinity_delta": 0.4,
        "duration": 24,
        "plateau": 6,
        "decay": 0.1,
        "name": "Norway-EU Energy Partnership"
    },
    {
        "month": "Apr 2023",
        "type": "capacity_shock",
        "cluster": "EU_CENTRAL",
        "factor": 0.9,
        "duration": 12,
        "plateau": 6,
        "decay": 0.2,
        "name": "German Nuclear Phase-Out"
    },
    {
        "month": "Jul 2023",
        "type": "supply_shock",
        "cluster": "EU_CENTRAL",
        "factor": 0.9,
        "duration": 5,
        "plateau": 2,
        "decay": 0.4,
        "name": "European Drought"
    },
    {
        "month": "Aug 2023",
        "type": "capacity_increase",
        "cluster": "EU_CENTRAL",
        "factor": 1.1,
        "duration": 8,
        "plateau": 4,
        "decay": 0.3,
        "name": "Coal Reactivation"
    },
    {
        "month": "Sep 2023",
        "type": "alliance_shift",
        "source_cluster": "CAUCASUS",
        "target_cluster": "EU_SOUTH",
        "affinity_delta": 0.35,
        "duration": 18,
        "plateau": 4,
        "decay": 0.1,
        "name": "Southern Gas Corridor Expansion"
    },

    # -----------------------------
    # 2024 - INSTABILITY
    # -----------------------------
    {
        "month": "Oct 2023",
        "type": "supply_shock",
        "cluster": "MIDDLE_EAST",
        "factor": 0.8,
        "duration": 6,
        "plateau": 2,
        "decay": 0.3,
        "name": "Israel-Gaza Conflict"
    },
    {
        "month": "Oct 2023",
        "type": "alliance_shift",
        "source_cluster": "MIDDLE_EAST",
        "target_cluster": "EU_SOUTH",
        "affinity_delta": -0.3,
        "duration": 8,
        "plateau": 2,
        "decay": 0.3,
        "name": "Middle East Instability"
    },
    {
        "month": "Dec 2023",
        "type": "capacity_shock",
        "target": "shipping",
        "factor": 0.7,
        "duration": 6,
        "plateau": 2,
        "decay": 0.3,
        "name": "Red Sea Disruptions"
    },
    {
        "month": "Mar 2024",
        "type": "demand_shock",
        "cluster": "ASIA",
        "factor": 1.1,
        "duration": 4,
        "plateau": 1,
        "decay": 0.4,
        "name": "China Demand Surge"
    },
    {
        "month": "Apr 2024",
        "type": "uncertainty_shock",
        "factor": 1.05,
        "duration": 3,
        "plateau": 1,
        "decay": 0.4,
        "name": "US LNG Policy Uncertainty"
    },

    # -----------------------------
    # 2025 - SYSTEMIC STRESS
    # -----------------------------
    {
        "month": "Jan 2025",
        "type": "uncertainty_shock",
        "factor": 1.05,
        "duration": 3,
        "plateau": 1,
        "decay": 0.4,
        "name": "Geopolitical Uncertainty"
    },
    {
        "month": "Feb 2025",
        "type": "supply_shock",
        "cluster": "MIDDLE_EAST",
        "factor": 0.85,
        "duration": 3,
        "plateau": 1,
        "decay": 0.2,
        "name": "Iran Sanctions Tightened"
    },
    {
        "month": "Feb 2025",
        "type": "alliance_shift",
        "source_cluster": "MIDDLE_EAST",
        "target_cluster": "TURKEY",
        "affinity_delta": -0.2,
        "duration": 6,
        "plateau": 1,
        "decay": 0.3,
        "name": "Gulf Tensions"
    },
    {
        "month": "Jun 2025",
        "type": "variability_shock",
        "factor": 1.1,
        "duration": 3,
        "plateau": 1,
        "decay": 0.4,
        "name": "Renewables Volatility"
    },
    {
        "month": "Sep 2025",
        "type": "demand_shock",
        "cluster": "EU_CENTRAL",
        "factor": 0.95,
        "duration": 3,
        "plateau": 1,
        "decay": 0.3,
        "name": "Demand Stabilization"
    },
    # -----------------------------
    # 2025 MID – FIRST IRAN ESCALATION
    # -----------------------------
    {
        "month": "Jun 2025",
        "type": "supply_shock",
        "cluster": "MIDDLE_EAST",
        "factor": 0.78,
        "duration": 4,
        "plateau": 2,
        "decay": 0.25,
        "name": "Israel Op. Rising Lion (12./13.06.) + US Op. Midnight Hammer (21./22.06.) — Iran nuclear sites struck",
        "note": "7 B-2 bombers, 14 GBU-57 MOPs on Fordow/Natanz/Isfahan; first kinetic strike on Iran nuclear program"
    },
    {
        "month": "Jun 2025",
        "type": "uncertainty_shock",
        "factor": 1.20,
        "duration": 4,
        "plateau": 2,
        "decay": 0.20,
        "name": "Strait of Hormuz closure threats — Iranian Parliament vote 23.06., shipping risk premium spikes"
    },
    # -----------------------------
    # 2025 LATE – ESCALATION
    # -----------------------------
    {
        "month": "Oct 2025",
        "type": "supply_shock",
        "cluster": "MIDDLE_EAST",
        "factor": 0.7,
        "duration": 8,
        "plateau": 3,
        "decay": 0.15,
        "name": "Iran Max Pressure Campaign"
    },
    {
        "month": "Oct 2025",
        "type": "uncertainty_shock",
        "factor": 1.08,
        "duration": 6,
        "plateau": 2,
        "decay": 0.2,
        "name": "Iran Snapback Sanctions"
    },
    {
        "month": "Dec 2025",
        "type": "capacity_shock",
        "target": "shipping",
        "factor": 0.75,
        "duration": 6,
        "plateau": 2,
        "decay": 0.2,
        "name": "Venezuela Tanker Seizures"
    },
    {
        "month": "Dec 2025",
        "type": "alliance_shift",
        "source_cluster": "MIDDLE_EAST",
        "target_cluster": "EU_SOUTH",
        "affinity_delta": -0.25,
        "duration": 8,
        "plateau": 2,
        "decay": 0.15,
        "name": "Middle East Supply Risk"
    },

    # -----------------------------
    # 2026 – SYSTEMIC SHOCKS
    # -----------------------------
    {
        "month": "Jan 2026",
        "type": "supply_shock",
        "cluster": "MIDDLE_EAST",
        "factor": 0.5,
        "duration": 10,
        "plateau": 4,
        "decay": 0.1,
        "name": "Venezuela US Intervention",
        "note": "US seizes Venezuelan oil tankers, PDVSA cut off"
    },
    {
        "month": "Jan 2026",
        "type": "uncertainty_shock",
        "factor": 1.25,
        "duration": 10,
        "plateau": 4,
        "decay": 0.08,
        "name": "Global Energy Market Shock"
    },
    {
        "month": "Jan 2026",
        "type": "alliance_shift",
        "source_cluster": "RUSSIA",
        "target_cluster": "EU_CENTRAL",
        "affinity_delta": -0.3,
        "duration": 12,
        "plateau": 4,
        "decay": 0.08,
        "name": "Geopolitical Realignment"
    },
    {
        "month": "Feb 2026",
        "type": "supply_shock",
        "cluster": "MIDDLE_EAST",
        "factor": 0.3,
        "duration": 12,
        "plateau": 6,
        "decay": 0.08,
        "name": "US-Israel Strikes on Iran"
    },
    {
        "month": "Feb 2026",
        "type": "capacity_shock",
        "target": "shipping",
        "factor": 0.15,
        "duration": 10,
        "plateau": 5,
        "decay": 0.08,
        "name": "Strait of Hormuz Closure"
    },
    {
        "month": "Feb 2026",
        "type": "alliance_shift",
        "source_cluster": "MIDDLE_EAST",
        "target_cluster": "TURKEY",
        "affinity_delta": -0.5,
        "duration": 10,
        "plateau": 4,
        "decay": 0.1,
        "name": "Iran-Turkey Relations Collapse"
    },
    {
        "month": "Feb 2026",
        "type": "alliance_shift",
        "source_cluster": "CAUCASUS",
        "target_cluster": "EU_SOUTH",
        "affinity_delta": 0.3,
        "duration": 8,
        "plateau": 2,
        "decay": 0.15,
        "name": "Caucasus Route Activation"
    },
    {
        "month": "Mar 2026",
        "type": "uncertainty_shock",
        "factor": 1.3,
        "duration": 8,
        "plateau": 3,
        "decay": 0.15,
        "name": "Regional War Spillover"
    },
    {
        "month": "Apr 2026",
        "type": "coupling_shift",
        "factor": 0.85,
        "duration": 4,
        "plateau": 1,
        "decay": 0.3,
        "name": "Energy Network Fragmentation"
    },
    {
        "month": "Feb 2026",
        "type": "demand_shock",
        "cluster": "EU_CENTRAL",
        "factor": 1.15,
        "duration": 6,
        "plateau": 2,
        "decay": 0.2,
        "name": "EU Emergency Energy Demand"
    },
    {
        "month": "Mar 2026",
        "type": "supply_shock",
        "cluster": "EU_NORTH",
        "factor": 0.8,
        "duration": 4,
        "plateau": 1,
        "decay": 0.3,
        "name": "LNG Diversion to Asia"
    },
]
