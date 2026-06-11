from models.ue import UE
from models.salle import Salle


def affecter_salles(coloration):

    planning = []

    salles = Salle.query.all()

    occupations = {}

    for code_ue, creneau in coloration.items():

        ue = UE.query.filter_by(
            code=code_ue
        ).first()

        salle_trouvee = None

        for salle in salles:

            # capacité insuffisante

            if salle.capacite < ue.effectif:
                continue

            # besoin de laboratoire

            if ue.besoin_labo:

                if salle.type_salle != "labo":
                    continue

            # salle déjà utilisée
            # dans ce créneau

            cle = (
                creneau,
                salle.id
            )

            if cle in occupations:
                continue

            salle_trouvee = salle

            occupations[cle] = True

            break

        planning.append({

            "ue": ue.code,

            "creneau": creneau,

            "salle":
            salle_trouvee.nom
            if salle_trouvee
            else "AUCUNE SALLE"

        })

    return planning