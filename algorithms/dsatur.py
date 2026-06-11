def dsatur(G):

    couleurs = {}

    saturation = {
        sommet: 0
        for sommet in G.nodes()
    }

    degres = dict(G.degree())

    while len(couleurs) < len(G.nodes()):

        sommet = max(
            (
                s
                for s in G.nodes()
                if s not in couleurs
            ),
            key=lambda x:
            (
                saturation[x],
                degres[x]
            )
        )

        couleurs_voisines = {

            couleurs[v]

            for v in G.neighbors(sommet)

            if v in couleurs
        }

        couleur = 0

        while couleur in couleurs_voisines:
            couleur += 1

        couleurs[sommet] = couleur

        for voisin in G.neighbors(sommet):

            if voisin not in couleurs:

                saturation[voisin] = len(

                    {
                        couleurs[v]

                        for v in G.neighbors(voisin)

                        if v in couleurs
                    }

                )

    return couleurs