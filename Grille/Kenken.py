import random
import vérification_Kenken

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


def generer_cages_remplies(grille, taille_min=2, taille_max=10):
    n = len(grille)
    cases_disponibles = [(i,j) for i in range(n) for j in range(n)]  # Liste de toutes les cases de la grille sous forme de tuples.
    random.shuffle(cases_disponibles)       # Mélange de ces cases pour en prendre une aléatoirement après.
    cages = []

    while cases_disponibles:
        case = cases_disponibles.pop()
        cage = [case]

        taille_max_possible = min(taille_max, len(cases_disponibles)+1) # on ajuste les valeurs possibles pour le nombre de case par cages.
        taille_min_possible = min(taille_min, taille_max_possible)
        taille_cage = random.randint(taille_min_possible, taille_max_possible) # Choisit aléatoirement le nombre de cases par cages
    
        
        while len(cage) < taille_cage:
            voisins = []
            for (i,j) in cage:   # On cherche les voisins possibles des cases déjà dans la cage.
                for ni,nj in [(i-1,j),(i+1,j),(i,j-1),(i,j+1)]:   # On fait en sorte que les conditions soent respéctées
                    if 0 <= ni < n and 0 <= nj < n \
                       and (ni,nj) in cases_disponibles \
                       and (ni,nj) not in cage:
                       voisins.append((ni,nj)) # Tous les voisins valides sont ajoutés à la liste des voisins.

            if not voisins:  # Si il n'ya pas de voisins valides , on arrete le processus
                break
            nouveau = random.choice(voisins)   # on choisit un voisin aléatoirement parmis ceux disponibles.
            cage.append(nouveau)  # On l'ajoute à la cage 
            cases_disponibles.remove(nouveau) #puis on le supprime de la liste des cases disponibles

        cages.append(cage)

    return cages


def générer_grille_KenKen(taille, max_case):
    global cages_finales
    while True:
        grille = remplir_grille(taille)  
        if grille is None:
            continue  

        cages = generer_cages_remplies(grille, taille_min=2, taille_max=max_case)  

        if sum(len(cage) for cage in cages) == taille * taille:
            break  

    cages_finales = {}
    for position in cages:   # On choisit aléatoirement une opération qu'on éxécute dans une cage et on rend un dictionnaire qui nous donne toutes les informations d'une cage.
        if len(position) == 2 and (grille[position[0][0]][position[0][1]] % grille[position[1][0]][position[1][1]] == 0 or grille[1][0] % grille[1][1] == 0):
            opération = random.choice(["+", "*", "-", "/", "/", "/", "/", "/"])
        elif len(position) == 2 and abs(grille[position[0][0]][position[0][1]] - grille[position[1][0]][position[1][1]]) != 0:
            opération = random.choice(["+", "*", "-", "-", "-"])
        else:
            opération =random.choice(["+", "*"])

        if opération == "+":
            compteur = 0
            for j in position:
                k, l = j
                compteur += grille[k][l]
            cages_finales["cage" + str(cages.index(position) + 1)] = {"opération" : "+", "résultat" : compteur, "cases": position}

        if opération == "*":
            compteur = 1
            for j in position:
                k, l = j
                compteur *= grille[k][l]
            cages_finales["cage" + str(cages.index(position) + 1)] = {"opération" : "*", "résultat" : compteur, "cases": position}

        if opération == "-":
            a = grille[position[0][0]][position[0][1]]
            b = grille[position[1][0]][position[1][1]]
            compteur = max(a,b) - min(a,b)
            cages_finales["cage" + str(cages.index(position) + 1)] = {"opération": "-", "résultat": compteur, "cases": position}


        if opération == "/":
            a = grille[position[0][0]][position[0][1]]
            b = grille[position[1][0]][position[1][1]]
            compteur = max(a,b) / min(a,b)  
            cages_finales["cage" + str(cages.index(position) + 1)] = {"opération": "/", "résultat": compteur, "cases": position}
    
    global grille_générée
    grille_générée = grille
    
    return grille, cages_finales

a = générer_grille_KenKen(6, 4)

while vérification_Kenken.verifier_unicite_kenken(6, cages_finales, limite=2) != 1:
    a = générer_grille_KenKen(6, 4)

print(a)