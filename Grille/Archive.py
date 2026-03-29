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
    print()

