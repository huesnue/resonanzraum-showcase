"""
Critical Infrastructure Scenario Loader
========================================
Analog zu cyber_cloud.py / financial.py — laedt Nodes/Edges fuer das
Rail & Critical Infrastructure Resilience Scenario 2020-2030.

Pfad-Auswahl: 'resilient' | 'hybrid' | 'fragile'

Vier Cluster auf Makroebene (Vier-Raum-Architektur):
  digital  : Cloud-Plattform, IAM, Leitstelle (OT/IT), API-Gateway,
             Kommunikationsnetz
  rail     : Bahnknoten, Stellwerk/Signalisierung, Disposition,
             Wartungskapazitaet, Regionalnetz
  economic : Lieferkette, Gueterverkehr, Produktion, Dienstleistungen,
             Marktstimmung
  social   : Bahn-Pendler, Auto-Nutzer, Homeoffice, alternative
             Mobilitaet, Flugreisen

Brueckenkanten (type='bridge') verbinden die vier Raeume.
Neu gegenueber dem Drei-Raum-Cyber-Szenario: ein expliziter sozialer
Raum mit Substitutions-Kanten (type='substitution') fuer
Cluster-Migration zwischen Mobilitaetsformen.

IP-Hinweis: Keine R2M-Variablen oder Formeln exponiert.
Alle Groessen oeffentlich neutral benannt.
"""

import os
import copy
import csv


def _load_nodes_csv(path):
    nodes = {}
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            nid = row["id"]

            def f2(v, d=0.0):
                try:
                    return float(v)
                except (ValueError, TypeError):
                    return d

            nodes[nid] = {
                "id":           nid,
                "type":         row.get("type", "consumer"),
                "space":        row.get("space", "digital"),  # digital | rail | economic | social
                "cluster":      row.get("cluster", "default"),
                "supply":       f2(row.get("supply")),
                "demand":       f2(row.get("demand")),
                "capacity":     f2(row.get("capacity")),
                "fin_capacity": f2(row.get("fin_capacity")),
                "econ_output":  f2(row.get("econ_output")),
                "received":     0.0,
                "stress":       0.0,
                "status":       "active",
            }
    return nodes


def _load_edges_csv(path):
    edges = []
    with open(path, newline="") as f:
        for row in csv.DictReader(f):

            def f2(v, d=0.0):
                try:
                    return float(v)
                except (ValueError, TypeError):
                    return d

            edges.append({
                "source":   row["source"],
                "target":   row["target"],
                "capacity": f2(row.get("capacity")),
                "strength": f2(row.get("strength")),
                "type":     row.get("type", "default"),
                "flow":     0.0,
                "status":   "active",
            })
    return edges


def load_scenario(path="resilient"):
    """
    Laedt das Rail & Critical Infrastructure Resilience Scenario.

    path: 'resilient' | 'hybrid' | 'fragile'
    Gibt dict zurueck: {type, path, nodes, edges}
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "..", "data")
    nodes_path = os.path.join(data_dir, "critical_infra_nodes.csv")
    edges_path = os.path.join(data_dir, "critical_infra_edges.csv")

    nodes = _load_nodes_csv(nodes_path)
    edges = _load_edges_csv(edges_path)

    nodes = copy.deepcopy(nodes)
    edges = copy.deepcopy(edges)

    return {
        "type":  "critical_infra",
        "path":  path,
        "nodes": nodes,
        "edges": edges,
    }
