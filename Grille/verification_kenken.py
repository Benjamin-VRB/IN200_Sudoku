def verifier_unicite_kenken(dimension, cages, limite=2):

    compteur_de_solution = 0

    liste_ligne = [[True]*dimension for _ in range(dimension)]  # Création d'une liste pour les termes des lignes.
    liste_colonne = [[True]*dimension for _ in range(dimension)]  # Création d'une liste pour les termes des colonnes.

    grille = [[0]*dimension for k in range(dimension)]    # Création d'une matrice nulle.

    essaie = [(i,j) for i in range(dimension) for j in range(dimension)]  # création s'une matrice d'essais...


    def verifier_cage(cage):      # Fonction qui teste les opérations dans les cages.

        operation = cage["opération"]
        resultat = cage["résultat"]
        cases = cage["cases"]

        valeurs = []

        for (i,j) in cases:  
            if grille[i][j] == 0:
                return True
            valeurs.append(grille[i][j])

        if operation == "+":     # Test pour le cas d'une somme
            return sum(valeurs) == resultat

        if operation == "*":     # Test pour le cas s'un produit
            produit = 1
            for v in valeurs:
                produit *= v
            return produit == resultat

        if operation == "-":     # Test pour le cas d'une différence
            a,b = valeurs
            return abs(a-b) == resultat

        if operation == "/":     # test pour le cas d'un quotient
            a,b = valeurs
            return max(a,b) // min(a,b) == resultat


    def cages_valides():   # Fonction qui vérifie vérifie la validité des cages.

        for cage in cages.values():
            if not verifier_cage(cage):
                return False
        return True


    def solveur():        # Fonction qui compte le nombre de solutions de la grille générée
        nonlocal compteur_de_solution

        if compteur_de_solution >= limite: # Si la limite (de deux solutions) et atteinte, on s'arrête.
            return

        if not essaie:   # S'il n'y plus de solutions à tester, on s'arrête et on renvoie la valeur du compteur 
            compteur_de_solution += 1
            return

        indice_min = -1        # On cherche la case avec le moins de valeurs possibles.
        valeurs_possibles_min = []
        nb_valeurs_min = dimension + 1

        for idx,(ligne,colonne) in enumerate(essaie):    # On regarde chaque case libre

            valeurs_possibles = []

            for indice in range(dimension):

                if liste_ligne[ligne][indice] and liste_colonne[colonne][indice]:
                    valeurs_possibles.append(indice + 1)

            nb_valeurs = len(valeurs_possibles)

            if nb_valeurs < nb_valeurs_min:   # On cherche de nouveau la case ayant le moins de choix possibles.
                nb_valeurs_min = nb_valeurs
                valeurs_possibles_min = valeurs_possibles
                indice_min = idx

            if nb_valeurs == 1:      # Si une case n'a qu'une seule valeur possible, on s'arrete pour cette case.
                break

        if nb_valeurs_min == 0:     # Si une case n'a pas de valeurs possibles, la combinaison testée n'est pas possible.
            return


        ligne,colonne = essaie.pop(indice_min)    # La case vient d'être "remplie". On l'enlève donc de la liste des cases vides.

        for valeur in valeurs_possibles_min:   

            grille[ligne][colonne] = valeur

            liste_ligne[ligne][valeur-1] = False
            liste_colonne[colonne][valeur-1] = False

            if cages_valides():       # On teste la validité des cages et on relance le solveur pour les cages vides restantes.
                solveur()

            liste_ligne[ligne][valeur-1] = True          # On annule le choix et on reautorise l'utilisation de la valeur en question. on recommence a zero pour une autre combinaison.
            liste_colonne[colonne][valeur-1] = True

            grille[ligne][colonne] = 0

            if compteur_de_solution >= limite:    # Si le compteur depasse la limite de 2 solutions, on s'arrete.
                break


        essaie.insert(indice_min,(ligne,colonne))


    solveur()
    return compteur_de_solution