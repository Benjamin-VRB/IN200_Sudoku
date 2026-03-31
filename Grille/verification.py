import math

def verification_condition_sudoku( grille: list[list[int]], dimension: int, coord: tuple[int, int]):
    """Vérifie que la valeur de la case venant 'être saisie vérifie les règles du sudoku.
    
    Entrée:
        La grille de sudoku ainsi que sa dimension et les coordonnées de la case venant d'ête remplie 
        par l'utilisateur.
    
    Sortie:
        Liste des coordonnées des cases pour lesquelles cela les règles du sudoku ne sont pas respectées."""
   
    liste_cases_invalides = []     

    ligne = coord[0]
    colonne = coord[1]
    valeur = grille[ligne][colonne]

    liste_indices_lignes = [i for i in range(dimension)]   # Liste des indices des lignes a tester.
    liste_indices_lignes.remove(ligne)                     # a laquelle on enlève l'indice de la case venant d'être remplie.

    for i in liste_indices_lignes:
        if grille[i][colonne] == valeur:
            liste_cases_invalides.append((i, colonne))     # On regarde dans toute la ligne.


    liste_indices_colonnes = [i for i in range(dimension)]  # Liste des indices des colonnes a tester.
    liste_indices_colonnes.remove(colonne)                  # a laquelle on enlève l'indice de la case venant d'être remplie.

    for i in liste_indices_colonnes:
        if grille[ligne][i] == valeur:
            liste_cases_invalides.append((ligne, i))        # On regarde dans toute la colonne


    taille_bloc = int(math.sqrt(dimension))                 # calcul de la taille d'un carré

    debut_ligne = (ligne // taille_bloc) * taille_bloc          # On regarde dans quel bloc se trouve la case qu'on vient de remplir
    debut_colonne = (colonne // taille_bloc) * taille_bloc

    for i in range(debut_ligne, debut_ligne + taille_bloc):           # On teste toutes les cases de ce bloc.
        for j in range(debut_colonne, debut_colonne + taille_bloc):
            if (i, j) != coord and grille[i][j] == valeur:
                liste_cases_invalides.append((i, j))

    return liste_cases_invalides                            # On renvoie la liste des coordonnées des cases a faire voir au joueur.
