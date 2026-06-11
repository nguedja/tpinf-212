from flask import Blueprint, render_template, request, redirect, url_for

from extensions import db
from models.ue import UE
from models.conflit import Conflit

conflit_bp = Blueprint("conflit", __name__)


@conflit_bp.route("/conflits")
def liste_conflits():

    conflits = Conflit.query.all()

    return render_template(
        "conflits.html",
        conflits=conflits
    )


@conflit_bp.route("/conflits/ajouter", methods=["GET", "POST"])
def ajouter_conflit():

    if request.method == "POST":

        conflit = Conflit(
            ue1_id=request.form["ue1"],
            ue2_id=request.form["ue2"]
        )

        db.session.add(conflit)
        db.session.commit()

        return redirect(url_for("conflit.liste_conflits"))

    ues = UE.query.all()

    return render_template(
        "ajouter_conflit.html",
        ues=ues
    )