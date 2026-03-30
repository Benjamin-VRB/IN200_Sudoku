import math
import copy
import random

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

def generateur_grille_vide(dimension : int): 
    """
    Génère une matrice vide à la dimension démandée  
    """
    grille_vide = [[0] * dimension for i in range(dimension)]
    return(grille_vide)

def remplir_grille_V2(dimension : int):
    """
    Génère une grille de Sudoku complète en utilisant une stratégie de 
    Backtracking optimisée.

    L'optimisation réside dans le choix des cases à traiter : en prenant celle qui à le moins de chiffres possibles.
    """
    racine = int(math.sqrt(dimension))

    grille = generateur_grille_vide(dimension)

    liste_ligne = [[True]*dimension for _ in range(dimension)]
    liste_colonne = [[True]*dimension for _ in range(dimension)]
    liste_carre = [[True]*dimension for _ in range(dimension)]

    essaie = [(i,e) for i in range(dimension) for e in range(dimension)]

    def solveur():
        if not essaie:
            return True

        indice_min = -1
        valeurs_possibles_min = []
        nb_valeurs_min = dimension + 1

        for idx, (ligne, colonne) in enumerate(essaie):
            numero_carre = (ligne//racine)*racine + (colonne//racine)
            candidats = [v for v in range(dimension)
                         if liste_ligne[ligne][v] and
                            liste_colonne[colonne][v] and
                            liste_carre[numero_carre][v]]

            nb_valeurs = len(candidats)
            if nb_valeurs < nb_valeurs_min:
                nb_valeurs_min = nb_valeurs
                valeurs_possibles_min = candidats
                indice_min = idx
            if nb_valeurs == 1:
                break

        if nb_valeurs_min == 0 or indice_min == -1:
            return False

        ligne, colonne = essaie.pop(indice_min)
        numero_carre = (ligne//racine)*racine + (colonne//racine)
        random.shuffle(valeurs_possibles_min)

        for i in valeurs_possibles_min:
            grille[ligne][colonne] = i + 1
            liste_ligne[ligne][i] = False
            liste_colonne[colonne][i] = False
            liste_carre[numero_carre][i] = False

            if solveur():
                return True

            # backtrack
            grille[ligne][colonne] = 0
            liste_ligne[ligne][i] = True
            liste_colonne[colonne][i] = True
            liste_carre[numero_carre][i] = True

        essaie.insert(indice_min, (ligne, colonne))
        return False

    if solveur():  
        return grille
    else:
        return None
        
def supprimer_valeur(nombre_valeur_a_supprimer : int, dimension : int):
    """
    Transforme notre grille pleine en un sudoku à remplir.
    Tout en s'assurant que le joueur n'aura toujours qu'une seule solution possible.

    Entrée : 
        nombre_valeurs_a_supprimer: Le nombre de cases que l'on veut vider.
        dimension : taille de notre grille
    Sortie : 
        grille_vidée : Une grille de Sudoku prête à être resolue par l'utilisateur
    """
    grille_complet = remplir_grille_V2(dimension)
    grille_vidée = copy.deepcopy(grille_complete)
    positions = [(ligne, colonne) for ligne in range(dimension) for colonne in range(dimension)]
    random.shuffle(positions)

    nombre_case_supprime = 0

    while nombre_case_supprime < nombre_valeur_a_supprimer:
        if not positions:
            # plus de positions → recommence avec nouvelle grille
            if (nombre_valeur_a_supprimer - nombre_case_supprime) > 5:   
                return supprimer_valeur(remplir_grille(dimension), nombre_valeur_a_supprimer, dimension)
            else:
                return grille_vidée

        ligne, colonne = positions.pop()
        valeur_originale = grille_vidée[ligne][colonne]
        grille_vidée[ligne][colonne] = 0

        if compter_solution_V3(grille_vidée, dimension) == 1:
            nombre_case_supprime += 1
        else:
            grille_vidée[ligne][colonne] = valeur_originale

    return grille_vidée
