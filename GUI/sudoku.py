
import tkinter as tk

from GUI.fenetre import LARGEUR_PIXEL_FENETRE, HAUTEUR_PIXEL_FENETRE
from GUI.animations import mouvement_exterieur_fond_menu
from GUI.widgets import creer_grille_sudoku


def aller_sudoku(canvas: tk.Canvas) -> None:
    
    mouvement_exterieur_fond_menu(canvas)

    LONGUEUR_COTE_CASE: int = 30
    NB_CASE_COTE: int = 15
    NB_CARRE_COTE: int = 5
    LONGUEUR_COTE_GRILLE: int = LONGUEUR_COTE_CASE * NB_CASE_COTE
    X_GRILLE: int = (LARGEUR_PIXEL_FENETRE - LONGUEUR_COTE_GRILLE) // 2
    Y_GRILLE: int = (HAUTEUR_PIXEL_FENETRE - LONGUEUR_COTE_GRILLE) // 2
    creer_grille_sudoku(canvas, tag="grille_sudoku", coord=(X_GRILLE, Y_GRILLE), nb_case_cote=NB_CASE_COTE, 
                        longueur_cote_case=LONGUEUR_COTE_CASE, nb_carre_cote=NB_CARRE_COTE)
