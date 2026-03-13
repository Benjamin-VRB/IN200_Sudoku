def verifier_unicite_kenken(dimension, cages, limite=2):

    compteur_de_solution = 0

    liste_ligne = [[True]*dimension for _ in range(dimension)]
    liste_colonne = [[True]*dimension for _ in range(dimension)]

    grille = [[0]*dimension for _ in range(dimension)]

    essaie = [(i,j) for i in range(dimension) for j in range(dimension)]


    def verifier_cage(cage):

        operation = cage["opération"]
        resultat = cage["résultat"]
        cases = cage["cases"]

        valeurs = []

        for (i,j) in cases:
            if grille[i][j] == 0:
                return True
            valeurs.append(grille[i][j])

        if operation == "+":
            return sum(valeurs) == resultat

        if operation == "*":
            produit = 1
            for v in valeurs:
                produit *= v
            return produit == resultat

        if operation == "-":
            a,b = valeurs
            return abs(a-b) == resultat

        if operation == "/":
            a,b = valeurs
            return max(a,b) // min(a,b) == resultat


    def cages_valides():

        for cage in cages.values():
            if not verifier_cage(cage):
                return False
        return True


    def solveur():
        nonlocal compteur_de_solution

        if compteur_de_solution >= limite:
            return

        if not essaie:
            compteur_de_solution += 1
            return

        indice_min = -1
        valeurs_possibles_min = []
        nb_valeurs_min = dimension + 1

        for idx,(ligne,colonne) in enumerate(essaie):

            valeurs_possibles = []

            for indice in range(dimension):

                if liste_ligne[ligne][indice] and liste_colonne[colonne][indice]:
                    valeurs_possibles.append(indice+1)

            nb_valeurs = len(valeurs_possibles)

            if nb_valeurs < nb_valeurs_min:
                nb_valeurs_min = nb_valeurs
                valeurs_possibles_min = valeurs_possibles
                indice_min = idx

            if nb_valeurs == 1:
                break

        if nb_valeurs_min == 0:
            return


        ligne,colonne = essaie.pop(indice_min)

        for valeur in valeurs_possibles_min:

            grille[ligne][colonne] = valeur

            liste_ligne[ligne][valeur-1] = False
            liste_colonne[colonne][valeur-1] = False

            if cages_valides():
                solveur()

            liste_ligne[ligne][valeur-1] = True
            liste_colonne[colonne][valeur-1] = True

            grille[ligne][colonne] = 0

            if compteur_de_solution >= limite:
                break


        essaie.insert(indice_min,(ligne,colonne))


    solveur()
    return compteur_de_solution
