from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session
)

from extensions import db
from models.etablissement import Etablissement

etablissement_bp = Blueprint(
    "etablissement",
    __name__
)


@etablissement_bp.route(
    "/etablissements",
    methods=["GET", "POST"]
)
def liste_etablissements():

    etablissements = Etablissement.query.all()
    message = None

    if request.method == "POST":

        nom = request.form["nom"]

        existe = Etablissement.query.filter_by(
            nom=nom
        ).first()

        if existe:
            message = "Cet etablissement existe deja !"
        else:

            etab = Etablissement(
                nom=nom,
                adresse=request.form.get("adresse", "")
            )

            db.session.add(etab)
            db.session.commit()

            return redirect(
                url_for("etablissement.liste_etablissements")
            )

    return render_template(
        "etablissements.html",
        etablissements=etablissements,
        message=message
    )


@etablissement_bp.route(
    "/etablissements/selectionner/<int:id>"
)
def selectionner(id):

    session["etablissement_id"] = id

    return redirect(url_for("index"))


@etablissement_bp.route(
    "/etablissements/supprimer/<int:id>",
    methods=["POST"]
)
def supprimer(id):

    etab = Etablissement.query.get_or_404(id)

    db.session.delete(etab)
    db.session.commit()

    if session.get("etablissement_id") == id:
        session.pop("etablissement_id", None)

    return redirect(
        url_for("etablissement.liste_etablissements")
    )
