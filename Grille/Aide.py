import random
from Grille.verification import  est_valide


def verificateur_ligne_colonne(valeur,dimension,grille,ligne,colonne): 
 
    #verification de la lignes : 
    if valeur in grille[ligne]:
        return False
    #verification de la colonnes : 
    for i in range(dimension):
        if valeur == grille[i][colonne]:  
                return False
    return True

def indicateur_Sudoku(grille_actuelle : list[list:int],grille_solution : list[list:int],dimension : int):
    """permet d'indiquer à l'utilisateur une case"""
    Cases_vides= [(l,c) for l in range(dimension) for c in range(dimension) if grille_actuelle[l][c] == 0]
    
    #eviter de donner toujours les cases en haut à gauche 
    random.shuffle(Cases_vides)

    for l,c in Cases_vides : 
        
        #pour regler le probleme de l'unicite on recupere directement la solution attendue
        solution_attendue = grille_solution[l][c]

        #on verifie si cela est possible avec la grille actuelle
        if verificateur_ligne_colonne(solution_attendue,dimension,grille_actuelle,l,c): 
            return  solution_attendue,(l,c)
    
    return None

def indicateur_kenken(dimension,grille_actuelle):
    grille_valeurs = grille_actuelle[0]
    dico_cage = grille_actuelle[1]

    #determination des cases libres :
    cases_libres= []
    for i in range(dimension):
        for j in range(dimension):
            if grille_valeurs[i][j] == 0 : 
                cases_libres.append((i,j))
    
    for l,c in cases_libres :
        for valeur in range(1, dimension +1): 
        
            if not verificateur_ligne_colonne(valeur,dimension,grille_valeurs,l,c) : 
                continue

            #On l'ajoute pour l'instant dans la grille : 
            grille_tempo = [ligne[:] for ligne in grille_valeurs]
            grille_tempo[l][c] = valeur


            #Retrouver sa cage : 
            cage= None

            for cage_test in dico_cage.values():
                if (l,c) in cage_test["cases"] : 
                    cage = cage_test
                    break

            #validité de la cage trouvée : 
            valeurs = []
            cage_incomplete = False
            operation = cage["opération"]
            resultat = cage["résultat"]
            cases = cage["cases"]
            
            for (i,j) in cases:  
                if grille_tempo[i][j] == 0:
                    cage_incomplete = True
                    break
                valeurs.append(grille_tempo[i][j])
            
            if cage_incomplete: 
                continue

            if operation == "+":     # Test pour le cas d'une somme
                if sum(valeurs) == resultat :
                    return valeur, (l,c)

            if operation == "*":     # Test pour le cas s'un produit
                produit = 1
                for v in valeurs:
                    produit *= v
                if produit == resultat : 
                    return valeur, (l,c)

            if operation == "-":     # Test pour le cas d'une différence
                a,b = valeurs
                if abs(a-b) == resultat : 
                    return valeur, (l,c)

            if operation == "/":     # test pour le cas d'un quotient
                a,b = valeurs
                if max(a,b) // min(a,b) == resultat : 
                    return valeur, (l,c)
                
                #Reste à faire le cas ou aucune case est pleine
    return 'aucune valeur'
