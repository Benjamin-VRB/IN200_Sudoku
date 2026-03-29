import math
from Grille.verification import est_valide

def compter_solution_V2(grille : list[list:int], dimension : int, limite : int=2):
    ligne = [0] * dimension
    colonne = [0] * dimension
    carre = [0] * dimension
    essaie = []
    racine = int(math.sqrt(dimension))

    for i in range (dimension): # séparation des case remplie des case vide
        for e in range (dimension):
            valeur = grille[i][e]
            if valeur == 0:
                essaie.append((i, e))
            else :
                mask = 1 << (valeur - 1) # enregistrement de la valeur dans la ligne colonne et carre
                ligne[i] |= mask
                colonne[e] |= mask
                carre[(i // racine) * racine + (e // racine)] |= mask

    compteur_de_solution = 0

    def solve():
        nonlocal compteur_de_solution
        
        if compteur_de_solution >= limite: # on a donc au moins 2 solution, on arrete
            return
        
        if essaie == []: # si essaie vide, alors la grille est remplie, on à trouver une solution
            compteur_de_solution += 1
            return

        min_index = -1 
        min_mask = 0
        min_nombre_valeur_possible = dimension

        for h, (i, e) in enumerate(essaie): # enumeration de tout les couple h(indice dans la liste essaie) et des tuples (ligne, colonne)
            index_carre = (i // racine) * racine + (e // racine) # determination de l'indice du carre (de 0 a 8) (se représenter les carre et leur donner un numero de gauche à droite et de bas en haut
            bit_utilise = ligne[i] | colonne[e] | carre[index_carre] # determination des bit deja utilisé dans la ligne, colonne et carre de la valeur pour faire l'union des trois
            valeur_possible = (~bit_utilise) &  ((1 << dimension) - 1) # obtention de valeur possible par inversion de valeur interdite à valeur possible + limitation au 9 premier bits 
            nombre_de_valeur_possible = valeur_possible.bit_count() # compte le nombre de valeur possible

            if nombre_de_valeur_possible < min_nombre_valeur_possible: # recherche de la case avec le moins de valeur possible pour en retenir les infos
                min_nombre_valeur_possible = nombre_de_valeur_possible
                min_mask = valeur_possible
                min_index = h

            if nombre_de_valeur_possible == 1: # on arrete de cherche pour prendre le chemin
                break
        
        if min_nombre_valeur_possible == 0: # abandon du chemin
            return
        
        i, e = essaie.pop(min_index) # on retirer la case choisie de la liste des cases à essaiyer
        c = (i // racine) * racine + (e // racine)
        valeur_possible = min_mask # attribution comme valeur possible, celle déterminer plus tôt 
        
        while valeur_possible:  # boucle sur chaque valeur possible
            bit = valeur_possible & -valeur_possible # on prend le bit le plus faible
            valeur_possible ^= bit # on retire ce bit du masque 

            ligne[i] |= bit # Marquer le chiffre comme utilisé dans ligne, colonne et bloc
            colonne[e] |= bit
            carre[c] |= bit

            solve() # appel récursif pour remplir la prochaine case

            ligne[i] ^= bit  # annulation des choix (backtracking)
            colonne[e] ^= bit
            carre[c] ^= bit

            if compteur_de_solution >= limite: # stop si on atteint la limite
                break

        essaie.insert(min_index, (i, e))  # réinsertion de la case dans la liste pour les appels supérieurs

    solve() # début résolution récursive
    return compteur_de_solution # renvoie le nombre de solution trouvé

def compter_solution_V1(grille, dimension, limite=2):
    compteur = [0] # Compte le nombre de solutions, s'arrête dès qu'on atteint la limite
    def resoudre():  
        if compteur[0] >= limite:
            return
        for i in range(dimension):
            for e in range(dimension):
                if grille[i][e] == 0:
                    for valeur in range(1, dimension + 1):
                        if est_valide(grille, i, e, valeur, dimension):
                            grille[i][e] = valeur
                            resoudre()
                            grille[i][e] = 0
                    return # case vide sans solution valide
        compteur[0] += 1 # grille complète trouvée
    resoudre()
    return compteur[0]

def calculer_sommes(solution, groupes):
    return [sum(solution[i][j] for (i,j) in g) for g in groupes]

def remplir_grille_kakuro(grille):
    dimension = len(grille)
    groupes_h = trouver_groupes_horizontaux_kakuro(grille)
    groupes_v = trouver_groupes_verticaux_kakuro(grille)
    
    dict_h = {i: list(range(1,10)) for i in range(len(groupes_h))}
    dict_v = {i: list(range(1,10)) for i in range(len(groupes_v))}
    
    case_vers_groupes = {}
    for idx, g in enumerate(groupes_h):
        for (i,j) in g:
            case_vers_groupes[(i,j)] = case_vers_groupes.get((i,j), [None,None])
            case_vers_groupes[(i,j)][0] = idx
    for idx, g in enumerate(groupes_v):
        for (i,j) in g:
            case_vers_groupes[(i,j)] = case_vers_groupes.get((i,j), [None,None])
            case_vers_groupes[(i,j)][1] = idx
    
    solution = [[None]*dimension for _ in range(dimension)]
    cases = [(i,j) for i in range(dimension) for j in range(dimension) if grille[i][j] == 0]
    
    def backtrack(index):
        if index == len(cases):
            return True
        i,j = cases[index]
        g_h, g_v = case_vers_groupes[(i,j)]
        
        candidats = list(set(dict_h[g_h]) & set(dict_v[g_v]))
        random.shuffle(candidats)
        
        for val in candidats:
            solution[i][j] = val
            dict_h[g_h].remove(val)
            dict_v[g_v].remove(val)
            if backtrack(index+1):
                return True
            solution[i][j] = None
            dict_h[g_h].append(val)
            dict_v[g_v].append(val)
        return False
    
    if backtrack(0):
        return solution
    else:
        return None

def generer_kakuro(dimension):
    while True:
        masque = generer_masque_kakuro(dimension)
        if not valider_masque_kakuro(masque):
            continue
        
        solution = remplir_grille_kakuro(masque)
        if solution is None:
            continue
        
        groupes_h = trouver_groupes_horizontaux_kakuro(masque)
        groupes_v = trouver_groupes_verticaux_kakuro(masque)
        sommes_h = calculer_sommes(solution, groupes_h)
        sommes_v = calculer_sommes(solution, groupes_v)
        
        nb = compter_solution_kakuro(
            copy.deepcopy(masque),
            dimension,
            groupes_h,
            sommes_h,
            groupes_v,
            sommes_v,
            limite=2
        )
        if nb == 1:
            break  # succès
        
    return {
        "masque": masque,
        "solution": solution,
        "groupes_horizontaux": groupes_h,
        "groupes_verticaux": groupes_v,
        "sommes_horizontales": sommes_h,
        "sommes_verticales": sommes_v
    }

def is_valid_group(group):
    """Vérifie qu'il n'y a pas de doublon et que la somme est cohérente"""
    return len(set(group)) == len(group) and all(1 <= n <= 9 for n in group)

def solve_kakuro(grid, horizontal_groups, vertical_groups):
    """Solveur par backtracking pour garantir unicité."""
    rows, cols = len(grid), len(grid[0])
    solutions = []

    def backtrack(r, c):
        if r == rows:
            solutions.append([row[:] for row in grid])
            return len(solutions) <= 1  # Stop si plus d'une solution
        if c == cols:
            return backtrack(r + 1, 0)
        if grid[r][c] != 0:
            return backtrack(r, c + 1)

        # Identifier groupes horizontaux et verticaux
        for val in range(1, 10):
            grid[r][c] = val
            if all_valid(grid, horizontal_groups, vertical_groups):
                if not backtrack(r, c + 1):
                    grid[r][c] = 0
                    return False
            grid[r][c] = 0
        return True

    def all_valid(grid, h_groups, v_groups):
        for (r, c, length) in h_groups:
            vals = [grid[r][c+i] for i in range(length)]
            if 0 not in vals and len(set(vals)) != len(vals):
                return False
        for (r, c, length) in v_groups:
            vals = [grid[r+i][c] for i in range(length)]
            if 0 not in vals and len(set(vals)) != len(vals):
                return False
        return True

    backtrack(0, 0)
    return solutions

def generate_kakuro(rows, cols):
    """Génère une grille de Kakuro avec une seule solution"""
    grid = [[0 for _ in range(cols)] for _ in range(rows)]

    # Définir les groupes horizontaux et verticaux (au moins 2 cases)
    horizontal_groups = []
    vertical_groups = []

    # Pour simplifier, créer des groupes de longueur aléatoire >=2
    for r in range(rows):
        c = 0
        while c < cols - 1:
            length = random.randint(2, min(4, cols - c))
            horizontal_groups.append((r, c, length))
            c += length
            if c < cols:
                grid[r][c] = -1  # Case noire séparatrice
                c += 1

    for c in range(cols):
        r = 0
        while r < rows - 1:
            length = random.randint(2, min(4, rows - r))
            vertical_groups.append((r, c, length))
            r += length
            if r < rows:
                grid[r][c] = -1  # Case noire séparatrice
                r += 1

    # Résoudre la grille pour obtenir une seule solution
    solutions = solve_kakuro(grid, horizontal_groups, vertical_groups)
    if not solutions:
        return generate_kakuro(rows, cols)  # Recommencer si pas de solution unique
    solution = solutions[0]

    # Calculer les indices (sums)
    horizontal_sums = {}
    vertical_sums = {}

    for r, c, length in horizontal_groups:
        horizontal_sums[(r, c-1)] = sum(solution[r][c + i] for i in range(length))
    for r, c, length in vertical_groups:
        vertical_sums[(r-1, c)] = sum(solution[r + i][c] for i in range(length))

    return solution, horizontal_sums, vertical_sums

def print_kakuro(grid, horizontal_sums, vertical_sums):
    rows, cols = len(grid), len(grid[0])
    for r in range(rows):
        line = ""
        for c in range(cols):
            if grid[r][c] == -1:
                line += "█\t"
            else:
                h_sum = horizontal_sums.get((r, c-1), "")
                v_sum = vertical_sums.get((r-1, c), "")
                if h_sum or v_sum:
                    line += f"{v_sum}\\{h_sum}\t"
                else:
                    line += ".\t"
        print(line)

    def remplir_grille(dimension : int):
    
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
    print()
    
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

def initialiser_dictionnaires_variantes(dimension : int):
    
    
    global dictionnaire_liste_ligne
    global dictionnaire_liste_colonne

    dictionnaire_liste_ligne = {}
    dictionnaire_liste_colonne = {}
    
    for i in range(dimension):
        dictionnaire_liste_ligne[i] = list(range(1, dimension + 1))
        dictionnaire_liste_colonne[i] = list(range(1, dimension + 1))

def remplir_grille_variante(dimension : int):
    """
    Génère une grille complète en utilisant un backtracking itératif.
    """
    grille = generateur_grille_vide(dimension)
    initialiser_dictionnaires(dimension)
    essais = [[[] for _ in range(dimension)] for _ in range(dimension)]  # valeurs déjà essayées par les cases
    ligne = 0
    colonne = 0
    
    while ligne < dimension:
        candidats = list(set(dictionnaire_liste_ligne[ligne]) & set(dictionnaire_liste_colonne[colonne]) - set(essais[ligne][colonne])) # Candidats = intersection des listes disponibles en retirant les valeurs déjà essayées
        
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
            dictionnaire_liste_colonne[colonne].append(val_precedente)
            grille[ligne][colonne] = 0 
        
        else:
            valeur = (random.choice(candidats)) # On choisit une valeur et on avance
            grille[ligne][colonne] = valeur
            dictionnaire_liste_ligne[ligne].remove(valeur) # on retire la valeur tenté des choix possibles
            dictionnaire_liste_colonne[colonne].remove(valeur)
            
            if colonne == dimension - 1: 
                ligne += 1
                colonne = 0
            
            else:
                colonne += 1
    
    return (grille)

def generer_masque_kakuro(dimension, max_groupe=9): 
    """Génère un masque de Kakuro valide (0 = case blanche, 1 = case noire)."""
    grille = [[1 for _ in range(dimension)] for _ in range(dimension)]
    
    for ligne in range(dimension):
        colonne = 0
        while colonne < dimension:
            restant = dimension - colonne
            if restant < 2:
                break
            taille = random.randint(2, min(max_groupe, restant))
            for i in range(taille):
                grille[ligne][colonne + i] = 0
            colonne += taille
            if colonne < dimension:
                grille[ligne][colonne] = 1
                colonne += 1
    return grille

def est_valide(grille : list[list], ligne : int, colonne : int, valeur : int, dimension : int):
    """
    Vérifie si on a le droit de poser un chiffre à un endroit précis.
    Regarde si le chiffre existe déjà sur la ligne, la colonne ou dans son carré.
    
    Entrée : 
        grille: La grille actuelle.
        ligne, colonne: Les coordonnées de la case visée.
        valeur: Le chiffre que l'on veut tester.
        dimension : la taille de notre grille.
    """

    if valeur in grille[ligne]: # Vérifie la ligne
        return False
    if any(grille[i][colonne] == valeur for i in range(dimension)):  # Vérifie la colonne
        return False
    ligne_0, colonne_0 = (ligne // int(math.sqrt(dimension))) * int(math.sqrt(dimension)), (colonne // int(math.sqrt(dimension))) * int(math.sqrt(dimension)) # Vérifie le carré 3x3
    return not any(grille[i][e] == valeur for i in range(ligne_0, ligne_0 + int(math.sqrt(dimension))) for e in range(colonne_0, colonne_0 + int(math.sqrt(dimension))))

def compter_taille_groupe_horizontal_kakuro(grille : list[list:int], ligne, colonne, dimension):
    # Compter à gauche
    taille = 0
    c = colonne - 1
    while c >= 0 and grille[ligne][c] == 0:
        taille += 1
        c -= 1

    # Compter à droite
    c = colonne + 1
    while c < dimension and grille[ligne][c] == 0:
        taille += 1
        c += 1

    # Si on coupe un groupe existant, il doit rester >= 2
    if taille == 1:
        return False

    return True

def compter_taille_groupe_vertical_kakuro(grille, ligne, colonne, dimension):
    taille = 0
    l = ligne - 1
    while l >= 0 and grille[l][colonne] == 0:
        taille += 1
        l -= 1

    l = ligne + 1
    while l < dimension and grille[l][colonne] == 0:
        taille += 1
        l += 1

    if taille == 1:
        return False

    return True

def compter_solution_kakuro(grille : list[list:int], dimension,
                            groupes_horizontaux, sommes_horizontales,
                            groupes_verticaux, sommes_verticales,
                            limite=2):
    max_val = 9
    dispo_h = [[True]*max_val for _ in range(len(groupes_horizontaux))]
    dispo_v = [[True]*max_val for _ in range(len(groupes_verticaux))]
    grille_test = copy.deepcopy(grille)
    somme_h = [0]*len(groupes_horizontaux)
    somme_v = [0]*len(groupes_verticaux)
    
    case_vers_groupes = {}
    for idx, g in enumerate(groupes_horizontaux):
        for (i,j) in g:
            case_vers_groupes[(i,j)] = [idx, None]
    for idx, g in enumerate(groupes_verticaux):
        for (i,j) in g:
            case_vers_groupes[(i,j)][1] = idx
    
    cases_vides = []
    for i in range(dimension):
        for j in range(dimension):
            if grille_test[i][j] == 0:
                cases_vides.append((i,j))
            else:
                if (i,j) not in case_vers_groupes:
                    continue
                h, v = case_vers_groupes[(i,j)]
                val = grille_test[i][j]
                dispo_h[h][val-1] = False
                dispo_v[v][val-1] = False
                somme_h[h] += val
                somme_v[v] += val
    
    compteur = 0
    def solveur():
        nonlocal compteur
        if compteur >= limite:
            return
        if not cases_vides:
            compteur += 1
            return
        # MRV
        best_idx = -1
        best_vals = []
        min_poss = max_val+1
        for idx, (i,j) in enumerate(cases_vides):
            h,v = case_vers_groupes[(i,j)]
            candidats = []
            for val in range(1, max_val+1):
                if not dispo_h[h][val-1] or not dispo_v[v][val-1]:
                    continue
                if somme_h[h]+val > sommes_horizontales[h] or somme_v[v]+val > sommes_verticales[v]:
                    continue
                candidats.append(val)
            if len(candidats) < min_poss:
                min_poss = len(candidats)
                best_vals = candidats
                best_idx = idx
            if min_poss == 1:
                break
        if min_poss == 0:
            return
        i,j = cases_vides.pop(best_idx)
        h,v = case_vers_groupes[(i,j)]
        for val in best_vals:
            dispo_h[h][val-1] = False
            dispo_v[v][val-1] = False
            somme_h[h] += val
            somme_v[v] += val
            grille_test[i][j] = val
            complet_h = all(grille_test[x][y] != 0 for x,y in groupes_horizontaux[h])
            complet_v = all(grille_test[x][y] != 0 for x,y in groupes_verticaux[v])
            valide = True
            if complet_h and somme_h[h] != sommes_horizontales[h]:
                valide = False
            if complet_v and somme_v[v] != sommes_verticales[v]:
                valide = False
            if valide:
                solveur()
            dispo_h[h][val-1] = True
            dispo_v[v][val-1] = True
            somme_h[h] -= val
            somme_v[v] -= val
            grille_test[i][j] = 0
            if compteur >= limite:
                break
        cases_vides.insert(best_idx, (i,j))
    
    solveur()
    return compteur

def trouver_groupes_horizontaux_kakuro(grille : list[list:int]):
    groupes = []
    dimension = len(grille)
    for ligne in range(dimension):
        groupe = []
        for colonne in range(dimension):
            if grille[ligne][colonne] == 0:
                groupe.append((ligne, colonne))
            else:
                if len(groupe) >= 2:
                    groupes.append(groupe)
                groupe = []
        if len(groupe) >= 2:
            groupes.append(groupe)
    return groupes

def trouver_groupes_verticaux_kakuro(grille: list[list:int]):
    groupes = []
    dimension = len(grille)
    for colonne in range(dimension):
        groupe = []
        for ligne in range(dimension):
            if grille[ligne][colonne] == 0:
                groupe.append((ligne, colonne))
            else:
                if len(groupe) >= 2:
                    groupes.append(groupe)
                groupe = []
        if len(groupe) >= 2:
            groupes.append(groupe)
    return groupes

def valider_masque_kakuro(grille : list[list:int]):
    dimension = len(grille)
    groupes_h = trouver_groupes_horizontaux_kakuro(grille)
    groupes_v = trouver_groupes_verticaux_kakuro(grille)
    
    # Vérifier tailles des groupes
    for g in groupes_h + groupes_v:
        if len(g) < 2 or len(g) > 9:
            return False
    
    # Vérifier que chaque case blanche appartient à 2 groupes
    compteur = [[0]*dimension for _ in range(dimension)]
    for g in groupes_h + groupes_v:
        for (i,j) in g:
            compteur[i][j] += 1
    for i in range(dimension):
        for j in range(dimension):
            if grille[i][j] == 0 and compteur[i][j] != 2:
                return False
    return True
