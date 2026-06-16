from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session
)

from extensions import db
from models.etudiant import Etudiant
from models.ue import UE
from models.inscription import Inscription

etudiant_bp = Blueprint("etudiant", __name__)


def get_etab_id():
    return session.get("etablissement_id")


@etudiant_bp.route("/etudiants")
def liste_etudiants():

    etab_id = get_etab_id()

    if not etab_id:
        return redirect(
            url_for("etablissement.liste_etablissements")
        )

    etudiants = Etudiant.query.filter_by(
        etablissement_id=etab_id
    ).all()

    return render_template(
        "etudiants.html",
        etudiants=etudiants
    )


@etudiant_bp.route(
    "/etudiants/ajouter",
    methods=["GET", "POST"]
)
def ajouter_etudiant():

    etab_id = get_etab_id()

    if not etab_id:
        return redirect(
            url_for("etablissement.liste_etablissements")
        )

    message = None

    if request.method == "POST":

        matricule = request.form["matricule"]

        existe = Etudiant.query.filter_by(
            matricule=matricule,
            etablissement_id=etab_id
        ).first()

        if existe:
            message = "Ce matricule existe deja !"
        else:
            etudiant = Etudiant(
                etablissement_id=etab_id,
                matricule=matricule,
                nom=request.form["nom"],
                filiere=request.form["filiere"]
            )

            db.session.add(etudiant)
            db.session.commit()

            return redirect(
                url_for("etudiant.liste_etudiants")
            )

    return render_template(
        "ajouter_etudiant.html",
        message=message
    )


@etudiant_bp.route(
    "/etudiants/<int:id>/inscrire",
    methods=["GET", "POST"]
)
def inscrire_ue(id):

    etab_id = get_etab_id()

    if not etab_id:
        return redirect(
            url_for("etablissement.liste_etablissements")
        )

    etudiant = Etudiant.query.get_or_404(id)

    ues = UE.query.filter_by(
        etablissement_id=etab_id
    ).all()

    message = None

    if request.method == "POST":

        ue_id = int(request.form["ue_id"])

        existe = Inscription.query.filter_by(
            etudiant_id=id,
            ue_id=ue_id
        ).first()

        if existe:
            message = "Cet etudiant est deja inscrit a cette UE !"
        else:
            inscription = Inscription(
                etudiant_id=id,
                ue_id=ue_id
            )

            db.session.add(inscription)
            db.session.commit()

            return redirect(
                url_for("etudiant.inscrire_ue", id=id)
            )

    return render_template(
        "inscrire.html",
        etudiant=etudiant,
        ues=ues,
        message=message
    )


@etudiant_bp.route(
    "/etudiants/<int:etudiant_id>"
    "/desinscrire/<int:inscription_id>",
    methods=["POST"]
)
def desinscrire(etudiant_id, inscription_id):

    inscription = Inscription.query.get_or_404(
        inscription_id
    )

    db.session.delete(inscription)
    db.session.commit()

    return redirect(
        url_for("etudiant.inscrire_ue", id=etudiant_id)
    )
