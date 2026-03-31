import random

dictionnaire_liste_ligne = {}
dictionnaire_liste_colonne = {}




def generateur_grille_vide(nombre_de_valeur):       # Fonction qui génère une grille de dimenseion quelconque.
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
    """Fonction qui génère aléatoirement des "cages" dans la grille de Sudoku générée précedemment.
    
    Entrée:
        Grille de sudoku générée, la taille minimale des cages, et la taille maximale des cages.
        
    Sortie:
        Liste contenant la liste de toutes les cases de chaque cages"""
    
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
            cases_disponibles.remove(nouveau) # puis on le supprime de la liste des cases disponibles

        cages.append(cage)

    return cages





def générer_grille_KenKen(taille : int, max_case : int):
    """Fonction qui génère une grille de Kenken complète avec les gages munies de leur opération et du 
    résultat de cette opération.
    
    Entrée:
        Taille de la grille qu'il faut générer et le maximum de cases à mettre par cages.
        
    Sortie:
        Grille générée + Dictionnaire dont les clés sont le numéros des cages et dont les valeurs sont un dictionnaire 
        contenant toutes les informations de la cages (opérations, résultats, cages concernées)."""


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

        if opération == "+":   # Si le + a été choisit, on effectue cette opération dans la cage et on la garde en mémoire dans le dictionnaire correspondant.
            compteur = 0
            for j in position:
                k, l = j
                compteur += grille[k][l]
            cages_finales["cage" + str(cages.index(position) + 1)] = {"opération" : "+", "résultat" : compteur, "cases": position}

        if opération == "*":  # Si le * a été choisit, on effectue cette opération dans la cage et on la garde en mémoire dans le dictionnaire correspondant.
            compteur = 1
            for j in position:
                k, l = j
                compteur *= grille[k][l]
            cages_finales["cage" + str(cages.index(position) + 1)] = {"opération" : "*", "résultat" : compteur, "cases": position}

        if opération == "-":   # Si le - a été choisit, on effectue cette opération dans la cage et on la garde en mémoire dans le dictionnaire correspondant.
            a = grille[position[0][0]][position[0][1]]
            b = grille[position[1][0]][position[1][1]]
            compteur = max(a,b) - min(a,b)
            cages_finales["cage" + str(cages.index(position) + 1)] = {"opération": "-", "résultat": compteur, "cases": position}


        if opération == "/":   # Si le / a été choisit, on effectue cette opération dans la cage et on la garde en mémoire dans le dictionnaire correspondant.
            a = grille[position[0][0]][position[0][1]]
            b = grille[position[1][0]][position[1][1]]
            compteur = max(a,b) / min(a,b)  
            cages_finales["cage" + str(cages.index(position) + 1)] = {"opération": "/", "résultat": compteur, "cases": position}

    return grille, cages_finales





def verifier_unicite_kenken(dimension, cages, limite=2):
    """Fonction qui compte le nombre de solutions de ma grille de Kenken.
    
    Entrée:
        Dimensions de la grille à étudier, dictionnaire contenant les cages et limite du nombre de 
        solutions à ne pas atteindre.
        
    Sortie:
        Renvoie True si le compteur est egal à 1 et False sinon."""

    compteur_de_solution = 0

    liste_ligne = [[True]*dimension for _ in range(dimension)]  # Création d'une liste pour les termes des lignes.
    liste_colonne = [[True]*dimension for _ in range(dimension)]  # Création d'une liste pour les termes des colonnes.

    grille = [[0]*dimension for k in range(dimension)]    # Création d'une matrice nulle.

    essaie = [(i,j) for i in range(dimension) for j in range(dimension)]  # création s'une matrice d'essais...


    def verifier_cage(cage):
        """Fonction qui vérifie les opéraions dans les cages
        
        Entrée:
            dictionnaire contenant les informations d'UNE cage.
            
        Sortie:
            Renvoie True si les valeurs rentrée vérifient bien le résultat et l'opération et False sinon."""

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


    def cages_valides():
        """Fonction qui vérifie la validité des cages dans tous le dictionnaire contenant les infos.
        --> Renvoie True si toutes les cages sont valides et False sinon."""
        for cage in cages.values():
            if not verifier_cage(cage):
                return False
        return True


    def solveur():
        """Fonction qui compte le nombre de solutions d'une grille.
        Cette fonction incrémente un compteur qui est une variable nonlocal
        Elle ne renvoie rien."""
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
    return compteur_de_solution == 1







def retourner_infos(dimensions):
    """Fonction qui génère et affiche une les infos d'une grille de Kenken.
    
    Entrée:
        Dimensions de la grille que l'on veut générer.
    
    sortie:
        Grille générée + dictionnaire contenant les infos de la grille."""

    a = générer_grille_KenKen(dimensions, 4)
    while not verifier_unicite_kenken(dimensions, cages_finales, limite=2):
        a = générer_grille_KenKen(dimensions, 4)
    print(a)


retourner_infos(5)