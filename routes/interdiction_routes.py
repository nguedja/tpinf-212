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
from models.interdiction import Interdiction

interdiction_bp = Blueprint(
    "interdiction",
    __name__
)


def get_etab_id():
    return session.get("etablissement_id")


@interdiction_bp.route("/interdictions")
def liste_interdictions():

    etab_id = get_etab_id()

    if not etab_id:
        return redirect(
            url_for("etablissement.liste_etablissements")
        )

    interdictions = Interdiction.query.filter_by(
        etablissement_id=etab_id
    ).all()

    return render_template(
        "interdictions.html",
        interdictions=interdictions
    )


@interdiction_bp.route(
    "/interdictions/ajouter",
    methods=["GET", "POST"]
)
def ajouter_interdiction():

    etab_id = get_etab_id()

    if not etab_id:
        return redirect(
            url_for("etablissement.liste_etablissements")
        )

    message = None

    if request.method == "POST":

        ue1_id = int(request.form["ue1"])
        ue2_id = int(request.form["ue2"])

        if ue1_id == ue2_id:
            message = "Impossible d'interdire une UE avec elle-meme !"
        else:

            existe = Interdiction.query.filter(
                (
                    (Interdiction.ue1_id == ue1_id)
                    & (Interdiction.ue2_id == ue2_id)
                )
                | (
                    (Interdiction.ue1_id == ue2_id)
                    & (Interdiction.ue2_id == ue1_id)
                )
            ).first()

            if existe:
                message = "Cette interdiction existe deja !"
            else:

                interdiction = Interdiction(
                    etablissement_id=etab_id,
                    ue1_id=ue1_id,
                    ue2_id=ue2_id,
                    raison=request.form.get(
                        "raison",
                        "Interdiction explicite"
                    )
                )

                db.session.add(interdiction)
                db.session.commit()

                return redirect(
                    url_for(
                        "interdiction.liste_interdictions"
                    )
                )

    ues = UE.query.filter_by(
        etablissement_id=etab_id
    ).all()

    return render_template(
        "ajouter_interdiction.html",
        ues=ues,
        message=message
    )


@interdiction_bp.route(
    "/interdictions/supprimer/<int:id>",
    methods=["POST"]
)
def supprimer_interdiction(id):

    interdiction = Interdiction.query.get_or_404(id)

    db.session.delete(interdiction)
    db.session.commit()

    return redirect(
        url_for("interdiction.liste_interdictions")
    )
