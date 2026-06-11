import csv
import os


def exporter_csv(planning, chemin="output/planning.csv"):

    os.makedirs(os.path.dirname(chemin), exist_ok=True)

    with open(chemin, mode="w", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)

        writer.writerow(["UE", "Créneau", "Salle"])

        for ligne in planning:

            writer.writerow([
                ligne["ue"],
                ligne["creneau"],
                ligne["salle"]
            ])

    return chemin