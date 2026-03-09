import tkinter as tk

from GUI.fenetre import racine, LARGEUR_PIXEL_FENETRE, HAUTEUR_PIXEL_FENETRE
from GUI.sudoku import aller_sudoku
from GUI.stats import aller_stats
from GUI.credits import aller_credits
from GUI.widgets import creer_boutton, survole_non_survole
from GUI.animations import mouvement_interieur_fond_menu


def aller_menu() -> tk.Canvas:
    """
    Crée le canvas et affiche le menu
    """
    # canvas
    COULEUR_FOND_CNV: str = "#ffffff"

    cnv: tk.Canvas = tk.Canvas(
        racine, 
        width=LARGEUR_PIXEL_FENETRE,
        height=HAUTEUR_PIXEL_FENETRE,
        bg=COULEUR_FOND_CNV
        )

    cnv.pack()

    # menu

    # côté gauche du fond
    COULEUR_FOND_GAUCHE: str = "#4373A3"
    TAG_FOND_GAUCHE: str = "fond_bleu"
    x_lim_gauche_haut: int = LARGEUR_PIXEL_FENETRE // 4 + 100
    x_lim_gauche_bas: int = LARGEUR_PIXEL_FENETRE // 5 + 100

    cnv.create_polygon(((-x_lim_gauche_haut, 0), (0, 0), 
                        (x_lim_gauche_bas - x_lim_gauche_haut, HAUTEUR_PIXEL_FENETRE), 
                        (-x_lim_gauche_haut, HAUTEUR_PIXEL_FENETRE)), 
                        fill=COULEUR_FOND_GAUCHE, outline=COULEUR_FOND_GAUCHE, 
                        tags=TAG_FOND_GAUCHE)

    cnv.create_polygon(((-50, 0), (-25, 0), 
                        (x_lim_gauche_bas - x_lim_gauche_haut - 25, HAUTEUR_PIXEL_FENETRE), 
                        (x_lim_gauche_bas - x_lim_gauche_haut - 50, HAUTEUR_PIXEL_FENETRE)), 
                        fill=COULEUR_FOND_CNV, outline=COULEUR_FOND_CNV, 
                        tags=TAG_FOND_GAUCHE)
    
    # côté droite du fond
    COULEUR_FOND_DROITE: str = "#CE8450"
    TAG_FOND_DROITE: str = "fond_orange"
    x_lim_droite_haut: int = 4 * LARGEUR_PIXEL_FENETRE // 5 - 100
    x_lim_droite_bas: int = 3 * LARGEUR_PIXEL_FENETRE // 4 - 100

    cnv.create_polygon(((2 * LARGEUR_PIXEL_FENETRE - x_lim_droite_bas, 0), 
                        (x_lim_droite_haut + LARGEUR_PIXEL_FENETRE - x_lim_droite_bas, 0), 
                        (LARGEUR_PIXEL_FENETRE, HAUTEUR_PIXEL_FENETRE), 
                        (2 * LARGEUR_PIXEL_FENETRE - x_lim_droite_bas, HAUTEUR_PIXEL_FENETRE)), 
                        fill=COULEUR_FOND_DROITE, outline=COULEUR_FOND_DROITE, 
                        tags=TAG_FOND_DROITE)

    cnv.create_polygon(((x_lim_droite_haut + 25 + LARGEUR_PIXEL_FENETRE - x_lim_droite_bas, 0), 
                        (x_lim_droite_haut + 50 + LARGEUR_PIXEL_FENETRE - x_lim_droite_bas, 0), 
                        (LARGEUR_PIXEL_FENETRE + 50, HAUTEUR_PIXEL_FENETRE), 
                        (LARGEUR_PIXEL_FENETRE + 25, HAUTEUR_PIXEL_FENETRE)), 
                        fill=COULEUR_FOND_CNV, outline=COULEUR_FOND_CNV, 
                        tags=TAG_FOND_DROITE)
    
    # boutons
    PARAMS_BOUTON: dict[str, int | str | tuple] = {
            "largeur" : 300,
            "hauteur" : 124,
            "police" : ("Cooper Black", 16),
            "epaisseur_bordure" : 2
        }

    COULEURS_BOUTON: dict[str, str] = {
            "couleur_fond" : "#E9E5DE",
            "couleur_bordure" : "#F4EFE4"
        }
    
    ECART_RANGEE: int = 200
    RANGEE1: int = (HAUTEUR_PIXEL_FENETRE - PARAMS_BOUTON["hauteur"]) // 2 - ECART_RANGEE
    RANGEE2: int = RANGEE1 + ECART_RANGEE
    RANGEE3: int = RANGEE2 + ECART_RANGEE
    COLONNE1: int = -PARAMS_BOUTON["largeur"]
    COLONNE2: int = LARGEUR_PIXEL_FENETRE

    COULEURS_SURVOLE: dict[str, str] = {
        "couleur_fond_surv" : "#C7C3BE",
        "couleur_bordure_surv" : "#AFAAA3"
    }

    TAG_PERSO: str = "bouton_perso"
    TAG_PUZZ: str = "bouton_puzz"
    TAG_SAUV: str = "bouton_sauv"
    TAG_STATS: str = "bouton_stats"
    TAG_CREDITS: str = "bouton_credits"
    TAG_QUITTER: str = "bouton_quitter"

    fond_perso, bordure_perso =  \
        creer_boutton(cnv, coord=(COLONNE1, RANGEE1), tag=TAG_PERSO, 
                    texte="Partie personnalisée", couleur_texte=COULEUR_FOND_GAUCHE, 
                    **(PARAMS_BOUTON | COULEURS_BOUTON))[:-1]
    
    fond_puzz, bordure_puzz =  \
        creer_boutton(cnv, coord=(COLONNE1, RANGEE2), tag=TAG_PUZZ, 
                    texte="Puzzles", couleur_texte=COULEUR_FOND_GAUCHE, 
                    **(PARAMS_BOUTON | COULEURS_BOUTON))[:-1]
    
    fond_sauv, bordure_sauv =  \
        creer_boutton(cnv, coord=(COLONNE1, RANGEE3), tag=TAG_SAUV, 
                      texte="Sauvegardes", couleur_texte=COULEUR_FOND_GAUCHE, 
                      **(PARAMS_BOUTON | COULEURS_BOUTON))[:-1]
    
    fond_stats, bordure_stats =  \
        creer_boutton(cnv, coord=(COLONNE2, RANGEE1), tag=TAG_STATS, 
                    texte="Statistiques", couleur_texte=COULEUR_FOND_DROITE, 
                    **(PARAMS_BOUTON | COULEURS_BOUTON))[:-1]
    
    fond_credits, bordure_credits =  \
        creer_boutton(cnv, coord=(COLONNE2, RANGEE2), tag=TAG_CREDITS, 
                    texte="Crédits", couleur_texte=COULEUR_FOND_DROITE, 
                    **(PARAMS_BOUTON | COULEURS_BOUTON))[:-1]
    
    fond_quitter, bordure_quitter =  \
        creer_boutton(cnv, coord=(COLONNE2, RANGEE3), tag=TAG_QUITTER, 
                texte="Quitter", couleur_texte=COULEUR_FOND_DROITE, 
                **(PARAMS_BOUTON | COULEURS_BOUTON))[:-1]

    survole_non_survole(cnv, tag=TAG_PERSO, fond=fond_perso, bordure=bordure_perso, 
                        **(COULEURS_BOUTON | COULEURS_SURVOLE))
    
    survole_non_survole(cnv, tag=TAG_PUZZ, fond=fond_puzz, bordure=bordure_puzz, 
                        **(COULEURS_BOUTON | COULEURS_SURVOLE))
    
    survole_non_survole(cnv, tag=TAG_SAUV, fond=fond_sauv, bordure=bordure_sauv, 
                        **(COULEURS_BOUTON | COULEURS_SURVOLE))

    survole_non_survole(cnv, tag=TAG_STATS, fond=fond_stats, bordure=bordure_stats, 
                        **(COULEURS_BOUTON | COULEURS_SURVOLE))
    
    survole_non_survole(cnv, tag=TAG_CREDITS, fond=fond_credits, bordure=bordure_credits, 
                        **(COULEURS_BOUTON | COULEURS_SURVOLE))
    
    survole_non_survole(cnv, tag=TAG_QUITTER, fond=fond_quitter, bordure=bordure_quitter, 
                        **(COULEURS_BOUTON | COULEURS_SURVOLE))

    cnv.tag_bind(tagOrId=TAG_PERSO, sequence="<Button-1>", 
                 func=lambda event: aller_sudoku(cnv))
    cnv.tag_bind(tagOrId=TAG_STATS, sequence="<Button-1>", 
                 func=lambda event: aller_stats(cnv))
    cnv.tag_bind(tagOrId=TAG_CREDITS, sequence="<Button-1>", func=lambda event: aller_credits(cnv))
    cnv.tag_bind(tagOrId=TAG_QUITTER, sequence="<Button-1>", func=lambda event: exit())

    # titre
    cnv.create_text((LARGEUR_PIXEL_FENETRE // 2, 0), 
                        text="Sudoku", font=("Californian fb", 100), anchor=tk.S, 
                        fill="#89BFC9", tags="sudoku")
    
    mouvement_interieur_fond_menu(cnv)
    return cnv