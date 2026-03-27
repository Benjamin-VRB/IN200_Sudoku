"""def verifier_unicite_kenken(dimension, cages, limite=2):

    compteur = 0

    grille = [[0]*dimension for _ in range(dimension)]

    lignes = [[True]*dimension for _ in range(dimension)]
    colonnes = [[True]*dimension for _ in range(dimension)]

    cases_vides = [(i, j) for i in range(dimension) for j in range(dimension)]

    # 🔥 associer chaque case à sa cage
    case_vers_cage = {}
    for cage in cages.values():
        for case in cage["cases"]:
            case_vers_cage[case] = cage

    # 🔥 vérifier UNE seule cage
    def verifier_cage(i, j):

        cage = case_vers_cage[(i, j)]
        op = cage["opération"]
        res = cage["résultat"]

        valeurs = []
        vide = 0

        for (x, y) in cage["cases"]:
            v = grille[x][y]
            if v == 0:
                vide += 1
            else:
                valeurs.append(v)

        # ➕
        if op == "+":
            s = sum(valeurs)
            if s > res:
                return False
            if vide == 0:
                return s == res
            return True

        # ✖️
        if op == "*":
            p = 1
            for v in valeurs:
                p *= v
            if p > res:
                return False
            if vide == 0:
                return p == res
            return True

        # ➖
        if op == "-":
            if vide > 0:
                return True
            a, b = valeurs
            return abs(a - b) == res

        # ➗
        if op == "/":
            if vide > 0:
                return True
            a, b = valeurs
            return max(a,b) % min(a,b) == 0 and max(a,b)//min(a,b) == res

        return True

    # 🔥 choisir la meilleure case (MRV)
    def choisir_case():
        best = None
        min_nb = dimension + 1
        best_vals = None

        for (i, j) in cases_vides:

            vals = []
            for v in range(dimension):
                if lignes[i][v] and colonnes[j][v]:
                    vals.append(v+1)

            if not vals:
                return None, None

            if len(vals) < min_nb:
                min_nb = len(vals)
                best = (i, j)
                best_vals = vals

            if min_nb == 1:
                break

        return best, best_vals

    def solve():
        nonlocal compteur

        if compteur >= limite:
            return

        if not cases_vides:
            compteur += 1
            return

        case, valeurs = choisir_case()

        if case is None:
            return

        i, j = case
        cases_vides.remove(case)

        for v in valeurs:

            # placer
            grille[i][j] = v
            lignes[i][v-1] = False
            colonnes[j][v-1] = False

            if verifier_cage(i, j):
                solve()

            # enlever
            grille[i][j] = 0
            lignes[i][v-1] = True
            colonnes[j][v-1] = True

            if compteur >= limite:
                break

        cases_vides.append(case)

    solve()
    return compteur

"""

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