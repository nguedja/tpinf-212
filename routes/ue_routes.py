from flask import Blueprint, render_template, request, redirect, url_for

from extensions import db
from models.ue import UE

ue_bp = Blueprint("ue", __name__)


@ue_bp.route("/ues")
def liste_ues():

    ues = UE.query.all()

    return render_template(
        "ues.html",
        ues=ues
    )

@ue_bp.route("/ues/ajouter", methods=["GET", "POST"])
def ajouter_ue():

    message = None

    if request.method == "POST":

        code = request.form["code"]

        # 🔴 Vérification anti-doublon
        existe = UE.query.filter_by(code=code).first()

        if existe:
            message = "❌ Ce code UE existe déjà !"
        else:
            ue = UE(
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

    return render_template("ajouter_ue.html", message=message)