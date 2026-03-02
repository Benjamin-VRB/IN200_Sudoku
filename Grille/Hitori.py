import random
import copy
import math

dictionnaire_liste_ligne = {}
dictionnaire_liste_colonne = {}

def generateur_grille_vide(nombre_de_valeur): 
    grille_vide = [[0] * nombre_de_valeur for i in range(nombre_de_valeur)]
    return(grille_vide)
def initialiser_dictionnaires(nombre_de_valeur):
    
    global dictionnaire_liste_ligne
    global dictionnaire_liste_colonne

    dictionnaire_liste_ligne = {}
    dictionnaire_liste_colonne = {}
    
    for i in range(nombre_de_valeur):
        dictionnaire_liste_ligne[i] = list(range(1, nombre_de_valeur + 1))
        dictionnaire_liste_colonne[i] = list(range(1, nombre_de_valeur + 1))

def remplir_grille(nombre_de_valeur):
    
    racine = int(math.sqrt(nombre_de_valeur))
    grille = generateur_grille_vide(nombre_de_valeur)
    initialiser_dictionnaires(nombre_de_valeur)
    essais = [[[] for _ in range(nombre_de_valeur)] for _ in range(nombre_de_valeur)]  # valeurs déjà essayées par les cases
    ligne = 0
    colonne = 0
    
    while ligne < nombre_de_valeur:
        candidats = list(set(dictionnaire_liste_ligne[ligne]) & set(dictionnaire_liste_colonne[colonne]) - set(essais[ligne][colonne])) # Candidats = intersection des listes disponibles en retirant les valeurs déjà essayées
        
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
            dictionnaire_liste_colonne[colonne].append(val_precedente)
            grille[ligne][colonne] = 0 
        
        else:
            valeur = random.choice(candidats) # On choisit une valeur et on avance
            grille[ligne][colonne] = valeur
            dictionnaire_liste_ligne[ligne].remove(valeur) # on retire la valeur tenté des choix possibles
            dictionnaire_liste_colonne[colonne].remove(valeur)
            
            if colonne == nombre_de_valeur - 1: 
                ligne += 1
                colonne = 0
            
            else:
                colonne += 1
    
    return (grille)

a = remplir_grille(10)
for i in range(10):
    print(a[i])
