from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session
)

from extensions import db
from models.ue import UE

ue_bp = Blueprint("ue", __name__)


def get_etab_id():
    return session.get("etablissement_id")


@ue_bp.route("/ues")
def liste_ues():

    etab_id = get_etab_id()

    if not etab_id:
        return redirect(
            url_for("etablissement.liste_etablissements")
        )

    ues = UE.query.filter_by(
        etablissement_id=etab_id
    ).all()

    return render_template(
        "ues.html",
        ues=ues
    )


@ue_bp.route("/ues/ajouter", methods=["GET", "POST"])
def ajouter_ue():

    etab_id = get_etab_id()

    if not etab_id:
        return redirect(
            url_for("etablissement.liste_etablissements")
        )

    message = None

    if request.method == "POST":

        code = request.form["code"]

        existe = UE.query.filter_by(
            code=code,
            etablissement_id=etab_id
        ).first()

        if existe:
            message = "Ce code UE existe deja !"
        else:
            ue = UE(
                etablissement_id=etab_id,
                code=code,
                nom=request.form["nom"],
                filiere=request.form["filiere"],
                professeur=request.form["professeur"],
                effectif=int(request.form["effectif"]),
                besoin_labo=("besoin_labo" in request.form)
            )

            db.session.add(ue)
            db.session.commit()

            return redirect(url_for("ue.liste_ues"))

    return render_template(
        "ajouter_ue.html",
        message=message
    )