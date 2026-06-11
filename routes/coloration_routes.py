from flask import Blueprint, render_template

from graph.graphe import construire_graphe

from algorithms.welsh_powell import (
    welsh_powell
)

from algorithms.dsatur import (
    dsatur
)

coloration_bp = Blueprint(
    "coloration",
    __name__
)


@coloration_bp.route("/coloration")
def coloration():

    G = construire_graphe()

    wp = welsh_powell(G)

    ds = dsatur(G)

    return render_template(
        "coloration.html",
        wp=wp,
        ds=ds,
        nb_wp=len(set(wp.values())),
        nb_ds=len(set(ds.values()))
    )