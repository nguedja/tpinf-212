from flask import Blueprint, render_template

from graph.graphe import construire_graphe
from graph.visualisation import dessiner_graphe

graphe_bp = Blueprint(
    "graphe",
    __name__
)


@graphe_bp.route("/graphe")
def graphe():

    G = construire_graphe()

    dessiner_graphe(
        G,
        "static/images/graphe.png"
    )

    stats = {

        "sommets":
        G.number_of_nodes(),

        "aretes":
        G.number_of_edges(),

        "degres":
        dict(G.degree())
    }

    return render_template(
        "graphe.html",
        stats=stats
    )