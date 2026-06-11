from flask import Blueprint, render_template, request, redirect, url_for

from extensions import db
from models.salle import Salle

salle_bp = Blueprint("salle", __name__)


@salle_bp.route("/salles")
def liste_salles():

    salles = Salle.query.all()

    return render_template(
        "salles.html",
        salles=salles
    )


@salle_bp.route("/salles/ajouter", methods=["GET", "POST"])
def ajouter_salle():

    if request.method == "POST":

        salle = Salle(
            nom=request.form["nom"],
            capacite=int(request.form["capacite"]),
            type_salle=request.form["type_salle"]
        )

        db.session.add(salle)
        db.session.commit()

        return redirect(url_for("salle.liste_salles"))

    return render_template("ajouter_salle.html")