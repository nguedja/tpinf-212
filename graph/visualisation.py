import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import networkx as nx


def dessiner_graphe(G, chemin):

    plt.figure(figsize=(8, 6))

    pos = nx.spring_layout(G)

    nx.draw(
        G,
        pos,
        with_labels=True,
        node_size=2000
    )

    plt.savefig(chemin)

    plt.close()