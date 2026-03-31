import random
import copy
import math
from verification import compter_solution_V3


dictionnaire_liste_ligne = {}
dictionnaire_liste_colonne = {}
dictionnaire_liste_carre = {}

def generateur_grille_vide(dimension : int): 
    """
    Génère une matrice vide à la dimension démandée  
    """
    grille_vide = [[0] * dimension for i in range(dimension)]
    return(grille_vide)

def initialiser_dictionnaires(dimension : int):
    """
    Initialise les dictionnaires globaux contenant les valeurs possibles 
    pour chaque ligne, colonne et carré.
    
    Chaque dictionnaire contient une liste de chiffres de 1 à 'dimension'.
    Utilisé pour accélérer la recherche de candidats lors du remplissage
    """
    racine = int(math.sqrt(dimension))
    carre = int(racine)
    
    global dictionnaire_liste_ligne
    global dictionnaire_liste_colonne
    global dictionnaire_liste_carre

    dictionnaire_liste_ligne = {}
    dictionnaire_liste_colonne = {}
    dictionnaire_liste_carre = {}
    
    for i in range(dimension):
        dictionnaire_liste_ligne[i] = list(range(1, dimension + 1))
        dictionnaire_liste_colonne[i] = list(range(1, dimension + 1))
    
    for i in range(carre):
        dictionnaire_liste_carre[i] = {}
        
        for e in range(carre):
            dictionnaire_liste_carre[i][e] = list(range(1, dimension + 1))

def remplir_grilleV2(dimension : int):
    
    racine = int(math.sqrt(dimension))
    grille = generateur_grille_vide(dimension)
    initialiser_dictionnaires(dimension)
    essais = [[[] for _ in range(dimension)] for _ in range(dimension)]  # valeurs déjà essayées par les cases
    ligne = 0
    colonne = 0
    
    while ligne < dimension:
        candidats = list(set(dictionnaire_liste_ligne[ligne]) & set(dictionnaire_liste_colonne[colonne]) & set(dictionnaire_liste_carre[ligne//racine][colonne//racine]) - set(essais[ligne][colonne])) # Candidats = intersection des listes disponibles en retirant les valeurs déjà essayées
        
        if not candidats: # Pas de candidat : on remet les essais à zéro pour cette case et on recule
            essais[ligne][colonne] = []
            
            if colonne >= 1: # si on est pas sur la première colonne on recule de une colonne
                colonne -= 1
            
            else: # sinon on remonte à la ligne de dessus et on se met sur la dernière colonne de la ligne
                ligne -= 1
                colonne = dimension - 1
            
            if ligne < 0: 
                return None 
            val_precedente = grille[ligne][colonne] # On rerajoute la valeur de la case précédente dans les listes
            essais[ligne][colonne].append(val_precedente)  # on mémorise qu'elle a échoué
            dictionnaire_liste_ligne[ligne].append(val_precedente) # on rerajoute la valeur testé dans les liste de choix possible car on retourne en arrière
            dictionnaire_liste_carre[ligne//racine][colonne//racine].append(val_precedente)
            dictionnaire_liste_colonne[colonne].append(val_precedente)
            grille[ligne][colonne] = 0 
        
        else:
            valeur = random.choice(candidats) # On choisit une valeur et on avance
            grille[ligne][colonne] = valeur
            dictionnaire_liste_ligne[ligne].remove(valeur) # on retire la valeur tenté des choix possibles
            dictionnaire_liste_colonne[colonne].remove(valeur)
            dictionnaire_liste_carre[ligne//racine][colonne//racine].remove(valeur)
            
            if colonne == dimension - 1: 
                ligne += 1
                colonne = 0
            
            else:
                colonne += 1
    
    return (grille)

def supprimer_valeur(grille_complete : list[list:int], nombre_valeur_a_supprimer : int, dimension : int):
    """
    Transforme notre grille pleine en un sudoku à remplir.
    Tout en s'assurant que le joueur n'aura toujours qu'une seule solution possible.

    Entrée : 
        grille_a_vider: Une grille de Sudoku complète.
        nombre_valeurs_a_supprimer: Le nombre de cases que l'on veut vider.
        dimension : taille de notre grille
    Sortie : 
        grille_vidée : Une grille de Sudoku prête à être resolue par l'utilisateur
    """
    
    grille_vidée = copy.deepcopy(grille_complete)
    positions = [(ligne, colonne) for ligne in range(dimension) for colonne in range(dimension)]
    random.shuffle(positions)

    nombre_case_supprime = 0

    while nombre_case_supprime < nombre_valeur_a_supprimer:
        if not positions:
            # plus de positions → recommence avec nouvelle grille
            if (nombre_valeur_a_supprimer - nombre_case_supprime) > 5:   
                return supprimer_valeur(remplir_grilleV2(dimension), nombre_valeur_a_supprimer, dimension)
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

def generer_sudoku_consecutive(dimension):
    """Cette fonction crée une grille de sudoku_consecutif"""    

    grille_sudoku = remplir_grilleV2(dimension)
    
    duos = []
    for i in range(dimension):        # Création d'une liste qui va enregistrer toutes les cass adjacentes.
        for j in range(dimension):

            if j < dimension - 1:           # On enregistre la case de droite
                duos.append(((i, j), (i, j + 1)))       
            if i < dimension - 1:           # On enregistre la case du bas
                duos.append(((i, j), (i + 1, j)))

    duos_consecutifs = []

    for (i1, j1), (i2, j2) in duos:
        if abs(grille_sudoku[i1][j1] - grille_sudoku[i2][j2]) == 1:
            duos_consecutifs.append(((i1, j1), (i2, j2)))             # Si on a deux cases consécutives qui contiennent deux chiffres consecutifs on l'enregistre das la liste prévue a cet effet.
    
    grille_finale = supprimer_valeur(grille_sudoku, 60, 9)         # On supprime les valeurs de la grille pour avoir la version finales.

    return (grille_finale, duos_consecutifs)


print(generer_sudoku_consecutive(9))