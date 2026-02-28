import random
import copy

valeur_ligne_1 = [1,2,3,4,5,6,7,8,9]
valeur_ligne_2 = [1,2,3,4,5,6,7,8,9]
valeur_ligne_3 = [1,2,3,4,5,6,7,8,9]
valeur_ligne_4 = [1,2,3,4,5,6,7,8,9]
valeur_ligne_5 = [1,2,3,4,5,6,7,8,9]
valeur_ligne_6 = [1,2,3,4,5,6,7,8,9]
valeur_ligne_7 = [1,2,3,4,5,6,7,8,9]
valeur_ligne_8 = [1,2,3,4,5,6,7,8,9]
valeur_ligne_9 = [1,2,3,4,5,6,7,8,9]

dictionnaire_liste_ligne = {0 : valeur_ligne_1, 1 : valeur_ligne_2, 2 : valeur_ligne_3, 3 : valeur_ligne_4, 4 : valeur_ligne_5, 5 : valeur_ligne_6, 6 : valeur_ligne_7, 7 : valeur_ligne_8, 8 : valeur_ligne_9}

valeur_colonne_1 = [1,2,3,4,5,6,7,8,9]
valeur_colonne_2 = [1,2,3,4,5,6,7,8,9]
valeur_colonne_3 = [1,2,3,4,5,6,7,8,9]
valeur_colonne_4 = [1,2,3,4,5,6,7,8,9]
valeur_colonne_5 = [1,2,3,4,5,6,7,8,9]
valeur_colonne_6 = [1,2,3,4,5,6,7,8,9]
valeur_colonne_7 = [1,2,3,4,5,6,7,8,9]
valeur_colonne_8 = [1,2,3,4,5,6,7,8,9]
valeur_colonne_9 = [1,2,3,4,5,6,7,8,9]

dictionnaire_liste_colonne = {0 : valeur_colonne_1, 1 : valeur_colonne_2, 2 : valeur_colonne_3, 3 : valeur_colonne_4, 4 : valeur_colonne_5, 5 : valeur_colonne_6, 6 : valeur_colonne_7, 7 : valeur_colonne_8, 8 : valeur_colonne_9}

valeur_carre_1 = [1,2,3,4,5,6,7,8,9]
valeur_carre_2 = [1,2,3,4,5,6,7,8,9]
valeur_carre_3 = [1,2,3,4,5,6,7,8,9]
valeur_carre_4 = [1,2,3,4,5,6,7,8,9]
valeur_carre_5 = [1,2,3,4,5,6,7,8,9]
valeur_carre_6 = [1,2,3,4,5,6,7,8,9]
valeur_carre_7 = [1,2,3,4,5,6,7,8,9]
valeur_carre_8 = [1,2,3,4,5,6,7,8,9]
valeur_carre_9 = [1,2,3,4,5,6,7,8,9]

dictionnaire_valeur_1_a_3 = {0: valeur_carre_1, 1: valeur_carre_2, 2:valeur_carre_3}
dictionnaire_valeur_4_a_6 = {0: valeur_carre_4, 1: valeur_carre_5, 2:valeur_carre_6}
dictionnaire_valeur_7_a_9 = {0: valeur_carre_7, 1: valeur_carre_8, 2:valeur_carre_9}

dictionnaire_liste_carre = {0:dictionnaire_valeur_1_a_3 ,1:dictionnaire_valeur_4_a_6, 2:dictionnaire_valeur_7_a_9}

def generateur_grille_vide (): 
    grille_vide = [[0] * 9 for i in range(9)]
    return (grille_vide)

def reset_liste(): # reremplie les liste de valeur possible 
    for i in range(9):
        dictionnaire_liste_ligne[i][:] = [1,2,3,4,5,6,7,8,9]
        dictionnaire_liste_colonne[i][:] = [1,2,3,4,5,6,7,8,9]
    for i in range(3):
        for e in range(3):
            dictionnaire_liste_carre[i][e][:] = [1,2,3,4,5,6,7,8,9]

def grille_remplie():
    grille = generateur_grille_vide()
    reset_liste()
    essais = [[[] for _ in range(9)] for _ in range(9)]  # valeurs déjà essayées par les cases
    ligne = 0
    colonne = 0
    while ligne < 9:
        candidats = list(set(dictionnaire_liste_ligne[ligne]) & set(dictionnaire_liste_colonne[colonne]) & set(dictionnaire_liste_carre[ligne//3][colonne//3]) - set(essais[ligne][colonne])) # Candidats = intersection des listes disponibles en retirant les valeurs déjà essayées
        if not candidats: # Pas de candidat : on remet les essais à zéro pour cette case et on recule
            essais[ligne][colonne] = []
            if colonne >= 1: # si on est pas sur la première colonne on recule de une colonne
                colonne -= 1
            else: # sinon on remonte à la ligne de dessus et on se met sur la dernière colonne de la ligne
                ligne -= 1
                colonne = 8
            if ligne < 0: 
                return None 
            val_precedente = grille[ligne][colonne] # On rerajoute la valeur de la case précédente dans les listes
            essais[ligne][colonne].append(val_precedente)  # on mémorise qu'elle a échoué
            dictionnaire_liste_ligne[ligne].append(val_precedente) # on rerajoute la valeur testé dans les liste de choix possible car on retourne en arrière
            dictionnaire_liste_carre[ligne//3][colonne//3].append(val_precedente)
            dictionnaire_liste_colonne[colonne].append(val_precedente)
            grille[ligne][colonne] = 0 
        else:
            valeur = random.choice(candidats) # On choisit une valeur et on avance
            grille[ligne][colonne] = valeur
            dictionnaire_liste_ligne[ligne].remove(valeur) # on retire la valeur tenté des choix possibles
            dictionnaire_liste_colonne[colonne].remove(valeur)
            dictionnaire_liste_carre[ligne//3][colonne//3].remove(valeur)
            if colonne == 8: 
                ligne += 1
                colonne = 0
            else:
                colonne += 1
    
    return (grille)

def solveur(grille):
    for i in range(9): # Trouve la première case vide
        for e in range(9):
            if grille[i][e] == 0:
                for val in range(1, 10): # Teste toutes les valeurs possibles
                    if est_valide(grille, i, e, val):
                        grille[i][e] = val
                        if solveur(grille):
                            return True
                        grille[i][e] = 0
                return False  # Aucune valeur ne fonctionne retour en arrière
    return True  # solution trouvée

def est_valide(grille, ligne, colonne, valeur):
    if valeur in grille[ligne]: # Vérifie la ligne
        return False
    if any(grille[i][colonne] == valeur for i in range(9)):  # Vérifie la colonne
        return False
    ligne_0, colonne_0 = (ligne // 3) * 3, (colonne // 3) * 3 # Vérifie le carré 3x3
    return not any(grille[i][e] == valeur for i in range(ligne_0, ligne_0+3) for e in range(colonne_0, colonne_0+3))

def compte_solutions(grille, limite=2):
    compteur = [0] # Compte le nombre de solutions, s'arrête dès qu'on atteint la limite
    def resoudre():  
        if compteur[0] >= limite:
            return
        for i in range(9):
            for e in range(9):
                if grille[i][e] == 0:
                    for valeur in range(1, 10):
                        if est_valide(grille, i, e, valeur):
                            grille[i][e] = valeur
                            resoudre()
                            grille[i][e] = 0
                    return # case vide sans solution valide
        compteur[0] += 1 # grille complète trouvée
    resoudre()
    return compteur[0]

def suppression_valeur(grille_a_vider, nombre_valeur_a_supprimer):
    grille_vider = copy.deepcopy(grille_a_vider)  # copie de la grille envoyant à une autre liste indépendante 
    nombre_case_supprimer = 0
    positions = [(i,e) for i in range(9) for e in range(9)]
    while nombre_case_supprimer < nombre_valeur_a_supprimer: # on tente de supprimer tent que on est pas au nombre de case voulu
        position_tente = random.choice(positions)
        ligne, colonne = position_tente[0], position_tente[1]
        symetrique_ligne, symetrique_colonne = 8-ligne, 8-colonne  # coordonnées du symétrique
        valeur_1 = grille_vider[ligne][colonne] # sauvegarde des valeurs avant suppression
        valeur_2 = grille_vider[symetrique_ligne][symetrique_colonne] # sauvegarde du symétrique par rapport au centre pour pouvoire supprimer de case par deux
        grille_test = copy.deepcopy(grille_vider) # on tente la suppression
        grille_test[ligne][colonne] = 0
        grille_test[symetrique_ligne][symetrique_colonne] = 0
        if compte_solutions(grille_test) == 1: # verifie l'unicité de la solution
            grille_vider = grille_test
            nombre_case_supprimer += 2
            positions.remove(position_tente)
            if (symetrique_ligne, symetrique_colonne) in positions: # on retire le symétrique si il est dans les positions
                positions.remove((symetrique_ligne, symetrique_colonne))
        else:
            grille_test[ligne][colonne] = valeur_1 # on remet case 1, garde case 2 vide
            if compte_solutions(grille_test) == 1: # on retest l'unicité de la solution
                grille_vider = grille_test 
                nombre_case_supprimer += 1
                positions.remove(position_tente)
            else:
                grille_test[ligne][colonne] = 0 # on vide case 1
                grille_test[symetrique_ligne][symetrique_colonne] = valeur_2 # on remet case 2
                if compte_solutions(grille_test) == 1: # on retest l'unicité de la solution
                    grille_vider = grille_test
                    nombre_case_supprimer += 1
                    positions.remove(position_tente)
                else:
                    positions.remove(position_tente)
        if len(positions) == 0: # Verifie la présence de nouvelle solution possible
            if (nombre_valeur_a_supprimer - nombre_case_supprimer) > 1: # verifie si on a le bon nombre de valeur
                grille_vider = copy.deepcopy(grille_remplie()) # si l'écart est trop grand, il recomence avec une autre grille
                return suppression_valeur(grille_vider, nombre_valeur_a_supprimer) 
            else:
                break # sinon il s'arrete la et renvoie la grille comme elle est
    return grille_vider
