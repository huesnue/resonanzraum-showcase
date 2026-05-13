"""
Critical Infrastructure Event Timeline — Rail & Connected Systems Resilience
=============================================================================

Phase 1 (2020-01 bis 2026-05): Historische Rekonstruktion auf Basis
oeffentlich belegbarer Vorfaelle in den vier Raeumen.
  - COVID-Cloud-Schub + radikaler Pendler-Verhaltenswandel (2020)
  - SolarWinds + Cloud-Trust-Erosion (2020-2021)
  - DB-Bahnfunk-Sabotage Oct 2022 (Schleswig-Holstein, NRW)
  - GDL-Streiks 2024 (Jan-Mar)
  - DB-Generalsanierung Riedbahn Jul-Dec 2024
  - DORA-Geltung Jan 2025
  - Schienennetz-Stoerungen, Cyber-Vorfaelle, Lieferketten-Schocks

Phase 2 (2026-06 bis 2030-12): Strukturelle Projektionspfade
  - PATH_A: "Resilient" — ETCS-Vollausbau, Multi-Cloud-DR, robuste Substitution
  - PATH_B: "Hybrid"    — Teilmodernisierung, mittlere Resilienz
  - PATH_C: "Fragile"   — technische Schulden, IT-SPoF, Vertrauenskollaps

Event-Typen (aus dem bestehenden Showcase-Vokabular, IP-sicher):
  supply_shock        -> Versorgungs-/Verfuegbarkeitseinbruch
  demand_shock        -> Last steigt (Recovery, Pendlerrueckkehr)
  capacity_shock      -> Tragfaehigkeit reduziert (Outage, Stoerung)
  capacity_increase   -> Policy-Response/Investition staerkt Buffer
  coupling_shift     -> Vertrauensverschiebung in Kopplungen
  alliance_shift     -> Cluster-Affinitaet (Mobilitaetsverlagerung)
  uncertainty_shock  -> Systemweite Stressverstaerkung
  variability_shock  -> Volatile/ungleichmaessige Belastung
  migration_shift    -> NEU: Demand-Migration im sozialen Raum
                        (Bahn -> Auto / Homeoffice / Alt-Mobility)

Optionale Felder fuer das active_event-Tooltip im UI:
  attack_type   -> spezifischer Vorfalls-Subtyp
                   (cyber: ransomware, ddos, supply_chain, ...
                    rail:  signal_failure, sabotage, strike, ...
                    econ:  supply_disruption, sentiment_shock, ...)
  actor         -> Akteur/Quelle/Ursache

Cluster-Bezeichnungen (critical_infra_nodes.csv):
  digital-space  : Cloud, Security, OT_IT_Bridge, Platform, Network
  rail-space     : MainNodes, Signaling, Operations, Maintenance, Regional
  economic-space : Logistics, Production, Services, Sentiment
  social-space   : Mobility_Rail, Mobility_Car, Mobility_Remote,
                   Mobility_Alt, Mobility_Air

IP-Hinweis: Keine R2M-Formeln oder Variablen exponiert.
Alle Events oeffentlich referenzierbar (Bundesnetzagentur, BSI, ENISA,
DB-Geschaeftsberichte, EBA-Reports, Eurostat).
"""

# --------------------------------------------------
# HISTORISCHE TIMELINE 2020-2026
# --------------------------------------------------

EVENTS_HISTORICAL = [

    # ---- 2020: COVID-Schock + SolarWinds ----
    {
        "month": "Mar 2020",
        "type": "demand_shock",
        "cluster": "Mobility_Rail",
        "factor": 0.40,
        "duration": 6,
        "plateau": 3,
        "decay": 0.08,
        "name": "COVID-19 — Pendlerverkehr bricht ein, DB-Fernverkehr faellt ca. 60 %",
        "attack_type": "demand_collapse",
        "actor": "Pandemic shock",
        "source": "DB Geschaeftsbericht 2020; Eurostat ICT Survey 2020/21"
    },
    {
        "month": "Mar 2020",
        "type": "migration_shift",
        "cluster": "Mobility_Rail",
        "factor": 0.35,
        "duration": 12,
        "plateau": 6,
        "decay": 0.05,
        "name": "[Migration] Massiver Shift Bahn -> Homeoffice; Vertrauensschock Pendler",
        "attack_type": "behavioral_shift",
        "actor": "Pandemic response",
        "source": "Statista Mobility Reports 2020-2022; Civey Mobilitaetsumfragen"
    },
    {
        "month": "Mar 2020",
        "type": "coupling_shift",
        "cluster": "Cloud",
        "factor": 1.25,
        "duration": 6,
        "plateau": 3,
        "decay": 0.10,
        "name": "COVID-19 — beschleunigter Cloud-Adoption-Schub, Remote-Work",
        "attack_type": "structural_shift",
        "source": "ENISA Threat Landscape 2020"
    },
    {
        "month": "Dec 2020",
        "type": "coupling_shift",
        "cluster": "Security",
        "factor": 0.75,
        "duration": 8,
        "plateau": 3,
        "decay": 0.12,
        "name": "SolarWinds Sunburst — Supply-Chain-Kompromittierung, Cloud-Vertrauenserosion",
        "attack_type": "supply_chain",
        "actor": "APT29 / Cozy Bear",
        "source": "CISA AA20-352A; Mandiant 2021"
    },

    # ---- 2021: Erholung + Log4Shell ----
    {
        "month": "Jun 2021",
        "type": "demand_shock",
        "cluster": "Mobility_Rail",
        "factor": 1.15,
        "duration": 4,
        "plateau": 2,
        "decay": 0.20,
        "name": "Lockerungen — partielle Pendlerrueckkehr (gedaempfte Erholung)",
        "attack_type": "recovery_partial",
        "source": "DB Geschaeftsbericht 2021"
    },
    {
        "month": "Dec 2021",
        "type": "capacity_shock",
        "cluster": "Cloud",
        "factor": 0.82,
        "duration": 2,
        "plateau": 1,
        "decay": 0.25,
        "name": "Log4Shell (CVE-2021-44228) — kritische Java-Logging-Luecke, breite Exposition",
        "attack_type": "vulnerability_disclosure",
        "source": "CISA AA21-356A; NCSC-DE Bericht 2021"
    },

    # ---- 2022: Bahn-Sabotage + Ukraine ----
    {
        "month": "Feb 2022",
        "type": "uncertainty_shock",
        "cluster": "Sentiment",
        "factor": 1.30,
        "duration": 8,
        "plateau": 3,
        "decay": 0.10,
        "name": "Ukraine-Krieg Beginn — Energie-/Lieferkettenschock, Sentiment-Einbruch",
        "attack_type": "geopolitical_shock",
        "actor": "RU state aggression",
        "source": "ECB Financial Stability Review May 2022"
    },
    {
        # KORREKTUR: Region war "Berlin/SH/NRW" -> tatsaechlich Niedersachsen,
        # Bremen, Hamburg, Schleswig-Holstein. ICE-Strecke Berlin-NRW indirekt
        # betroffen. Datum: 8. Oktober 2022, ca. 3h Fernverkehr aus.
        "month": "Oct 2022",
        "type": "capacity_shock",
        "cluster": "Signaling",
        "factor": 0.55,
        "duration": 2,
        "plateau": 1,
        "decay": 0.40,
        "name": "DB Bahnfunk-Sabotage (08.10.2022) — Glasfaser-Schnitte Niedersachsen/Bremen/Hamburg/SH, ICE-Verkehr 3h aus",
        "attack_type": "sabotage",
        "actor": "Unbekannt (BKA-Ermittlungen)",
        "source": "BKA-Pressemitteilung 2022-10-08; DB-Mitteilung 2022-10-08"
    },
    {
        "month": "Oct 2022",
        "type": "uncertainty_shock",
        "cluster": "Mobility_Rail",
        "factor": 1.20,
        "duration": 4,
        "plateau": 2,
        "decay": 0.18,
        "name": "Vertrauensverlust Bahn — Resilienz-Debatte nach Sabotage",
        "attack_type": "trust_erosion",
        "source": "Civey Mobilitaetsumfragen Q4 2022"
    },

    # ---- 2023: Cyber-Druck + Hitze ----
    {
        "month": "Jun 2023",
        "type": "capacity_shock",
        "cluster": "Platform",
        "factor": 0.78,
        "duration": 3,
        "plateau": 1,
        "decay": 0.22,
        "name": "MOVEit Transfer (CVE-2023-34362) — Cl0p-Welle, Massendatenleck breite Branchen",
        "attack_type": "ransomware_extortion",
        "actor": "CL0P (russischsprachig)",
        "source": "Mandiant 2023; BSI Lagebericht 2023"
    },
    {
        # KORREKTUR: Aug -> Jul (Hitzewelle 2023 hatte Hoehepunkt Jul 24./25.)
        "month": "Jul 2023",
        "type": "variability_shock",
        "cluster": "Operations",
        "factor": 1.18,
        "duration": 4,
        "plateau": 2,
        "decay": 0.15,
        "name": "Hitzewelle Juli 2023 — vermehrte Schienen-Stoerungen, Oberleitungen, Stellwerks-Hitzeschutz",
        "attack_type": "environmental",
        "source": "DB-Berichte; DWD-Klimadaten 2023"
    },

    # ---- 2024: Streiks + Riedbahn + CrowdStrike + DFS-Cyber ----
    {
        # KORREKTUR: Praezisiert. Jan 2024: 10.-12.1. (3 Tage) + 24.-29.1. (6 Tage).
        # 35h-Wellenstreiks gab es eigentlich im Maerz (12./13.3.).
        "month": "Jan 2024",
        "type": "supply_shock",
        "cluster": "Operations",
        "factor": 0.45,
        "duration": 3,
        "plateau": 2,
        "decay": 0.30,
        "name": "GDL-Streiks Jan 2024 — 10.-12.1. + 24.-29.1. (6-Tage-Streik), Fernverkehr massiv reduziert",
        "attack_type": "strike",
        "actor": "GDL / DB-Tarifkonflikt",
        "source": "DB Geschaeftsbericht 2024; ADAC; bahndampf.de"
    },
    {
        "month": "Jan 2024",
        "type": "migration_shift",
        "cluster": "Mobility_Rail",
        "factor": 0.12,
        "duration": 4,
        "plateau": 2,
        "decay": 0.18,
        "name": "[Migration] Streik-bedingter Shift Bahn -> Auto/Homeoffice",
        "attack_type": "behavioral_shift",
        "source": "Civey/INSA Pendlerumfragen Q1 2024"
    },
    # Maerz-Wellenstreiks ergaenzt (faktisch der haerteste GDL-Block 2024)
    {
        "month": "Mar 2024",
        "type": "supply_shock",
        "cluster": "Operations",
        "factor": 0.50,
        "duration": 2,
        "plateau": 1,
        "decay": 0.35,
        "name": "GDL Wellenstreiks Maerz 2024 — sechster und letzter Streik (12./13.3.), Einigung 25.3.",
        "attack_type": "strike",
        "actor": "GDL / DB-Tarifkonflikt",
        "source": "GDL-Pressemitteilung 2024-03; DB-Pressemitteilung 2024-03"
    },
    {
        # KORREKTUR: praezisiert auf 15.07.-14.12.2024
        "month": "Jul 2024",
        "type": "capacity_shock",
        "cluster": "MainNodes",
        "factor": 0.40,
        "duration": 5,
        "plateau": 4,
        "decay": 0.18,
        "name": "Riedbahn-Generalsanierung (15.07.-14.12.2024) — 5 Mo. Vollsperrung Frankfurt-Mannheim, 70 km, 500 Mio. EUR",
        "attack_type": "scheduled_maintenance",
        "actor": "DB InfraGO",
        "source": "DB InfraGO Pressemeldung; riedbahn.de"
    },
    {
        "month": "Jul 2024",
        "type": "demand_shock",
        "cluster": "Logistics",
        "factor": 1.25,
        "duration": 5,
        "plateau": 3,
        "decay": 0.12,
        "name": "Riedbahn-Folge — Gueterverkehr-Umroutung, LKW-Substitution, Mehrkosten",
        "attack_type": "supply_disruption",
        "source": "VDV Gueterverkehrsstatistik 2024"
    },
    {
        # PRAEZISIERT: 19.07.2024, BER + Hamburg Airport stark betroffen, BSI Stufe 3
        "month": "Jul 2024",
        "type": "capacity_shock",
        "cluster": "Platform",
        "factor": 0.65,
        "duration": 1,
        "plateau": 1,
        "decay": 0.45,
        "name": "CrowdStrike Falcon-Update (19.07.2024) — ~8,5 Mio. Windows-BSOD weltweit, BER + Hamburg Airport, BSI Stufe 3",
        "attack_type": "vendor_misconfiguration",
        "actor": "CrowdStrike / Falcon Sensor",
        "source": "CISA Alert 2024-07-19; CrowdStrike RCA; BSI 2024-07-19"
    },
    # NEU: DFS-Cyberangriff (zentrales staatlich attribuiertes Verkehrs-Cyber-Event)
    {
        "month": "Aug 2024",
        "type": "capacity_shock",
        "cluster": "OT_IT_Bridge",
        "factor": 0.72,
        "duration": 3,
        "plateau": 1,
        "decay": 0.22,
        "name": "Cyber-Angriff Deutsche Flugsicherung (Aug 2024) — APT28/Fancy Bear, GRU attribuiert (offiziell 12.12.2025), Bueromission lahm, OT-Fluglotsen unberuehrt",
        "attack_type": "ot_it_compromise",
        "actor": "APT28 (Fancy Bear) / GRU",
        "source": "Auswaertiges Amt 2025-12-12; DFS-Bestaetigung 2024-09-01"
    },

    # ---- 2025: DORA, Eastwood, Mobilitaetsmonitor, Sabotage, H-B-Sperrung ----
    {
        # PRAEZISIERT: 17.01.2025 Geltung
        "month": "Jan 2025",
        "type": "capacity_increase",
        "cluster": "Security",
        "factor": 1.18,
        "duration": 8,
        "plateau": 5,
        "decay": 0.05,
        "name": "DORA-Geltung (17.01.2025) — operative Resilienz fuer Finanzsektor verpflichtend, DE KRITIS spillover",
        "attack_type": "regulatory_uplift",
        "source": "EU 2022/2554 (DORA), Geltung 17.01.2025"
    },
    # NEU/KORREKTUR: ersetzt das fiktive "ARD-Mobilitaetsmonitor Jun 2025"
    {
        "month": "Apr 2025",
        "type": "uncertainty_shock",
        "cluster": "Mobility_Rail",
        "factor": 1.15,
        "duration": 6,
        "plateau": 3,
        "decay": 0.10,
        "name": "acatech Mobilitaetsmonitor 2025 (08.04.2025) — 71% bewerten Schienennetz als schlecht, 2/3 der Stammnutzer mit Zugausfaellen",
        "attack_type": "trust_erosion",
        "source": "acatech / Allensbach 2025; ZDFheute 08.04.2025"
    },
    # NEU/KORREKTUR: ersetzt fiktives "NoName Mar 2025" durch Eastwood Jul 2025
    {
        "month": "Jul 2025",
        "type": "capacity_increase",
        "cluster": "Security",
        "factor": 1.12,
        "duration": 6,
        "plateau": 3,
        "decay": 0.08,
        "name": "Operation Eastwood (15.-17.07.2025) — BKA/ZIT zerschlagen NoName057(16)-Infrastruktur, 7 Partnerstaaten, hunderte Server abgeschaltet",
        "attack_type": "law_enforcement_uplift",
        "actor": "BKA / ZIT / Europol / Eurojust",
        "source": "BKA-Meldung 2025-07-16; Insikt Group 2025-07-22"
    },
    # NEU: Brandanschlag Duisburg-Duesseldorf
    {
        "month": "Aug 2025",
        "type": "capacity_shock",
        "cluster": "Regional",
        "factor": 0.62,
        "duration": 2,
        "plateau": 1,
        "decay": 0.30,
        "name": "Brandanschlaege Duisburg-Duesseldorf (31.07./01.08.2025) — 'Kommando Angry Birds', 700-800 Verbindungen/Tag, Flughafenanbindung lahm",
        "attack_type": "sabotage",
        "actor": "'Kommando Angry Birds' (klima-/industrieskeptisch)",
        "source": "ZDFheute 01.08.2025; NZZ 02.08.2025; DB-Pressemitteilung"
    },
    # NEU: Hamburg-Berlin Generalsanierung (zentraler Migration-Treiber)
    {
        "month": "Aug 2025",
        "type": "capacity_shock",
        "cluster": "MainNodes",
        "factor": 0.30,
        "duration": 11,  # bis Jun 2026
        "plateau": 9,
        "decay": 0.08,
        "name": "Hamburg-Berlin Generalsanierung (01.08.2025-13.06.2026) — 9 Mo. Vollsperrung 280 km, 30.000 Pendler/Tag, +45 min Umweg",
        "attack_type": "scheduled_maintenance",
        "actor": "DB InfraGO",
        "source": "hamburg-berlin.deutschebahn.com; VBB; ZDFheute 01.08.2025"
    },
    {
        "month": "Aug 2025",
        "type": "migration_shift",
        "cluster": "Mobility_Rail",
        "factor": 0.18,
        "duration": 11,
        "plateau": 9,
        "decay": 0.05,
        "name": "[Migration] Hamburg-Berlin-Sperrung — strukturelle Demand-Verlagerung Bahn -> Auto/Remote bei 30.000 Pendlern/Tag",
        "attack_type": "behavioral_shift",
        "source": "VBB; ADAC Bahnbaustellen 2025-2026"
    },
    {
        "month": "Aug 2025",
        "type": "demand_shock",
        "cluster": "Logistics",
        "factor": 1.30,
        "duration": 11,
        "plateau": 9,
        "decay": 0.06,
        "name": "Hamburg-Berlin-Folge — Seehafenhinterlandverkehr ueber Uelzen/Stendal/Hannover umgeleitet, Gueterverkehr ueberlastet",
        "attack_type": "supply_disruption",
        "source": "NEE (Netzwerk Europaeischer Eisenbahnen); DB InfraGO"
    },

    # ---- 2026: Sabotage-Welle vor Phase 2 ----
    # NEU: Stellwerk-Brand Hannover
    {
        "month": "Feb 2026",
        "type": "capacity_shock",
        "cluster": "Signaling",
        "factor": 0.60,
        "duration": 2,
        "plateau": 1,
        "decay": 0.30,
        "name": "Brandanschlag Stellwerk Hannover (~10.02.2026) — hunderte Fernzuege verspaetet",
        "attack_type": "sabotage",
        "actor": "Unbekannt (Staatsschutz ermittelt)",
        "source": "ZDFheute Feb 2026; dpa"
    },
    # NEU: DDoS DB
    {
        "month": "Feb 2026",
        "type": "capacity_shock",
        "cluster": "Platform",
        "factor": 0.55,
        "duration": 2,
        "plateau": 2,
        "decay": 0.40,
        "name": "DDoS-Grossangriff DB (17.02.2026) — bahn.de + DB-Navigator 2 Tage aus, BSI-Chefin Plattner: ungewoehnliche Dimension, Russland-Verdacht",
        "attack_type": "ddos",
        "actor": "Unattributed (RU-Bezug vermutet, BSI/dpa)",
        "source": "Bahnblogstelle 19.02.2026; Logistik Heute 18.02.2026; NZZ; security-insider.de"
    },
    {
        "month": "Feb 2026",
        "type": "uncertainty_shock",
        "cluster": "Sentiment",
        "factor": 1.18,
        "duration": 3,
        "plateau": 2,
        "decay": 0.18,
        "name": "Resilienz-Debatte nach Doppel-Schlag Stellwerk-Brand + DDoS — Vertrauensschock Verkehrsinfrastruktur",
        "attack_type": "trust_erosion",
        "source": "ARD/ZDF Feb 2026; Cybersecurity-Berichterstattung"
    },
    {
        "month": "Feb 2026",
        "type": "migration_shift",
        "cluster": "Mobility_Rail",
        "factor": 0.10,
        "duration": 3,
        "plateau": 2,
        "decay": 0.20,
        "name": "[Migration] Weitere Erosion Bahn-Loyalitaet — Sabotage- und Cyber-Wellen verstaerken Pendler-Wechsel",
        "attack_type": "behavioral_shift",
        "source": "HUK-Mobilitaetsstudie Vorabdaten; Civey Q1 2026"
    },
]


# --------------------------------------------------
# PHASE 2 — PATH A: RESILIENT (2026-06 bis 2030-12)
# --------------------------------------------------
EVENTS_PATH_A = [
    {
        "month": "Sep 2026",
        "type": "capacity_increase",
        "cluster": "Signaling",
        "factor": 1.20,
        "duration": 8,
        "plateau": 5,
        "decay": 0.05,
        "name": "[A] ETCS-Vollausbau Kernkorridore — Stellwerks-Resilienz steigt",
        "path": "resilient"
    },
    {
        "month": "Mar 2027",
        "type": "capacity_increase",
        "cluster": "Cloud",
        "factor": 1.15,
        "duration": 10,
        "plateau": 6,
        "decay": 0.05,
        "name": "[A] Multi-Cloud-Multi-Region DR-Programm abgeschlossen",
        "path": "resilient"
    },
    {
        "month": "Aug 2027",
        "type": "capacity_shock",
        "cluster": "Platform",
        "factor": 0.85,
        "duration": 2,
        "plateau": 1,
        "decay": 0.40,
        "name": "[A] Cyber-Vorfall — schnelle Eindaemmung, kurzer Impact",
        "attack_type": "ransomware",
        "actor": "Ransomware affiliate (unattributed)",
        "path": "resilient"
    },
    {
        "month": "Feb 2028",
        "type": "alliance_shift",
        "source_cluster": "Mobility_Rail",
        "target_cluster": "Mobility_Alt",
        "affinity_delta": 0.05,
        "factor": 1.0,
        "duration": 6,
        "plateau": 4,
        "decay": 0.04,
        "name": "[A] Multimodale Mobilitaet — Bahn + Carsharing/Bike koppeln staerker",
        "path": "resilient"
    },
    {
        "month": "Jun 2028",
        "type": "capacity_increase",
        "cluster": "MainNodes",
        "factor": 1.18,
        "duration": 8,
        "plateau": 5,
        "decay": 0.04,
        "name": "[A] Hochleistungskorridore Hamburg-Berlin generalsaniert in Betrieb",
        "path": "resilient"
    },
    {
        "month": "Apr 2029",
        "type": "capacity_increase",
        "cluster": "Logistics",
        "factor": 1.12,
        "duration": 6,
        "plateau": 4,
        "decay": 0.05,
        "name": "[A] Schienengueter-Marktanteil steigt, klimapolitische Steuerung wirkt",
        "path": "resilient"
    },
    {
        "month": "Sep 2030",
        "type": "uncertainty_shock",
        "cluster": "Sentiment",
        "factor": 1.05,
        "duration": 3,
        "plateau": 1,
        "decay": 0.25,
        "name": "[A] Marktstress-Episode — kurze Volatilitaetsphase, gut absorbiert",
        "path": "resilient"
    },
]


# --------------------------------------------------
# PHASE 2 — PATH B: HYBRID (2026-06 bis 2030-12)
# --------------------------------------------------
EVENTS_PATH_B = [
    {
        "month": "Aug 2026",
        "type": "capacity_shock",
        "cluster": "Signaling",
        "factor": 0.68,
        "duration": 3,
        "plateau": 2,
        "decay": 0.20,
        "name": "[B] Stellwerks-Stoerung Knoten Koeln — IT-Migration mit Konfig-Drift",
        "attack_type": "signal_failure",
        "path": "hybrid"
    },
    {
        "month": "Nov 2026",
        "type": "migration_shift",
        "cluster": "Mobility_Rail",
        "factor": 0.10,
        "duration": 5,
        "plateau": 3,
        "decay": 0.15,
        "name": "[B] [Migration] Pendler-Erosion durch Stoerhaeufung, Auto gewinnt",
        "path": "hybrid"
    },
    {
        "month": "Mar 2027",
        "type": "variability_shock",
        "cluster": "Network",
        "factor": 1.28,
        "duration": 4,
        "plateau": 2,
        "decay": 0.16,
        "name": "[B] DDoS-Hochsaison gegen Verkehrsportale, Mitigation auf Kante",
        "attack_type": "ddos",
        "actor": "Hacktivist coalition",
        "path": "hybrid"
    },
    {
        "month": "Jul 2027",
        "type": "capacity_shock",
        "cluster": "MainNodes",
        "factor": 0.62,
        "duration": 4,
        "plateau": 2,
        "decay": 0.18,
        "name": "[B] Korridor-Sperrung Mannheim-Stuttgart — Ausweichkapazitaet ueberlastet",
        "attack_type": "infrastructure_failure",
        "path": "hybrid"
    },
    {
        "month": "Jan 2028",
        "type": "capacity_shock",
        "cluster": "OT_IT_Bridge",
        "factor": 0.65,
        "duration": 3,
        "plateau": 1,
        "decay": 0.22,
        "name": "[B] Cyber-Vorfall Verkehrsleitstelle — laengere Containment-Phase",
        "attack_type": "ot_compromise",
        "actor": "State-nexus APT (unattributed)",
        "path": "hybrid"
    },
    {
        "month": "Jun 2028",
        "type": "uncertainty_shock",
        "cluster": "Sentiment",
        "factor": 1.22,
        "duration": 5,
        "plateau": 3,
        "decay": 0.14,
        "name": "[B] Konjunktur-Eintruebung, Investitionszurueckhaltung in Resilienz",
        "path": "hybrid"
    },
    {
        "month": "Oct 2028",
        "type": "migration_shift",
        "cluster": "Mobility_Rail",
        "factor": 0.08,
        "duration": 4,
        "plateau": 2,
        "decay": 0.18,
        "name": "[B] [Migration] Strukturelle Verlagerung Pendler -> Auto setzt sich fort",
        "path": "hybrid"
    },
    {
        "month": "May 2029",
        "type": "capacity_shock",
        "cluster": "Cloud",
        "factor": 0.70,
        "duration": 3,
        "plateau": 2,
        "decay": 0.18,
        "name": "[B] Hyperscaler-Region-Outage — Single-Region-Architektur betroffen",
        "attack_type": "cloud_outage",
        "actor": "Cloud provider incident",
        "path": "hybrid"
    },
    {
        "month": "Feb 2030",
        "type": "uncertainty_shock",
        "cluster": "Mobility_Rail",
        "factor": 1.18,
        "duration": 4,
        "plateau": 2,
        "decay": 0.15,
        "name": "[B] Vertrauen Bahn stagniert auf niedrigem Niveau",
        "path": "hybrid"
    },
]


# --------------------------------------------------
# PHASE 2 — PATH C: FRAGILE (2026-06 bis 2030-12)
# --------------------------------------------------
EVENTS_PATH_C = [
    {
        "month": "Jul 2026",
        "type": "capacity_shock",
        "cluster": "Cloud",
        "factor": 0.60,
        "duration": 4,
        "plateau": 2,
        "decay": 0.18,
        "name": "[C] Hyperscaler-Multi-Region-Outage — Single-Cloud-Architektur kollabiert",
        "attack_type": "cloud_outage",
        "actor": "Cloud provider incident + config drift",
        "path": "fragile"
    },
    {
        "month": "Sep 2026",
        "type": "capacity_shock",
        "cluster": "Signaling",
        "factor": 0.55,
        "duration": 3,
        "plateau": 2,
        "decay": 0.22,
        "name": "[C] Stellwerks-Komplettausfall Knoten Frankfurt — veraltete Technik",
        "attack_type": "signal_failure",
        "path": "fragile"
    },
    {
        "month": "Sep 2026",
        "type": "migration_shift",
        "cluster": "Mobility_Rail",
        "factor": 0.18,
        "duration": 6,
        "plateau": 3,
        "decay": 0.12,
        "name": "[C] [Migration] Vertrauenseinbruch — starker Shift Bahn -> Auto/Homeoffice",
        "attack_type": "behavioral_shift",
        "path": "fragile"
    },
    {
        "month": "Jan 2027",
        "type": "supply_shock",
        "cluster": "Operations",
        "factor": 0.50,
        "duration": 4,
        "plateau": 3,
        "decay": 0.20,
        "name": "[C] Tarifkonflikte + Personalmangel — laenger anhaltende Stoerungen",
        "attack_type": "strike",
        "path": "fragile"
    },
    {
        "month": "May 2027",
        "type": "capacity_shock",
        "cluster": "OT_IT_Bridge",
        "factor": 0.50,
        "duration": 4,
        "plateau": 2,
        "decay": 0.16,
        "name": "[C] Ransomware-Welle gegen Verkehrsleitstellen — Wochen-Recovery",
        "attack_type": "ransomware",
        "actor": "Ransomware affiliate (RaaS)",
        "path": "fragile"
    },
    {
        "month": "Aug 2027",
        "type": "uncertainty_shock",
        "cluster": "Sentiment",
        "factor": 1.35,
        "duration": 6,
        "plateau": 3,
        "decay": 0.10,
        "name": "[C] Kaskadensorge Wirtschaft + Markt — Investitions-Stopp",
        "path": "fragile"
    },
    {
        "month": "Dec 2027",
        "type": "migration_shift",
        "cluster": "Mobility_Rail",
        "factor": 0.15,
        "duration": 6,
        "plateau": 3,
        "decay": 0.10,
        "name": "[C] [Migration] Bahn-Anteil sinkt strukturell, Substitution dominiert",
        "path": "fragile"
    },
    {
        "month": "Apr 2028",
        "type": "capacity_shock",
        "cluster": "MainNodes",
        "factor": 0.45,
        "duration": 5,
        "plateau": 3,
        "decay": 0.15,
        "name": "[C] Bahn-Knoten Berlin/Muenchen kaskadische Ausfaelle — Wartungs-Schulden",
        "attack_type": "infrastructure_failure",
        "path": "fragile"
    },
    {
        "month": "Sep 2028",
        "type": "coupling_shift",
        "cluster": "Security",
        "factor": 0.72,
        "duration": 5,
        "plateau": 3,
        "decay": 0.10,
        "name": "[C] Identity-Federation-Bruch — Trust-Layer global geschwaecht",
        "attack_type": "identity_compromise",
        "actor": "Storm-class threat actor",
        "path": "fragile"
    },
    {
        "month": "Mar 2029",
        "type": "capacity_shock",
        "cluster": "Logistics",
        "factor": 0.60,
        "duration": 4,
        "plateau": 2,
        "decay": 0.18,
        "name": "[C] Schienengueter-Marktanteil bricht ein, LKW-Substitution kostspielig",
        "path": "fragile"
    },
    {
        "month": "Aug 2029",
        "type": "uncertainty_shock",
        "cluster": "Mobility_Rail",
        "factor": 1.40,
        "duration": 6,
        "plateau": 4,
        "decay": 0.10,
        "name": "[C] Politische Krise Bahn-Reform — Vertrauen Mehrjahrestief",
        "path": "fragile"
    },
    {
        "month": "Feb 2030",
        "type": "variability_shock",
        "cluster": "Network",
        "factor": 1.45,
        "duration": 4,
        "plateau": 2,
        "decay": 0.16,
        "name": "[C] Hypervolumetric-DDoS-Welle (>10 Tbps) — Mitigation ueberfordert",
        "attack_type": "ddos",
        "actor": "Hacktivist coalition + booter services",
        "path": "fragile"
    },
    {
        "month": "Jun 2030",
        "type": "capacity_shock",
        "cluster": "Platform",
        "factor": 0.55,
        "duration": 5,
        "plateau": 2,
        "decay": 0.16,
        "name": "[C] SaaS-Supply-Chain-Compromise — wochenlange Recovery, Spionage-Komponente",
        "attack_type": "supply_chain",
        "actor": "State-nexus APT (unattributed)",
        "path": "fragile"
    },
]


# --------------------------------------------------
# EXPORT: Vollstaendige Event-Sets pro Pfad
# --------------------------------------------------

def get_events(path="base"):
    """
    Gibt die vollstaendige Event-Liste fuer den gewaehlten Pfad zurueck.
    path: 'resilient' | 'hybrid' | 'fragile' | 'base' (nur historisch)
    """
    if path == "resilient":
        return EVENTS_HISTORICAL + EVENTS_PATH_A
    elif path == "hybrid":
        return EVENTS_HISTORICAL + EVENTS_PATH_B
    elif path == "fragile":
        return EVENTS_HISTORICAL + EVENTS_PATH_C
    else:
        return EVENTS_HISTORICAL


# --------------------------------------------------
# STOCHASTIC_PARAMS: Pfad-spezifische Parameter
#
# t=0 Initialbedingungen (Jan 2020) szenario-spezifisch begruendet:
#
#   initial_buffer       : Schockabsorptionsfaehigkeit
#                          (Multi-Cloud, ETCS-Reife, OT-Segmentierung,
#                           Wartungsbudget, Substitutionskapazitaet)
#   initial_stress_acc   : Latenter Vorstress
#                          (technische Schulden, IT-Altsysteme,
#                           Personalmangel, Schienennetz-Substanz)
#   initial_econ_scale   : Wirtschaftliche Ausgangslage
#                          (Investitionsklima, Lieferkettenrobustheit)
#   initial_supply_scale : Operative Versorgungskapazitaet
#                          (Betriebsreife, Wartungsdurchsatz)
#   initial_edge_scale   : Kopplungsqualitaet
#                          (OT/IT-Brueckenstabilitaet, Trust-Layer)
#   initial_trust_rail   : Sozialer Vertrauensanker fuer Mobility_Rail
#                          (Pendler-Loyalitaet, Reputations-Kapital)
#                          Steuert Cluster-Migration-Rate.
# --------------------------------------------------

STOCHASTIC_PARAMS = {
    "resilient": {
        # Projektionsphase
        "poisson_rate":   0.08,
        "beta_a": 2, "beta_b": 8,
        "coupling_decay": 0.012,
        "seed": 42,
        # t=0 Initialbedingungen
        # Hohe Bahn-Investitionen, ETCS-Vollausbau-Plan, Multi-Cloud,
        # robuste OT-Segmentierung, gepflegtes Schienennetz, hohe
        # Substitutionskapazitaet (Carsharing, multimodal).
        "initial_buffer":       0.82,
        "initial_stress_acc":   0.12,
        "initial_econ_scale":   1.00,
        "initial_supply_scale": 1.05,
        "initial_edge_scale":   1.00,
        # Sozialer Vertrauens-Anker Bahn: hoch -> wenig Migration
        "initial_trust_rail":   0.85,
        "migration_floor":      0.20,   # min. Rail_Commuter-Demand-Anteil
    },
    "hybrid": {
        # Projektionsphase
        "poisson_rate":   0.16,
        "beta_a": 2, "beta_b": 4,
        "coupling_decay": 0.022,
        "seed": 137,
        # t=0 Initialbedingungen
        # Teil-ETCS, Single-Cloud-Region fuer Kernservices, gemischte
        # OT-Modernisierung, Schienen-Wartungsstau, Personalmangel,
        # mittlere Substitutionskapazitaet.
        "initial_buffer":       0.60,
        "initial_stress_acc":   0.42,
        "initial_econ_scale":   0.94,
        "initial_supply_scale": 0.92,
        "initial_edge_scale":   0.90,
        "initial_trust_rail":   0.60,
        "migration_floor":      0.10,
    },
    "fragile": {
        # Projektionsphase
        "poisson_rate":   0.26,
        "beta_a": 3, "beta_b": 3,
        "coupling_decay": 0.045,
        "seed": 999,
        # t=0 Initialbedingungen
        # Veraltete Stellwerkstechnik (Bj. 70er/80er), zentralisierte
        # IT-Steuerung, OT/IT-Brueckenkompromittierung wahrscheinlich,
        # massiver Wartungsrueckstau, demografischer Personalengpass,
        # Substitution nur teilweise verfuegbar (laendliche Raeume).
        "initial_buffer":       0.40,
        "initial_stress_acc":   0.68,
        "initial_econ_scale":   0.86,
        "initial_supply_scale": 0.82,
        "initial_edge_scale":   0.84,
        "initial_trust_rail":   0.38,
        "migration_floor":      0.05,
    },
}
