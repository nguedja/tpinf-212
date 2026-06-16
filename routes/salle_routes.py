from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session
)

from extensions import db
from models.salle import Salle

salle_bp = Blueprint("salle", __name__)


def get_etab_id():
    return session.get("etablissement_id")


@salle_bp.route("/salles")
def liste_salles():

    etab_id = get_etab_id()

    if not etab_id:
        return redirect(
            url_for("etablissement.liste_etablissements")
        )

    salles = Salle.query.filter_by(
        etablissement_id=etab_id
    ).all()

    return render_template(
        "salles.html",
        salles=salles
    )


@salle_bp.route(
    "/salles/ajouter",
    methods=["GET", "POST"]
)
def ajouter_salle():

    etab_id = get_etab_id()

    if not etab_id:
        return redirect(
            url_for("etablissement.liste_etablissements")
        )

    if request.method == "POST":

        salle = Salle(
            etablissement_id=etab_id,
            nom=request.form["nom"],
            capacite=int(request.form["capacite"]),
            type_salle=request.form["type_salle"]
        )

        db.session.add(salle)
        db.session.commit()

        return redirect(url_for("salle.liste_salles"))

    return render_template("ajouter_salle.html")