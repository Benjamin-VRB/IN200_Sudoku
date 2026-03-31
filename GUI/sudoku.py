import tkinter as tk

from GUI.fenetre import LARGEUR_PIXEL_FENETRE, HAUTEUR_PIXEL_FENETRE
from GUI.animations import mouvement_exterieur_fond_menu, retour_menu
from GUI.widgets import creer_grille_sudoku, creer_boutton, survole_non_survole, remplir_grille_sudoku_GUI

from Grille.Sudoku import supprimer_valeur


def aller_sudoku(canvas: tk.Canvas) -> None:
    
    mouvement_exterieur_fond_menu(canvas)

    TAG: str = "sudoku"

    NB_CASE_COTE: int = 9
    LONGUEUR_COTE_GRILLE: int = NB_CASE_COTE * 60
    NB_CARRE_COTE: int = 3
    LONGUEUR_COTE_CASE: int = LONGUEUR_COTE_GRILLE // NB_CASE_COTE
    
    X_GRILLE: int = (LARGEUR_PIXEL_FENETRE - LONGUEUR_COTE_GRILLE) // 2
    Y_GRILLE: int = (HAUTEUR_PIXEL_FENETRE - LONGUEUR_COTE_GRILLE) // 2

    grille: tuple[list[tuple[int, int]], list[int]] = \
        creer_grille_sudoku(canvas, tag=TAG, coord=(X_GRILLE, Y_GRILLE), nb_case_cote=NB_CASE_COTE, 
                            longueur_cote_case=LONGUEUR_COTE_CASE, nb_carre_cote=NB_CARRE_COTE)
    grille_valeur: list[list[int]] = supprimer_valeur(nombre_valeur_a_supprimer=60, 
                                                      dimension=NB_CASE_COTE)
    remplir_grille_sudoku_GUI(canvas, cases=grille[0], grille_valeur=grille_valeur)
    
    PARAMS_BOUTON: dict[str, int | str | tuple[str, int]] = {
        "largeur" : 200,
        "hauteur" : 76,
        "police" : ("Cooper Black", 16),
        "epaisseur_bordure" : 2,
        "couleur_texte" : "#ffffff"
    }

    COULEURS_BOUTON: dict[str, str] = {
        "couleur_fond" : "#E0D4C1",
        "couleur_bordure" : "#E9E0CE"
    }
    
    COULEURS_SURVOLE: dict[str, str] = {
        "couleur_fond_surv" : "#BEB2A4",
        "couleur_bordure_surv" : "#A89E90"
    }

    ECART_RANGEE: int = PARAMS_BOUTON["hauteur"] + 100
    RANGEE2: int = (HAUTEUR_PIXEL_FENETRE - PARAMS_BOUTON["hauteur"]) // 2 
    RANGEE1: int = RANGEE2 + ECART_RANGEE
    RANGEE3: int = RANGEE2 - ECART_RANGEE
    COLONNE1: int = 75

    TAG_AIDE: str = "bouton_sudoku_aide"
    TAG_SAUV: str = "bouton_sudoku_sauv"
    TAG_RETOUR: str = "bouton_sudoku_retour"
    
    fond_aide, bordure_aide =  \
        creer_boutton(canvas, coord=(COLONNE1, RANGEE3), tag=TAG_AIDE, 
                    texte="Aide", **(PARAMS_BOUTON | COULEURS_BOUTON))[:-1]

    fond_sauv, bordure_sauv =  \
        creer_boutton(canvas, coord=(COLONNE1, RANGEE2), tag=TAG_SAUV, 
                    texte="Sauvegarder", **(PARAMS_BOUTON | COULEURS_BOUTON))[:-1]

    fond_retour, bordure_retour =  \
        creer_boutton(canvas, coord=(COLONNE1, RANGEE1), tag=TAG_RETOUR, 
                    texte="Retour", **(PARAMS_BOUTON | COULEURS_BOUTON))[:-1]

    survole_non_survole(canvas, tag=TAG_AIDE, fond=fond_aide, bordure=bordure_aide, 
                        **(COULEURS_BOUTON | COULEURS_SURVOLE))

    survole_non_survole(canvas, tag=TAG_SAUV, fond=fond_sauv, bordure=bordure_sauv, 
                        **(COULEURS_BOUTON | COULEURS_SURVOLE))

    survole_non_survole(canvas, tag=TAG_RETOUR, fond=fond_retour, bordure=bordure_retour, 
                        **(COULEURS_BOUTON | COULEURS_SURVOLE))
    
    canvas.tag_bind(tagOrId=TAG_RETOUR, sequence="<Button-1>", func=lambda event: 
                    retour_menu(canvas, tags_or_ids=[TAG, TAG_SAUV, TAG_RETOUR, TAG_AIDE, "clavier_num"]))
