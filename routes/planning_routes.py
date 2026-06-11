from flask import Blueprint, render_template

from graph.graphe import construire_graphe
from algorithms.dsatur import dsatur

from scheduling.affectation import affecter_salles
from scheduling.verification import verifier_planning
from scheduling.export_csv import exporter_csv


planning_bp = Blueprint("planning", __name__)


@planning_bp.route("/planning")
def planning():

    G = construire_graphe()

    coloration = dsatur(G)

    planning_final = affecter_salles(coloration)

    erreurs = verifier_planning(planning_final)

    fichier = exporter_csv(planning_final)

    return render_template(
        "planning.html",
        planning=planning_final,
        erreurs=erreurs,
        fichier=fichier
    )