import random

def generer_reseau_groupes(taille=9, max_groupe=4):
    """
    Génère un réseau de cases blanches/noires avec plusieurs groupes par ligne/colonne.
    - True = case blanche
    - False = case noire (pour indices)
    """
    reseau = [[False]*taille for _ in range(taille)]
    
    # Ligne 0 et Colonne 0 = toujours case noire pour indices
    for r in range(1, taille):
        c = 1
        while c < taille:
            borne_sup = min(max_groupe, taille - c)
            if borne_sup < 2:
                break
            taille_groupe = random.randint(2, borne_sup)
            for i in range(taille_groupe):
                reseau[r][c+i] = True
            c += taille_groupe
            if c < taille:
                reseau[r][c] = False
                c += 1

    for c in range(1, taille):
        r = 1
        while r < taille:
            borne_sup = min(max_groupe, taille - r)
            if borne_sup < 2:
                break
            taille_groupe = random.randint(2, borne_sup)
            for i in range(taille_groupe):
                reseau[r+i][c] = True
            r += taille_groupe
            if r < taille:
                reseau[r][c] = False
                r += 1
    return reseau

def generer_solution_backtracking(reseau):
    taille = len(reseau)
    grille = [[0]*taille for _ in range(taille)]
    colonnes_utilisees = [set() for _ in range(taille)]
    
    def remplir_case(r, c):
        if r == taille:
            return True
        next_r, next_c = (r, c+1) if c+1 < taille else (r+1, 1)
        if not reseau[r][c]:
            return remplir_case(next_r, next_c)
        chiffres = list(range(1, 10))
        random.shuffle(chiffres)
        for chiffre in chiffres:
            doublon_h = any(grille[r][k]==chiffre for k in range(c-1, -1, -1) if reseau[r][k])
            doublon_v = chiffre in colonnes_utilisees[c]
            if not doublon_h and not doublon_v:
                grille[r][c] = chiffre
                colonnes_utilisees[c].add(chiffre)
                if remplir_case(next_r, next_c):
                    return True
                grille[r][c] = 0
                colonnes_utilisees[c].remove(chiffre)
        return False
    
    success = remplir_case(1,1)
    if not success:
        return generer_solution_backtracking(reseau)
    return grille

def placer_indices(grille, reseau):
    taille = len(grille)
    final = [[None]*taille for _ in range(taille)]
    
    # copier les chiffres
    for r in range(taille):
        for c in range(taille):
            if reseau[r][c]:
                final[r][c] = grille[r][c]
    
    # indices horizontaux
    for r in range(1, taille):
        c = 1
        while c < taille:
            if reseau[r][c]:
                start = c
                while start>0 and reseau[r][start-1]:
                    start -= 1
                end = c
                while end<taille and reseau[r][end]:
                    end +=1
                somme = sum(grille[r][k] for k in range(start,end))
                if start>0:
                    if final[r][start-1] is None:
                        final[r][start-1] = [somme,None]
                    else:
                        if not isinstance(final[r][start-1], list):
                            final[r][start-1] = [somme,None]
                        else:
                            final[r][start-1][0] = somme
                c = end
            else:
                c+=1
    
    # indices verticaux
    for c in range(1, taille):
        r = 1
        while r < taille:
            if reseau[r][c]:
                start = r
                while start>0 and reseau[start-1][c]:
                    start-=1
                end = r
                while end<taille and reseau[end][c]:
                    end+=1
                somme = sum(grille[k][c] for k in range(start,end))
                if start>0:
                    if final[start-1][c] is None:
                        final[start-1][c] = [None,somme]
                    else:
                        if not isinstance(final[start-1][c], list):
                            final[start-1][c] = [None,somme]
                        else:
                            final[start-1][c][1] = somme
                r = end
            else:
                r+=1
    
    # remplir les autres cases noires
    for r in range(taille):
        for c in range(taille):
            if final[r][c] is None:
                final[r][c] = [None,None]
    return final

def generer_grille_kakuro_9x9_groupes():
    reseau = generer_reseau_groupes(9)
    solution = generer_solution_backtracking(reseau)
    return placer_indices(solution, reseau)

def afficher_grille(grille):
    for ligne in grille:
        print(" ".join(str(x) for x in ligne))

grille = generer_grille_kakuro_9x9_groupes()
afficher_grille(grille)

# COMMENT LIRE LA GRILLE
"""
- int -> chiffre de la solution (case blanche)
- list [somme_horizontale, somme_verticale] -> case indice
  None si pas de groupe dans cette direction
- Plusieurs groupes horizontaux et verticaux par ligne/colonne sont possibles
- Chaque case blanche appartient exactement à un groupe horizontal et un groupe vertical
"""
