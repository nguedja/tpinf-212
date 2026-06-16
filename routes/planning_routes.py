from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    session,
    send_file
)

from graph.graphe import construire_graphe
from graph.visualisation import dessiner_graphe
from algorithms.dsatur import dsatur

from scheduling.affectation import affecter_salles
from scheduling.verification import (
    verifier_planning,
    verifier_espace_filiere,
    verifier_charge_creneau
)
from scheduling.export_csv import exporter_csv
from scheduling.export_pdf import exporter_pdf


planning_bp = Blueprint("planning", __name__)


@planning_bp.route("/planning")
def planning():

    etab_id = session.get("etablissement_id")

    if not etab_id:
        return redirect(
            url_for("etablissement.liste_etablissements")
        )

    G = construire_graphe(etab_id)

    coloration = dsatur(G)

    dessiner_graphe(
        G,
        "static/images/graphe_colore.png",
        coloration=coloration
    )

    planning_final = affecter_salles(coloration, etab_id)

    erreurs = verifier_planning(planning_final)

    warnings_filiere = verifier_espace_filiere(
        planning_final
    )

    warnings_charge, infos_charge = verifier_charge_creneau(
        planning_final
    )

    exporter_csv(planning_final)
    exporter_pdf(planning_final)

    nb_creneaux = len(set(
        l["creneau"] for l in planning_final
    ))

    seen_creneaux = []
    seen_salles = []
    for l in planning_final:
        if l["creneau"] not in seen_creneaux:
            seen_creneaux.append(l["creneau"])
        if l["salle"] not in seen_salles:
            seen_salles.append(l["salle"])

    return render_template(
        "planning.html",
        planning=planning_final,
        erreurs=erreurs,
        warnings_filiere=warnings_filiere,
        warnings_charge=warnings_charge,
        infos_charge=infos_charge,
        nb_creneaux=nb_creneaux,
        creneaux_list=seen_creneaux,
        salles_list=seen_salles
    )


@planning_bp.route("/planning/telecharger")
def telecharger_planning():

    return send_file(
        "static/planning.csv",
        as_attachment=True,
        download_name="planning.csv"
    )


@planning_bp.route("/planning/telecharger-pdf")
def telecharger_planning_pdf():

    return send_file(
        "static/planning.pdf",
        as_attachment=True,
        download_name="planning.pdf"
    )


