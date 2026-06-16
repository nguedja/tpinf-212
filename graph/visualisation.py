import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import networkx as nx


def dessiner_graphe(G, chemin, coloration=None):

    plt.figure(figsize=(8, 6))

    pos = nx.spring_layout(G, seed=42)

    if coloration:

        couleurs = [
            coloration.get(noeud, 0)
            for noeud in G.nodes()
        ]

        plt.title("Graphe colore (chaque couleur = un creneau)")

    else:

        couleurs = "#4A90D9"

        plt.title("Graphe des conflits")

    nx.draw(
        G,
        pos,
        with_labels=True,
        node_size=2000,
        node_color=couleurs,
        cmap=plt.cm.Set3,
        edgecolors="black",
        font_size=8
    )

    plt.savefig(chemin, dpi=150, bbox_inches="tight")

    plt.close()