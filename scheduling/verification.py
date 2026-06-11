from models.ue import UE
from models.salle import Salle


def verifier_planning(planning):

    erreurs = []

    # (creneau, salle) → UE
    occupation = {}

    for ligne in planning:

        ue_code = ligne["ue"]
        creneau = ligne["creneau"]
        salle_nom = ligne["salle"]

        ue = UE.query.filter_by(code=ue_code).first()
        salle = Salle.query.filter_by(nom=salle_nom).first()

        # ❌ cas salle introuvable
        if not salle:
            erreurs.append(f"Salle introuvable pour {ue_code}")
            continue

        # 1. salle déjà utilisée au même créneau
        cle = (creneau, salle.nom)

        if cle in occupation:
            erreurs.append(
                f"Conflit salle: {salle.nom} utilisée 2 fois au créneau {creneau}"
            )
        else:
            occupation[cle] = ue_code

        # 2. capacité insuffisante
        if salle.capacite < ue.effectif:
            erreurs.append(
                f"Capacité insuffisante pour {ue_code} dans {salle.nom}"
            )

        # 3. contrainte labo
        if ue.besoin_labo and salle.type_salle != "labo":
            erreurs.append(
                f"UE {ue_code} nécessite un labo"
            )

    return erreurs