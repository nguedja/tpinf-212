def welsh_powell(G):

    couleurs = {}

    sommets = sorted(
        G.nodes(),
        key=lambda x: G.degree(x),
        reverse=True
    )

    couleur = 0

    for sommet in sommets:

        if sommet not in couleurs:

            couleurs[sommet] = couleur

            for autre in sommets:

                if autre not in couleurs:

                    voisin = False

                    for voisin_sommet in G.neighbors(autre):

                        if (
                            voisin_sommet in couleurs
                            and
                            couleurs[voisin_sommet] == couleur
                        ):
                            voisin = True
                            break

                    if not voisin:
                        couleurs[autre] = couleur

            couleur += 1

    return couleurs