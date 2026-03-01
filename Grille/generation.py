import random
import copy
import math
from verification import compte_solutions

dictionnaire_liste_ligne = {}
dictionnaire_liste_colonne = {}
dictionnaire_liste_carre = {}

def generateur_liste_valeur (nombre_de_valeur):
    liste=[[i] for i in range(nombre_de_valeur)]

def generateur_grille_vide (nombre_de_valeur): 
    grille_vide = [[0] * nombre_de_valeur for i in range(nombre_de_valeur)]
    return (grille_vide)

def initialiser_dictionnaires(nombre_de_valeur):
    racine = int(math.sqrt(nombre_de_valeur))
    carre = int(racine)
    
    global dictionnaire_liste_ligne
    global dictionnaire_liste_colonne
    global dictionnaire_liste_carre

    dictionnaire_liste_ligne = {}
    dictionnaire_liste_colonne = {}
    dictionnaire_liste_carre = {}
    
    for i in range(nombre_de_valeur):
        dictionnaire_liste_ligne[i] = list(range(1, nombre_de_valeur + 1))
        dictionnaire_liste_colonne[i] = list(range(1, nombre_de_valeur + 1))
    
    for i in range(carre):
        dictionnaire_liste_carre[i] = {}
        
        for e in range(carre):
            dictionnaire_liste_carre[i][e] = list(range(1, nombre_de_valeur + 1))

def grille_remplie(nombre_de_valeur):
    
    racine = int(math.sqrt(nombre_de_valeur))
    grille = generateur_grille_vide(nombre_de_valeur)
    initialiser_dictionnaires(nombre_de_valeur)
    essais = [[[] for _ in range(nombre_de_valeur)] for _ in range(nombre_de_valeur)]  # valeurs déjà essayées par les cases
    ligne = 0
    colonne = 0
    
    while ligne < nombre_de_valeur:
        candidats = list(set(dictionnaire_liste_ligne[ligne]) & set(dictionnaire_liste_colonne[colonne]) & set(dictionnaire_liste_carre[ligne//racine][colonne//racine]) - set(essais[ligne][colonne])) # Candidats = intersection des listes disponibles en retirant les valeurs déjà essayées
        
        if not candidats: # Pas de candidat : on remet les essais à zéro pour cette case et on recule
            essais[ligne][colonne] = []
            
            if colonne >= 1: # si on est pas sur la première colonne on recule de une colonne
                colonne -= 1
            
            else: # sinon on remonte à la ligne de dessus et on se met sur la dernière colonne de la ligne
                ligne -= 1
                colonne = nombre_de_valeur - 1
            
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
            
            if colonne == nombre_de_valeur - 1: 
                ligne += 1
                colonne = 0
            
            else:
                colonne += 1
    
    return (grille)

def suppression_valeur(grille_a_vider, nombre_valeur_a_supprimer, nombre_de_valeur):
    
    grille_vider = copy.deepcopy(grille_a_vider)  # copie de la grille envoyant à une autre liste indépendante 
    nombre_case_supprimer = 0
    positions = [(i,e) for i in range(nombre_de_valeur) for e in range(nombre_de_valeur)]
    
    while nombre_case_supprimer < nombre_valeur_a_supprimer: # on tente de supprimer tent que on est pas au nombre de case voulu
        position_tente = random.choice(positions)
        ligne, colonne = position_tente[0], position_tente[1]
        symetrique_ligne, symetrique_colonne = nombre_de_valeur-ligne-1, nombre_de_valeur-1-colonne  # coordonnées du symétrique
        valeur_1 = grille_vider[ligne][colonne] # sauvegarde des valeurs avant suppression
        valeur_2 = grille_vider[symetrique_ligne][symetrique_colonne] # sauvegarde du symétrique par rapport au centre pour pouvoire supprimer de case par deux
        grille_test = copy.deepcopy(grille_vider) # on tente la suppression
        grille_test[ligne][colonne] = 0
        grille_test[symetrique_ligne][symetrique_colonne] = 0
        
        if compte_solutions(grille_test, nombre_de_valeur) == 1: # verifie l'unicité de la solution
            grille_vider = grille_test
            nombre_case_supprimer += 2
            positions.remove(position_tente)
            if (symetrique_ligne, symetrique_colonne) in positions: # on retire le symétrique si il est dans les positions
                positions.remove((symetrique_ligne, symetrique_colonne))
    
        else:
            grille_test[ligne][colonne] = valeur_1 # on remet case 1, garde case 2 vide
            
            if compte_solutions(grille_test,nombre_de_valeur) == 1: # on retest l'unicité de la solution
                grille_vider = grille_test 
                nombre_case_supprimer += 1
                positions.remove(position_tente)
            
            else:
                grille_test[ligne][colonne] = 0 # on vide case 1
                grille_test[symetrique_ligne][symetrique_colonne] = valeur_2 # on remet case 2
                
                if compte_solutions(grille_test, nombre_de_valeur) == 1: # on retest l'unicité de la solution
                    grille_vider = grille_test
                    nombre_case_supprimer += 1
                    positions.remove(position_tente)
                
                else:
                    positions.remove(position_tente)
        
            if len(positions) == 0: # Verifie la présence de nouvelle solution possible
            
                if (nombre_valeur_a_supprimer - nombre_case_supprimer) > 1: # verifie si on a le bon nombre de valeur
                    grille_vider = copy.deepcopy(grille_remplie(nombre_de_valeur)) # si l'écart est trop grand, il recomence avec une autre grille
                return suppression_valeur(grille_vider, nombre_valeur_a_supprimer, nombre_de_valeur) 
            
            else:
                break # sinon il s'arrete la et renvoie la grille comme elle est
    
    return grille_vider
