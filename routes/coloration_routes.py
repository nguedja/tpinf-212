import time

from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    session
)

from graph.graphe import construire_graphe
from models.ue import UE

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

    etab_id = session.get("etablissement_id")

    if not etab_id:
        return redirect(
            url_for("etablissement.liste_etablissements")
        )

    G = construire_graphe(etab_id)

    effectifs = {
        ue.code: ue.effectif
        for ue in UE.query.filter_by(
            etablissement_id=etab_id
        ).all()
    }

    debut = time.time()
    wp = welsh_powell(G, effectifs)
    temps_wp = time.time() - debut

    debut = time.time()
    ds = dsatur(G)
    temps_ds = time.time() - debut

    return render_template(
        "coloration.html",
        wp=wp,
        ds=ds,
        nb_wp=len(set(wp.values())),
        nb_ds=len(set(ds.values())),
        temps_wp=round(temps_wp * 1000, 2),
        temps_ds=round(temps_ds * 1000, 2),
        nb_sommets=G.number_of_nodes(),
        nb_aretes=G.number_of_edges()
    )