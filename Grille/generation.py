import random
import copy
import math
from verification import compter_solution_V3
from verification import compter_solution_kakuro
from verification import valider_masque_kakuro
from verification import trouver_groupes_horizontaux_kakuro
from verification import trouver_groupes_verticaux_kakuro

dictionnaire_liste_ligne = {}
dictionnaire_liste_colonne = {}
dictionnaire_liste_carre = {}

def generateur_grille_vide(dimension): 
    grille_vide = [[0] * dimension for i in range(dimension)]
    return(grille_vide)

def initialiser_dictionnaires(dimension):
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

def initialiser_dictionnaires_variantes(dimension):
    
    global dictionnaire_liste_ligne
    global dictionnaire_liste_colonne

    dictionnaire_liste_ligne = {}
    dictionnaire_liste_colonne = {}
    
    for i in range(dimension):
        dictionnaire_liste_ligne[i] = list(range(1, dimension + 1))
        dictionnaire_liste_colonne[i] = list(range(1, dimension + 1))

def remplir_grille_variante(dimension):
    
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

def remplir_grille(dimension):
    
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

def supprimer_valeur(grille_complete, nombre_valeur_a_supprimer, dimension):
    grille_vider = copy.deepcopy(grille_complete)
    positions = [(ligne, colonne) for ligne in range(dimension) for colonne in range(dimension)]
    random.shuffle(positions)

    nombre_case_supprime = 0

    while nombre_case_supprime < nombre_valeur_a_supprimer:
        if not positions:
            # plus de positions → recommence avec nouvelle grille
            if (nombre_valeur_a_supprimer - nombre_case_supprime) > 5:   
                return supprimer_valeur(remplir_grille(dimension), nombre_valeur_a_supprimer, dimension)
            else:
                return grille_vider

        ligne, colonne = positions.pop()
        valeur_originale = grille_vider[ligne][colonne]
        grille_vider[ligne][colonne] = 0

        if compter_solution_V3(grille_vider, dimension) == 1:
            nombre_case_supprime += 1
        else:
            grille_vider[ligne][colonne] = valeur_originale

    return grille_vider

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

# --- Exemple d'utilisation ---
rows, cols = 5, 5
solution, h_sums, v_sums = generate_kakuro(rows, cols)

print("Solution complète:")
for row in solution:
    print(row)

print("\nKakuro avec indices:")
print_kakuro(solution, h_sums, v_sums)