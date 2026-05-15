"""
Standalone Intro-Renderer fuer das Rail & Critical Infrastructure Szenario.

Liefert zwei Funktionen analog zum Eurozone-/Cyber-Cloud-Pattern:
  - render_critical_infra_primer():  grosse Card vor dem ersten Run
  - render_critical_infra_intro():   kompakter Expander ueber den Controls

Theme-aware: das CSS nutzt currentColor/opacity statt harter weisser
Textfarben, damit es in Light- und Dark-Mode gleichermassen lesbar ist.
"""

import streamlit as st


# ============================================================
# TEXT-INHALTE
# ============================================================

PRIMER = {
    "topic": (
        "A cross-domain stress-test for transportation-critical infrastructure. "
        "Four coupled spaces — Digital (cloud, identity, control), Rail (main "
        "nodes, signaling, dispatch, regional), Economic (supply chain, freight, "
        "production, sentiment), and Social (commuter clusters: rail / car / "
        "home-office / alt-mobility / air) — interact through cross-space "
        "bridges and substitution paths. Phase 1 reconstructs COVID, the 2022 "
        "DB radio sabotage, the Riedbahn closure, CrowdStrike, the GRU-attributed "
        "DFS cyber-attack, Hamburg-Berlin (9 months), Operation Eastwood, and "
        "the Feb 2026 sabotage / DDoS wave on the railway."
    ),
    "problem": (
        "Resilience models treat railway operations and cyber security as "
        "separate silos. The real fragility lives in the cross-space coupling: "
        "an IT outage that strands rolling stock, a trust collapse that pulls "
        "commuters permanently off rail, an economic absorption that either "
        "cushions or cements the substitution. Once commuter trust drops "
        "below the hysteresis floor, rail share does not come back even after "
        "service is restored."
    ),
    "shows": (
        "How three pathways (Resilient / Hybrid / Fragile) diverge under the "
        "same historical stress chain. Different outcomes come from different "
        "internal coupling and trust hysteresis, not from different external "
        "shocks. The Fragile path shows permanent cluster migration; "
        "Resilient absorbs the same shocks without trust collapse."
    ),
    "network": (
        "Four coupled resonance spaces. Circles = digital, squares = rail, "
        "diamonds = economic, hexagons = social. Dashed edges are cross-space "
        "bridges — the channels where systemic risk crosses domains. Dotted "
        "edges are substitution paths (rail ⇄ social, digital ⇄ economic). "
        "Bridge and substitution edges light up when active."
    ),
    "signal": (
        "System Health is the headline. Four layer lines run alongside: "
        "Digital Resilience, Rail Operability, Economic Output, Social Mobility. "
        "Rail demand share on a secondary axis reveals the commuter migration "
        "dynamic. Phase 2 adds ensemble bands. Early Warning markers show "
        "lead time before Stability confirms the drop."
    ),
    "spaces": (
        "Digital supplies IT availability. Rail converts it into operational "
        "capacity. Economic absorbs shock via supply chain and substitution. "
        "Social carries commuter trust — when it breaks, rail falls "
        "structurally. The cross-space bridges are where stress crosses "
        "domains — that is where systemic events show up."
    ),
}

TAKEAWAYS = [
    "Cross-space coupling is where systemic risk lives — not in any single domain.",
    "Trust hysteresis: once commuter trust drops below the floor, rail share does not return.",
    "Fragile ≠ bigger shocks — same shocks, weaker cross-space coupling.",
]


# ============================================================
# CSS — THEME-AWARE
# Keine harten Text-Farben. currentColor erbt vom Streamlit-Theme.
# Backgrounds/Borders mit neutralen Graustufen, die in Light und
# Dark gleichermassen funktionieren.
# ============================================================

_CARD_CSS = """
<style>
.ci-primer-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px;
  margin-top: 12px;
}
.ci-primer-card {
  background: rgba(128, 128, 128, 0.08);
  border: 1px solid rgba(128, 128, 128, 0.22);
  border-radius: 8px;
  padding: 10px 14px;
}
.ci-primer-card .ci-label {
  font-size: 11px;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  opacity: 0.65;
  margin-bottom: 4px;
}
.ci-primer-card .ci-body {
  font-size: 13px;
  line-height: 1.45;
  opacity: 0.92;
}
.ci-primer-card.full {
  grid-column: span 2;
}
.ci-scenario-label {
  font-size: 11px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  opacity: 0.55;
  margin-top: 6px;
}
.ci-scenario-title {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 4px;
}
.ci-takeaways {
  margin-top: 14px;
  background: rgba(82, 196, 107, 0.10);
  border-left: 3px solid #52c46b;
  border-radius: 0 8px 8px 0;
  padding: 10px 16px;
}
.ci-takeaways .ci-tlabel {
  color: #2e8a47;
  font-weight: 600;
  font-size: 13px;
  margin-bottom: 6px;
}
.ci-takeaways ul {
  margin: 0;
  padding-left: 18px;
  font-size: 13px;
}
.ci-takeaways li {
  margin: 3px 0;
  opacity: 0.92;
}
@media (prefers-color-scheme: dark) {
  .ci-takeaways .ci-tlabel {
    color: #52c46b;
  }
}
</style>
"""


def _card(label, body, icon, full=False):
    cls = "ci-primer-card full" if full else "ci-primer-card"
    return (
        f'<div class="{cls}">'
        f'<div class="ci-label">{icon} {label}</div>'
        f'<div class="ci-body">{body}</div>'
        f'</div>'
    )


def _takeaways():
    items = "".join(f"<li>{t}</li>" for t in TAKEAWAYS)
    return (
        '<div class="ci-takeaways">'
        '<div class="ci-tlabel">🚩 Key takeaways</div>'
        f'<ul>{items}</ul>'
        '</div>'
    )


# ============================================================
# RENDER FUNCTIONS
# ============================================================

def render_critical_infra_primer():
    """Big card shown before the first ensemble run."""
    st.markdown(_CARD_CSS, unsafe_allow_html=True)

    st.markdown(
        '<div class="ci-scenario-label">SCENARIO</div>'
        '<div class="ci-scenario-title">Rail &amp; Critical Infrastructure</div>',
        unsafe_allow_html=True,
    )

    html = (
        '<div class="ci-primer-grid">'
        + _card("Topic",     PRIMER["topic"],   "📌")
        + _card("Problem",   PRIMER["problem"], "⚠️")
        + _card("What this scenario shows", PRIMER["shows"], "💡", full=True)
        + _card("Network plot",      PRIMER["network"], "🌐")
        + _card("Signal chart",      PRIMER["signal"],  "📈")
        + _card("Resonance spaces",  PRIMER["spaces"],  "🧊", full=True)
        + '</div>'
        + _takeaways()
    )
    st.markdown(html, unsafe_allow_html=True)


def render_critical_infra_intro():
    """Compact expander shown above the live-dashboard controls."""
    with st.expander("ℹ️  About this scenario", expanded=False):
        st.markdown(_CARD_CSS, unsafe_allow_html=True)
        html = (
            '<div class="ci-primer-grid">'
            + _card("Topic",   PRIMER["topic"],   "📌")
            + _card("Problem", PRIMER["problem"], "⚠️")
            + _card("What this scenario shows", PRIMER["shows"], "💡", full=True)
            + _card("Network plot", PRIMER["network"], "🌐")
            + _card("Signal chart", PRIMER["signal"],  "📈")
            + _card("Resonance spaces", PRIMER["spaces"], "🧊", full=True)
            + '</div>'
            + _takeaways()
        )
        st.markdown(html, unsafe_allow_html=True)
