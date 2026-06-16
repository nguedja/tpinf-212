import networkx as nx

from models.ue import UE
from models.conflit import Conflit
from models.inscription import Inscription
from models.interdiction import Interdiction
from models.etudiant import Etudiant


def construire_graphe(etablissement_id):

    G = nx.Graph()

    ues = UE.query.filter_by(
        etablissement_id=etablissement_id
    ).all()

    for ue in ues:
        G.add_node(ue.code)

    conflits = Conflit.query.filter_by(
        etablissement_id=etablissement_id
    ).all()

    for conflit in conflits:
        G.add_edge(
            conflit.ue1.code,
            conflit.ue2.code
        )

    etudiants = Etudiant.query.filter_by(
        etablissement_id=etablissement_id
    ).all()

    etudiant_ids = [e.id for e in etudiants]

    inscriptions = Inscription.query.filter(
        Inscription.etudiant_id.in_(etudiant_ids)
    ).all()

    ue_par_etudiant = {}
    for insc in inscriptions:
        eid = insc.etudiant_id
        if eid not in ue_par_etudiant:
            ue_par_etudiant[eid] = []
        ue_par_etudiant[eid].append(insc.ue.code)

    for codes in ue_par_etudiant.values():
        for i in range(len(codes)):
            for j in range(i + 1, len(codes)):
                if not G.has_edge(codes[i], codes[j]):
                    G.add_edge(codes[i], codes[j])

    for i in range(len(ues)):
        for j in range(i + 1, len(ues)):
            if ues[i].professeur == ues[j].professeur:
                if not G.has_edge(ues[i].code, ues[j].code):
                    G.add_edge(ues[i].code, ues[j].code)

    interdictions = Interdiction.query.filter_by(
        etablissement_id=etablissement_id
    ).all()

    for inter in interdictions:
        if not G.has_edge(inter.ue1.code, inter.ue2.code):
            G.add_edge(inter.ue1.code, inter.ue2.code)

    return G


def matrice_adjacence(G):

    noeuds = sorted(G.nodes())
    n = len(noeuds)
    index = {noeud: i for i, noeud in enumerate(noeuds)}

    matrice = [[0] * n for _ in range(n)]

    for u, v in G.edges():
        matrice[index[u]][index[v]] = 1
        matrice[index[v]][index[u]] = 1

    return noeuds, matrice


def liste_adjacence(G):

    liste = {}

    for noeud in sorted(G.nodes()):
        liste[noeud] = sorted(G.neighbors(noeud))

    return liste