import random
from Grille.verification import  est_valide

def indicateur(grille_actuelle : list[list:int],grille_solution : list[list:int],dimension : int):
    """permet d'indiquer à l'utilisateur une case"""
    Cases_vides= [(l,c) for l in range(dimension) for c in range(dimension) if grille_actuelle[l][c] == 0]
    
    #eviter de donner toujours les cases en haut à gauche 
    random.shuffle(Cases_vides)

    for l,c in Cases_vides : 
        
        #pour regler le probleme de l'unicite on recupere directement la solution attendue
        solution_attendue = grille_solution[l][c]

        #on verifie si cela est possible avec la grille actuelle
        if est_valide(grille_actuelle,l,c,solution_attendue,dimension): 
            return  solution_attendue,(l,c)
    
    return None


    
