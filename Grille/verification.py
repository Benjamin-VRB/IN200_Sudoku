import math
import copy

def compter_solution_V3(grille : list[list:int], dimension : int, limite : int = 2):
    """
    Compte combien de solutions différentes possède une grille.
    Cela sert à verifier que notre grille a bien une unique solution.
    """
    # Booléens pour savoir si une valeur est utilisée
    liste_ligne = [[True] * dimension for _ in range(dimension)]
    liste_colonne = [[True] * dimension for _ in range(dimension)]
    liste_carre = [[True] * dimension for _ in range(dimension)]
    
    racine = int(math.sqrt(dimension))
    essaie = []  # liste des cases vides
    compteur_de_solution = 0

    # Initialisation
    for ligne in range(dimension):
        for colonne in range(dimension):
            valeur = grille[ligne][colonne]
            if valeur == 0:
                essaie.append((ligne,colonne))
            else:
                indice_valeur = valeur - 1
                liste_ligne[ligne][indice_valeur] = False
                liste_colonne[colonne][indice_valeur] = False
                liste_carre[(ligne // racine) * racine + (colonne // racine)][indice_valeur] = False

    def solveur():
        nonlocal compteur_de_solution

        if compteur_de_solution >= limite:
            return

        if not essaie:  # plus de case à remplir
            compteur_de_solution += 1
            return

        # MRV : choisir la case avec le moins de valeurs possibles
        indice_min = -1
        valeurs_possibles_min = []
        nb_valeurs_min = dimension + 1

        for idx, (ligne, colonne) in enumerate(essaie):
            numero_carre = (ligne // racine) * racine + (colonne // racine)
            
            valeurs_possibles = []

            for indice in range(dimension):
                if liste_ligne[ligne][indice] and liste_colonne[colonne][indice] and liste_carre[numero_carre][indice]:
                    valeurs_possibles.append(indice)
            
            nb_valeurs = len(valeurs_possibles)
            
            if nb_valeurs < nb_valeurs_min:
                nb_valeurs_min = nb_valeurs
                valeurs_possibles_min = valeurs_possibles
                indice_min = idx
            
            if nb_valeurs == 1:
                break  # optimisation

        if nb_valeurs_min == 0:
            return  # abandon

        # Retirer la case choisie
        ligne, colonne = essaie.pop(indice_min)
        numero_carre = (ligne // racine) * racine + (colonne // racine)

        for indice in valeurs_possibles_min:
            # Marquer la valeur comme utilisée
            liste_ligne[ligne][indice] = False
            liste_colonne[colonne][indice] = False
            liste_carre[numero_carre][indice] = False

            solveur()  # récursion

            # Backtracking
            liste_ligne[ligne][indice] = True
            liste_colonne[colonne][indice] = True
            liste_carre[numero_carre][indice] = True

            if compteur_de_solution >= limite:
                break

        # Réinsertion pour les appels supérieurs
        essaie.insert(indice_min, (ligne, colonne))

    solveur()
    return compteur_de_solution
