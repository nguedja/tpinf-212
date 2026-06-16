from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    session
)

from graph.graphe import (
    construire_graphe,
    matrice_adjacence,
    liste_adjacence
)
from graph.visualisation import dessiner_graphe

graphe_bp = Blueprint(
    "graphe",
    __name__
)


@graphe_bp.route("/graphe")
def graphe():

    etab_id = session.get("etablissement_id")

    if not etab_id:
        return redirect(
            url_for("etablissement.liste_etablissements")
        )

    G = construire_graphe(etab_id)

    dessiner_graphe(
        G,
        "static/images/graphe.png"
    )

    noeuds, matrice = matrice_adjacence(G)

    liste = liste_adjacence(G)

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
        stats=stats,
        noeuds=noeuds,
        matrice=matrice,
        liste=liste
    )