import tkinter as tk

from GUI.fenetre import LARGEUR_PIXEL_FENETRE, HAUTEUR_PIXEL_FENETRE
from GUI.widgets import creer_boutton, survole_non_survole
from GUI.animations import retour_menu, mouvement_exterieur_fond_menu


def aller_credits(canvas: tk.Canvas) -> None:
    """
    Affiche la page des crédits
    """
    mouvement_exterieur_fond_menu(canvas)

    TAG: str = "credits"

    # fond
    COULEUR_FOND: str = "#373737"

    canvas.create_rectangle((0, 0), (LARGEUR_PIXEL_FENETRE, HAUTEUR_PIXEL_FENETRE), 
                            fill=COULEUR_FOND, outline=COULEUR_FOND, tags=TAG)
    
    # texte / titre
    POLICE: str = "Bell MT"

    PARAMS_TEXT: dict[str, str] = {
        "anchor" : tk.CENTER, 
        "fill" : "#ffffff",  
        "tags" : TAG
        }

    canvas.create_text((LARGEUR_PIXEL_FENETRE // 2, 50), text="Crédits", font=(POLICE, 50), **PARAMS_TEXT)
    
    # cadre
    COULEUR_CADRE: str = "#444444"
    ECART_CENTRE:int = 200
    XY1: tuple[int] = (LARGEUR_PIXEL_FENETRE // 2 - ECART_CENTRE, 110)
    XY2: tuple[int] = (LARGEUR_PIXEL_FENETRE // 2 + ECART_CENTRE, 500)

    canvas.create_rectangle(XY1, XY2, fill=COULEUR_CADRE, outline=COULEUR_CADRE, tags=TAG)
    
    # texte / crédits
    X_TEXT: int = LARGEUR_PIXEL_FENETRE // 2

    canvas.create_text((X_TEXT, 175), text="Créateurs :", font=(POLICE, 35), **PARAMS_TEXT)

    TAILLE_TEXT: int = 20

    canvas.create_text((X_TEXT, 250), text="Adam CONTAT", font=(POLICE, TAILLE_TEXT), 
                       **PARAMS_TEXT)
    canvas.create_text((X_TEXT, 300), text="Joseph HOUËL", font=(POLICE, TAILLE_TEXT), 
                       **PARAMS_TEXT)
    canvas.create_text((X_TEXT, 350), text="Louis THALGOTT-KAISER", font=(POLICE, TAILLE_TEXT), 
                       **PARAMS_TEXT)
    canvas.create_text((X_TEXT, 400), text="Benjamin VRBANAC", font=(POLICE, TAILLE_TEXT), 
                       **PARAMS_TEXT)
    
    # bouton de retour au menu
    LARGEUR_BOUTON: int = 300
    HAUTEUR_BOUTON: int = 124
    X_BOUTON: int = (LARGEUR_PIXEL_FENETRE - LARGEUR_BOUTON) // 2
    Y_BOUTON: int = HAUTEUR_PIXEL_FENETRE - HAUTEUR_BOUTON - 50

    COULEUR_BOUTON: dict[str, str] = {
        "couleur_fond" : "#939393",
        "couleur_bordure" : "#ADADAD"
    }

    COULEURS_SURVOLE: dict[str, str] = {
        "couleur_fond_surv" : "#636363",
        "couleur_bordure_surv" : "#454545"
    }

    TAG_RETOUR: str = "bouton_credits_retour"

    fond_retour, bordure_retour =  \
        creer_boutton(canvas, coord=(X_BOUTON, Y_BOUTON), tag=TAG_RETOUR, 
                    texte="Retour", largeur=LARGEUR_BOUTON, hauteur=HAUTEUR_BOUTON,  
                    police=("Cooper Black", 16), epaisseur_bordure=2, 
                    **COULEUR_BOUTON)[:-1]
    
    survole_non_survole(canvas, tag=TAG_RETOUR, fond=fond_retour, 
                        bordure=bordure_retour, **(COULEUR_BOUTON | COULEURS_SURVOLE))
    
    canvas.tag_bind(TAG_RETOUR, "<Button-1>", 
                lambda event: retour_menu(canvas, TAG, TAG_RETOUR))