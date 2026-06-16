from models.ue import UE
from models.salle import Salle


def verifier_planning(planning):

    erreurs = []

    occupation = {}

    for ligne in planning:

        ue_code = ligne["ue"]
        creneau = ligne["creneau"]
        salle_nom = ligne["salle"]

        ue = UE.query.filter_by(code=ue_code).first()
        salle = Salle.query.filter_by(nom=salle_nom).first()

        if not salle:
            erreurs.append(
                f"Salle introuvable pour {ue_code}"
            )
            continue

        cle = (creneau, salle.nom)

        if cle in occupation:
            erreurs.append(
                f"Conflit salle: {salle.nom} utilisee 2 fois a {creneau}"
            )
        else:
            occupation[cle] = ue_code

        if salle.capacite < ue.effectif:
            erreurs.append(
                f"Capacite insuffisante pour {ue_code} dans {salle.nom}"
            )

        if ue.besoin_labo and salle.type_salle != "labo":
            erreurs.append(
                f"UE {ue_code} necessite un labo"
            )

    return erreurs


def verifier_espace_filiere(planning):

    warnings = []

    filieres = {}
    for ligne in planning:
        ue_code = ligne["ue"]
        ue = UE.query.filter_by(code=ue_code).first()
        if ue.filiere not in filieres:
            filieres[ue.filiere] = []
        filieres[ue.filiere].append(
            (ligne["creneau_idx"], ue_code, ligne["creneau"])
        )

    for filiere, exams in filieres.items():

        exams_tries = sorted(exams, key=lambda x: x[0])

        for i in range(len(exams_tries) - 1):

            c1, ue1, label1 = exams_tries[i]
            c2, ue2, label2 = exams_tries[i + 1]

            if c2 - c1 == 1:
                warnings.append(
                    f"Filiere '{filiere}': "
                    f"{ue1} ({label1}) et "
                    f"{ue2} ({label2}) sont consecutifs"
                )

    return warnings


def verifier_charge_creneau(planning):

    compteurs = {}
    for ligne in planning:
        c = ligne["creneau"]
        compteurs[c] = compteurs.get(c, 0) + 1

    if not compteurs:
        return [], {}

    min_c = min(compteurs.values())
    max_c = max(compteurs.values())

    infos = {
        "par_creneau": compteurs,
        "moyenne": round(
            sum(compteurs.values()) / len(compteurs), 1
        ),
        "min": min_c,
        "max": max_c
    }

    warnings = []

    if max_c - min_c > 1:
        warnings.append(
            f"Charge desequilibree: "
            f"min={min_c}, max={max_c} examens/creneau"
        )

    return warnings, infos