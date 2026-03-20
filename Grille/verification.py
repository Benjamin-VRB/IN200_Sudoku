import math
import copy

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