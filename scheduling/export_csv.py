import csv
import os


def exporter_csv(planning, chemin="static/planning.csv"):

    os.makedirs(os.path.dirname(chemin), exist_ok=True)

    creneaux = sorted(set(l["creneau"] for l in planning))
    salles = sorted(set(l["salle"] for l in planning))

    cellules = {}
    for l in planning:
        cellules[(l["creneau"], l["salle"])] = (
            f"{l['ue']} ({l['effectif']})"
        )

    with open(chemin, mode="w", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)

        writer.writerow(["Creneau \\ Salle"] + salles)

        for c in creneaux:

            ligne = [f"{c}"]

            for s in salles:

                ligne.append(
                    cellules.get((c, s), "")
                )

            writer.writerow(ligne)

    return chemin