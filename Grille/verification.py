import math

def verification_condition_sudoku(dimension : int, grille : list[list[int]], coord : tuple[int, int]):
    liste_cases_invalides = []
    
    ligne = coord[0]
    colonne = coord[1]
    
    liste_indices_lignes = [i for i in range(dimension)]
    liste_indices_lignes.remove(ligne)

    for i in liste_indices_lignes:
        if grille[i][colonne] == grille[ligne][colonne]:
            liste_cases_invalides.append((i, colonne))

    
    liste_indices_colonnes = [i for i in range(dimension)]
    liste_indices_colonnes.remove(ligne)

    for i in liste_indices_colonnes:
        if grille[ligne][i] == grille[ligne][colonne]:
            liste_cases_invalides.append((ligne, i))
    
    