from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
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
    nouveau_code = None

    if request.method == "POST":

        nom = request.form["nom"]

        existe = Etablissement.query.filter_by(
            nom=nom
        ).first()

        if existe:
            message = "Cet etablissement existe deja !"
        else:

            code = Etablissement.generer_code()

            etab = Etablissement(
                nom=nom,
                adresse=request.form.get("adresse", ""),
                code=code
            )

            db.session.add(etab)
            db.session.commit()

            nouveau_code = code

    return render_template(
        "etablissements.html",
        etablissements=etablissements,
        message=message,
        nouveau_code=nouveau_code
    )


@etablissement_bp.route(
    "/etablissements/selectionner/<int:id>",
    methods=["GET", "POST"]
)
def selectionner(id):

    etab = Etablissement.query.get_or_404(id)

    if request.method == "POST":

        code_saisi = request.form.get("code", "")

        if code_saisi == etab.code:
            session["etablissement_id"] = id
            return redirect(url_for("index"))
        else:
            flash("Code incorrect !", "error")
            return redirect(
                url_for(
                    "etablissement.selectionner",
                    id=id
                )
            )

    return render_template(
        "confirmer_etablissement.html",
        etablissement=etab
    )


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
