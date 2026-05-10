"""
scenario_intro.py
=================

Drei UI-Renderer auf Basis von scenarios.scenario_info:

    render_sidebar_tagline(label, lang="en")
        Schicht 1 — 1-Zeilen-Caption unter dem Selectbox in der Sidebar.

    render_primer_card(label, on_run_label="▶ Run Simulation", lang="en")
        Schicht 2 — volle Erklärung als Karte. Wird statt der nackten
        "Press Run Simulation"-Info angezeigt, solange noch keine
        Simulationsdaten im Session State liegen.

    render_intro_expander(label, lang="en", expanded=False)
        Schicht 3 — kompakter ℹ️-Expander mit demselben Inhalt für
        die Live-Dashboard-Ansicht.

Plus Helfer:

    metric_help(label, metric_label, lang="en")
        Liefert den Tooltip-String für `st.metric(..., help=...)`.
        Returnt None, wenn nichts hinterlegt ist (st.metric ignoriert None).

Die Renderer benutzen nur st.markdown / st.expander / st.caption / st.info —
keine HTML-Tags ausserhalb safe st-Komponenten und keine externen Assets.
Sie greifen weder in Session State noch in Simulation/Plotting ein.
"""

import streamlit as st

from scenarios.scenario_info import (
    get_info_by_label,
    SCENARIO_KEY_BY_LABEL,
    SCENARIO_ICON,
)


# ------------------------------------------------------------------
# Schicht 1 — Sidebar-Tagline
# ------------------------------------------------------------------
def render_sidebar_tagline(label: str, lang: str = "en") -> None:
    """Eine Zeile unterhalb des Scenario-Selectbox in der Sidebar."""
    info = get_info_by_label(label, lang=lang)
    tagline = info.get("tagline")
    if not tagline:
        return
    # Subtile Caption — passt zur bestehenden 'Structural instability …'-Zeile
    st.caption(f"› {tagline}")


# ------------------------------------------------------------------
# Schicht 2 — Primer-Karte (Pre-Run)
# ------------------------------------------------------------------
def render_primer_card(label: str, lang: str = "en") -> None:
    """Volle Erklärungs-Karte für den Pre-Run-Zustand.

    Drop-in-Ersatz für `st.info("Press 'Run Simulation' to start.")`.
    """
    info = get_info_by_label(label, lang=lang)
    if not info:
        st.info("Press '▶ Run Simulation' to start.")
        return

    key = SCENARIO_KEY_BY_LABEL.get(label, "")
    icon = SCENARIO_ICON.get(key, "ti-info-circle")

    # Card-Wrapper als HTML via st.markdown — bewusst zurückhaltend, ohne
    # Schatten/Gradient. Nutzt Streamlits theme-bewusste Farb-Variablen.
    header_html = (
        f"<div style='display:flex;align-items:center;gap:10px;"
        f"margin:8px 0 4px;'>"
        f"<span style='font-size:11px;font-weight:600;letter-spacing:0.06em;"
        f"text-transform:uppercase;color:#888;'>Scenario</span>"
        f"</div>"
        f"<div style='font-size:20px;font-weight:600;margin:0 0 18px;'>"
        f"{label}</div>"
    )
    st.markdown(header_html, unsafe_allow_html=True)

    # Topic + Problem nebeneinander
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(_section_block("🎯 Topic", info.get("topic", "")),
                    unsafe_allow_html=True)
    with c2:
        st.markdown(_section_block("⚠️ Problem", info.get("problem", "")),
                    unsafe_allow_html=True)

    # Goal volle Breite
    st.markdown(_section_block("💡 What this scenario shows",
                               info.get("goal", "")),
                unsafe_allow_html=True)

    # Wie zu lesen — zwei Spalten
    c3, c4 = st.columns(2)
    with c3:
        st.markdown(_section_block("🌐 Network plot",
                                   info.get("read_network", "")),
                    unsafe_allow_html=True)
    with c4:
        st.markdown(_section_block("📊 Signal chart",
                                   info.get("read_signals", "")),
                    unsafe_allow_html=True)

    # Optional: Resonanzräume — nur wenn das Szenario mehr als 1 Raum hat
    spaces_text = info.get("read_spaces")
    if spaces_text:
        st.markdown(_section_block("🧭 Resonance spaces", spaces_text),
                    unsafe_allow_html=True)

    # Key Takeaways als st.info-Block (theme-bewusst)
    takeaways = info.get("key_takeaways") or []
    if takeaways:
        bullet_lines = "\n".join(f"- {t}" for t in takeaways)
        st.success("**🚩 Key takeaways**\n\n" + bullet_lines)

    # Hinweis zum Run-Button (sitzt bereits oberhalb in app_demo.py)
    st.caption("Press the **▶ Run Simulation** button above to start.")


# ------------------------------------------------------------------
# Schicht 3 — Kompakter Expander (während der Simulation)
# ------------------------------------------------------------------
def render_intro_expander(label: str, lang: str = "en",
                          expanded: bool = False) -> None:
    """ℹ️-Expander für die Dashboard-Ansicht (default kollabiert)."""
    info = get_info_by_label(label, lang=lang)
    if not info:
        return

    with st.expander("ℹ️ About this scenario", expanded=expanded):
        # Topic + Problem
        st.markdown(f"**Topic.** {info.get('topic', '')}")
        st.markdown(f"**Problem.** {info.get('problem', '')}")
        st.markdown(f"**Goal.** {info.get('goal', '')}")

        st.markdown("**How to read it.**")
        st.markdown(f"- *Network plot:* {info.get('read_network', '')}")
        st.markdown(f"- *Signal chart:* {info.get('read_signals', '')}")
        if info.get("read_spaces"):
            st.markdown(f"- *Resonance spaces:* {info['read_spaces']}")

        takeaways = info.get("key_takeaways") or []
        if takeaways:
            st.markdown("**Key takeaways.**")
            for t in takeaways:
                st.markdown(f"- {t}")


# ------------------------------------------------------------------
# Helper für inline-Tooltips an st.metric(..., help=...)
# ------------------------------------------------------------------
def metric_help(label: str, metric_label: str, lang: str = "en"):
    """Tooltip-Text für eine bestimmte Metrik. None falls nicht hinterlegt."""
    info = get_info_by_label(label, lang=lang)
    return (info.get("metric_help") or {}).get(metric_label)


# ------------------------------------------------------------------
# Internals
# ------------------------------------------------------------------
def _section_block(title_with_icon: str, body: str) -> str:
    """Zurückhaltende Sektions-Card im Stil der bestehenden App."""
    return (
        "<div style='background:rgba(127,127,127,0.06);"
        "border:1px solid rgba(127,127,127,0.15);"
        "border-radius:8px;padding:10px 14px;margin:6px 0 10px;'>"
        f"<div style='font-size:11px;font-weight:600;letter-spacing:0.04em;"
        f"text-transform:uppercase;color:#888;margin-bottom:4px;'>"
        f"{title_with_icon}</div>"
        f"<div style='font-size:14px;line-height:1.5;'>{body}</div>"
        "</div>"
    )
