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
from models.conflit import Conflit

conflit_bp = Blueprint("conflit", __name__)


def get_etab_id():
    return session.get("etablissement_id")


@conflit_bp.route("/conflits")
def liste_conflits():

    etab_id = get_etab_id()

    if not etab_id:
        return redirect(
            url_for("etablissement.liste_etablissements")
        )

    conflits = Conflit.query.filter_by(
        etablissement_id=etab_id
    ).all()

    return render_template(
        "conflits.html",
        conflits=conflits
    )


@conflit_bp.route(
    "/conflits/ajouter",
    methods=["GET", "POST"]
)
def ajouter_conflit():

    etab_id = get_etab_id()

    if not etab_id:
        return redirect(
            url_for("etablissement.liste_etablissements")
        )

    if request.method == "POST":

        conflit = Conflit(
            etablissement_id=etab_id,
            ue1_id=request.form["ue1"],
            ue2_id=request.form["ue2"]
        )

        db.session.add(conflit)
        db.session.commit()

        return redirect(url_for("conflit.liste_conflits"))

    ues = UE.query.filter_by(
        etablissement_id=etab_id
    ).all()

    return render_template(
        "ajouter_conflit.html",
        ues=ues
    )