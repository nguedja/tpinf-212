from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session
)

from extensions import db
from models.creneau import Creneau

creneau_bp = Blueprint("creneau", __name__)


def get_etab_id():
    return session.get("etablissement_id")


@creneau_bp.route("/creneaux")
def liste_creneaux():

    etab_id = get_etab_id()

    if not etab_id:
        return redirect(
            url_for("etablissement.liste_etablissements")
        )

    creneaux = Creneau.query.filter_by(
        etablissement_id=etab_id
    ).order_by(
        Creneau.jour,
        Creneau.heure_debut
    ).all()

    return render_template(
        "creneaux.html",
        creneaux=creneaux
    )


@creneau_bp.route(
    "/creneaux/ajouter",
    methods=["GET", "POST"]
)
def ajouter_creneau():

    etab_id = get_etab_id()

    if not etab_id:
        return redirect(
            url_for("etablissement.liste_etablissements")
        )

    if request.method == "POST":

        creneau = Creneau(
            etablissement_id=etab_id,
            label=request.form["label"],
            heure_debut=request.form["heure_debut"],
            heure_fin=request.form["heure_fin"],
            jour=request.form["jour"]
        )

        db.session.add(creneau)
        db.session.commit()

        return redirect(
            url_for("creneau.liste_creneaux")
        )

    return render_template("ajouter_creneau.html")


@creneau_bp.route(
    "/creneaux/supprimer/<int:id>",
    methods=["POST"]
)
def supprimer_creneau(id):

    creneau = Creneau.query.get_or_404(id)

    db.session.delete(creneau)
    db.session.commit()

    return redirect(
        url_for("creneau.liste_creneaux")
    )
