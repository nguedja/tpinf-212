from models.ue import UE
from models.salle import Salle
from models.creneau import Creneau


def affecter_salles(coloration, etablissement_id):

    planning = []

    salles = Salle.query.filter_by(
        etablissement_id=etablissement_id
    ).all()

    creneaux_db = Creneau.query.filter_by(
        etablissement_id=etablissement_id
    ).order_by(
        Creneau.jour,
        Creneau.heure_debut
    ).all()

    mapping_creneaux = {}
    for i, c in enumerate(creneaux_db):
        mapping_creneaux[i] = c

    occupations = {}

    for code_ue, creneau_idx in coloration.items():

        ue = UE.query.filter_by(
            code=code_ue,
            etablissement_id=etablissement_id
        ).first()

        creneau_obj = mapping_creneaux.get(creneau_idx)

        if creneau_obj:
            creneau_label = (
                f"{creneau_obj.jour} "
                f"{creneau_obj.heure_debut}-"
                f"{creneau_obj.heure_fin}"
            )
        else:
            creneau_label = f"Creneau {creneau_idx}"

        salle_trouvee = None

        for salle in salles:

            if salle.capacite < ue.effectif:
                continue

            if ue.besoin_labo:

                if salle.type_salle != "labo":
                    continue

            cle = (
                creneau_idx,
                salle.id
            )

            if cle in occupations:
                continue

            salle_trouvee = salle

            occupations[cle] = True

            break

        planning.append({

            "ue": ue.code,

            "effectif": ue.effectif,

            "creneau_idx": creneau_idx,

            "creneau": creneau_label,

            "jour": creneau_obj.jour if creneau_obj else "",

            "salle":
            salle_trouvee.nom
            if salle_trouvee
            else "AUCUNE SALLE"

        })

    return planning