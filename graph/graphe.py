import networkx as nx

from models.ue import UE
from models.conflit import Conflit


def construire_graphe():

    G = nx.Graph()

    ues = UE.query.all()

    for ue in ues:

        G.add_node(
            ue.code
        )

    conflits = Conflit.query.all()

    for conflit in conflits:

        G.add_edge(
            conflit.ue1.code,
            conflit.ue2.code
        )

    return G