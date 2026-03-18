import tkinter as tk

from GUI.fenetre import LARGEUR_PIXEL_FENETRE


def creer_boutton(canvas: tk.Canvas, coord: tuple[int], tag: str, largeur: int = 200, 
        hauteur: int = 100, texte: str = "", couleur_fond: str = "#ffffff", 
        couleur_texte: str = "#ffffff", epaisseur_bordure: int= 5, 
        couleur_bordure: str = "#000000", police: tuple[str | int] = ("Arial", 11)
        ) -> tuple[list[int] | int]:
    """
    Crée un bouton sur le canvas 
    """
    bordure: list[int] = []

    bordure.append(
        canvas.create_arc(coord, (coord[0] + hauteur, coord[1] + hauteur), fill=couleur_bordure, 
                          outline=couleur_bordure, start=90, extent=180, tags=tag)
        )
    bordure.append(
        canvas.create_rectangle((coord[0] + hauteur // 2, coord[1]), 
                                (coord[0] + largeur - hauteur // 2, coord[1] + hauteur), 
                                fill=couleur_bordure, outline=couleur_bordure, tags=tag)
        )
    bordure.append(
        canvas.create_arc((coord[0] + largeur - hauteur, coord[1]), (coord[0] + largeur, coord[1] + hauteur), 
                          fill=couleur_bordure, outline=couleur_bordure, start=90, extent=-180, tags=tag)
        )
    
    fond: list[int] = []

    fond.append(
        canvas.create_arc((coord[0] + epaisseur_bordure, coord[1] + epaisseur_bordure), 
                          (coord[0] + hauteur - epaisseur_bordure, coord[1] + hauteur - epaisseur_bordure), 
                          fill=couleur_fond, outline=couleur_fond, start=90, extent=180, tags=tag)
        )
    fond.append(
        canvas.create_rectangle((coord[0] + (hauteur - 2 * epaisseur_bordure) // 2, coord[1] + epaisseur_bordure), 
                                (coord[0] + largeur - (hauteur - 2 * epaisseur_bordure) // 2, 
                                 coord[1] + hauteur - epaisseur_bordure), 
                                 fill=couleur_fond, outline=couleur_fond, tags=tag)
        )
    fond.append(
        canvas.create_arc((coord[0] + largeur - hauteur + epaisseur_bordure, coord[1] + epaisseur_bordure), 
                          (coord[0] + largeur - epaisseur_bordure, coord[1] + hauteur - epaisseur_bordure), 
                          fill=couleur_fond, outline=couleur_fond, start=90, extent=-180, tags=tag)
        )
    
    if texte != "":
        texte_bouton: int = canvas.create_text((coord[0] + largeur // 2, coord[1] + hauteur // 2), 
                                               text=texte, font=police, anchor=tk.CENTER, 
                                               fill=couleur_texte, tags=tag)
        
    return fond, bordure, texte_bouton


def survole(canvas: tk.Canvas, fond: list[int], bordure: list[int], 
                   couleur_fond: str, couleur_bordure: str) -> None:
    """
    Change les couleurs du widgets lorqu'il est survolé par la souris
    """
    for id in fond:
        canvas.itemconfig(tagOrId=id, fill=couleur_fond, outline=couleur_fond)
    for id in bordure:
        canvas.itemconfig(tagOrId=id, fill=couleur_bordure, outline=couleur_fond)


def non_survole(canvas: tk.Canvas, fond: list[int], bordure: list[int], 
                       couleur_fond: str, couleur_bordure: str) -> None:
    """
    Change les couleurs du widgets lorqu'il n'est plus survolé par la souris
    """
    for id in fond:
        canvas.itemconfig(tagOrId=id, fill=couleur_fond, outline=couleur_fond)
    for id in bordure:
        canvas.itemconfig(tagOrId=id, fill=couleur_bordure, outline=couleur_fond)


def survole_non_survole(canvas: tk.Canvas, tag: str, fond: list[int], bordure: list[int], 
                        couleur_fond: str, couleur_bordure: str, 
                        couleur_fond_surv: str, couleur_bordure_surv: str) -> None:
    """
    Change les couleurs du widgets lorqu'il est survolé et lorsqu'il n'est plus survolé par la souris
    """
    canvas.tag_bind(tagOrId=tag, sequence="<Enter>", 
                    func=lambda event: survole(canvas, fond=fond, bordure=bordure, 
                                               couleur_fond=couleur_fond_surv, 
                                               couleur_bordure=couleur_bordure_surv))
    canvas.tag_bind(tagOrId=tag, sequence="<Leave>", 
                    func=lambda event: non_survole(canvas, fond=fond, bordure=bordure, 
                                                   couleur_fond=couleur_fond, 
                                                   couleur_bordure=couleur_bordure))


def desactiver_widget(canvas: tk.Canvas, *tags_or_ids: str | int) -> None:
    """
    Desactive les interactions avec les widgets indiqués
    """
    for tag_or_id in tags_or_ids:
        canvas.itemconfig(tag_or_id, state=tk.DISABLED)


def activer_widget(canvas: tk.Canvas, *tags_or_ids: str | int) -> None:
    """
    Active les interactions avec les widgets indiqués
    """
    for tag_or_id in tags_or_ids:
        canvas.itemconfig(tag_or_id, state=tk.NORMAL)


def reset_focus_cases(canvas: tk.Canvas, *cases: tuple[int]) -> None:

    canvas.unbind_all(sequence="<KeyPress>")
    canvas.delete("clavier_num")
    for case in cases:
        canvas.itemconfig(tagOrId=case[0], width=1, outline="#000000")
        canvas.tag_lower(case[0])


def modifier_valeur_case_grille(event, canvas: tk.Canvas, case: tuple[int], 
                         valeur_max: int) -> None:
    
    texte: int = case[1]
    nombre_actuel: str = canvas.itemcget(tagOrId=texte, option="text")
    if event.char in "123456789" and int(nombre_actuel + event.char) <= valeur_max:
        canvas.itemconfig(tagOrId=texte, text=nombre_actuel + event.char)
    elif event.char == "0" and int(nombre_actuel + event.char) <= valeur_max \
        and nombre_actuel != "":
        canvas.itemconfig(tagOrId=texte, text=nombre_actuel + event.char)
    elif event.keysym == "BackSpace" or event.keysym == "KP_Delete":
        canvas.itemconfig(tagOrId=texte, text=nombre_actuel[:-1])
    elif event.keysym == "Return":
        reset_focus_cases(canvas, case)


def modifier_valeur_case_clavier_num(canvas: tk.Canvas, case: tuple[int], 
                                     valeur_max: int, valeur: str) -> None:
    
    texte: int = case[1]
    nombre_actuel: str = canvas.itemcget(tagOrId=texte, option="text")
    if valeur in "123456789" and int(nombre_actuel + valeur) <= valeur_max:
        canvas.itemconfig(tagOrId=texte, text=nombre_actuel + valeur)
    elif valeur == "0" and int(nombre_actuel + valeur) <= valeur_max \
        and nombre_actuel != "":
        canvas.itemconfig(tagOrId=texte, text=nombre_actuel + valeur)
    elif valeur == "suppr":
        canvas.itemconfig(tagOrId=texte, text=nombre_actuel[:-1])


def creer_clavier_numerique(canvas: tk.Canvas, coord: tuple[int], 
                            largeur: int, hauteur: int, case: tuple[int], 
                            valeur_max: int) -> None:
    
    largeur_bouton: int = largeur // 3
    hauteur_bouton: int = hauteur // 4

    PARAMAS_BOUTON: dict[str, str, tuple[str, int]] = {
        "bg" : "#ffffff", 
        "fg" : "#000000", 
        "font" : ("Century", 12), 
    }

    TAG: str = "clavier_num"
    ANCHOR = tk.NW
    FUNC = modifier_valeur_case_clavier_num

    bouton7: tk.Button = tk.Button(canvas, command=lambda case=case: 
                                   FUNC(canvas, case=case, valeur_max=valeur_max, valeur="7"), 
                                    text="7",**PARAMAS_BOUTON)
    canvas.create_window(coord, tags=TAG, anchor=ANCHOR, width=largeur_bouton, 
                         height=hauteur_bouton, window=bouton7)

    bouton8: tk.Button = tk.Button(canvas, command=lambda case=case:
                                   FUNC(canvas, case=case, valeur_max=valeur_max, valeur="8"),
                                   text="8", **PARAMAS_BOUTON)
    canvas.create_window((coord[0] + largeur_bouton, coord[1]),  tags=TAG,
                          anchor=ANCHOR, width=largeur_bouton, height=hauteur_bouton, 
                          window=bouton8)
    
    bouton9: tk.Button = tk.Button(canvas, command=lambda case=case:
                                   FUNC(canvas, case=case, valeur_max=valeur_max, valeur="9"),
                                   text="9", **PARAMAS_BOUTON)
    canvas.create_window((coord[0] + 2 *largeur_bouton, coord[1]),  tags=TAG,
                          anchor=ANCHOR, width=largeur_bouton, height=hauteur_bouton, 
                          window=bouton9)
    
    bouton4: tk.Button = tk.Button(canvas, command=lambda case=case:
                                   FUNC(canvas, case=case, valeur_max=valeur_max, valeur="4"),
                                   text="4", **PARAMAS_BOUTON)
    canvas.create_window((coord[0], coord[1] + hauteur_bouton),  tags=TAG,
                          anchor=ANCHOR, width=largeur_bouton, height=hauteur_bouton, 
                          window=bouton4)
    
    bouton5: tk.Button = tk.Button(canvas, command=lambda case=case:
                                   FUNC(canvas, case=case, valeur_max=valeur_max, valeur="5"),
                                   text="5", **PARAMAS_BOUTON)
    canvas.create_window((coord[0] + largeur_bouton, coord[1] + hauteur_bouton),  tags=TAG,
                          anchor=ANCHOR, width=largeur_bouton, height=hauteur_bouton, 
                          window=bouton5)
    
    bouton6: tk.Button = tk.Button(canvas, command=lambda case=case:
                                   FUNC(canvas, case=case, valeur_max=valeur_max, valeur="6"),
                                   text="6", **PARAMAS_BOUTON)
    canvas.create_window((coord[0] + 2 * largeur_bouton, coord[1] + hauteur_bouton),  tags=TAG,
                          anchor=ANCHOR, width=largeur_bouton, height=hauteur_bouton, 
                          window=bouton6)
    
    bouton1: tk.Button = tk.Button(canvas, command=lambda case=case:
                                   FUNC(canvas, case=case, valeur_max=valeur_max, valeur="1"),
                                   text="1", **PARAMAS_BOUTON)
    canvas.create_window((coord[0], coord[1] + 2 * hauteur_bouton),  tags=TAG,
                          anchor=ANCHOR, width=largeur_bouton, height=hauteur_bouton, 
                          window=bouton1)
    
    bouton2: tk.Button = tk.Button(canvas, command=lambda case=case:
                                   FUNC(canvas, case=case, valeur_max=valeur_max, valeur="2"),
                                   text="2", **PARAMAS_BOUTON)
    canvas.create_window((coord[0] + largeur_bouton, coord[1] + 2 * hauteur_bouton),  tags=TAG,
                          anchor=ANCHOR, width=largeur_bouton, height=hauteur_bouton, 
                          window=bouton2)
    
    bouton3: tk.Button = tk.Button(canvas, command=lambda case=case:
                                   FUNC(canvas, case=case, valeur_max=valeur_max, valeur="3"),
                                   text="3", **PARAMAS_BOUTON)
    canvas.create_window((coord[0] + 2 * largeur_bouton, coord[1] + 2 * hauteur_bouton),  tags=TAG,
                          anchor=ANCHOR, width=largeur_bouton, height=hauteur_bouton, 
                          window=bouton3)
    
    bouton0: tk.Button = tk.Button(canvas, command=lambda case=case:
                                   FUNC(canvas, case=case, valeur_max=valeur_max, valeur="0"),
                                   text="0", **PARAMAS_BOUTON)
    canvas.create_window((coord[0], coord[1] + 3 * hauteur_bouton),  tags=TAG,
                          anchor=ANCHOR, width=largeur_bouton, height=hauteur_bouton, 
                          window=bouton0)
    
    bouton_suppr: tk.Button = tk.Button(canvas, command=lambda case=case:
                                        FUNC(canvas, case=case, valeur_max=valeur_max, valeur="suppr"),
                                        text="Suppr", **PARAMAS_BOUTON)
    canvas.create_window((coord[0] + largeur_bouton, coord[1] + 3 * hauteur_bouton),  tags=TAG,
                          anchor=ANCHOR, width=2 * largeur_bouton, height=hauteur_bouton, 
                          window=bouton_suppr)
    
    COULEUR_CADRE: str = "#000000"
    EPAISSEUR_CADRE: int = 3

    canvas.create_rectangle((coord[0] - EPAISSEUR_CADRE, coord[1] - EPAISSEUR_CADRE), 
                            (coord[0] + 3 * largeur_bouton + EPAISSEUR_CADRE - 1, 
                             coord[1] + 4 * hauteur_bouton + EPAISSEUR_CADRE - 1), 
                            fill=COULEUR_CADRE, outline="", tags=TAG)
    

def entree_focus_case(canvas: tk.Canvas, case: tuple[int], valeur_max: int, 
                      cases_grille: list[int]) -> None:
    
    case_vide: int = case[0]
    texte: int = case[1]

    reset_focus_cases(canvas, *cases_grille)
    canvas.tag_raise(case_vide)
    canvas.tag_raise(texte)
    canvas.itemconfig(tagOrId=case_vide, width=4, outline="#3185ED")

    LARGEUR_CLAVIER_NUM: int = 250
    HAUTEUR_CLAVIER_NUM: int = 400
    creer_clavier_numerique(canvas, 
                            coord=(LARGEUR_PIXEL_FENETRE - 300, 150), 
                            largeur=LARGEUR_CLAVIER_NUM, hauteur=HAUTEUR_CLAVIER_NUM, 
                            case=case, valeur_max=valeur_max)
    
    canvas.bind_all(sequence="<KeyPress>", func=lambda event: 
                modifier_valeur_case_grille(event, canvas=canvas, case=case,
                                     valeur_max=valeur_max))


def creer_case(canvas: tk.Canvas, tag: str, coord: tuple[int], 
                    longueur_cote: int) -> tuple[int]:

    case_vide: int = canvas.create_rectangle(coord, (coord[0] + longueur_cote, coord[1] + longueur_cote),
                                             fill="#ffffff", outline="#000000", width=1, tags=tag)
    texte: int = canvas.create_text((coord[0] + longueur_cote // 2, coord[1] + longueur_cote // 2),
                                   anchor=tk.CENTER, font=("Century", int(1 / 3  * longueur_cote)), 
                                   fill="#000000", tags=tag, text="")
    return (case_vide, texte)


def creer_grille_sudoku(canvas: tk.Canvas, tag: str, coord: tuple[int], nb_case_cote: int, 
                        longueur_cote_case: int, nb_carre_cote: int) -> tuple[list[int]]:
    
    cases: list[int] = []
    for rangee in range(nb_case_cote):
        for colonne in range(nb_case_cote):
            x_case: int = coord[0] + colonne * longueur_cote_case
            y_case: int = coord[1] + rangee * longueur_cote_case
            cases.append(
                creer_case(canvas, tag=tag, coord=(x_case, y_case), 
                                longueur_cote=longueur_cote_case)
                )  
    
    carres: list[int] = []
    if nb_case_cote % nb_carre_cote == 0:
        longueur_cote_carre = longueur_cote_case * nb_case_cote // nb_carre_cote
        for i in range(nb_carre_cote):
            for j in range(nb_carre_cote):
                x_carre_1: int = coord[0] + longueur_cote_carre * i
                y_carre_2: int = coord[1] + longueur_cote_carre * j
                carres.append(
                    canvas.create_rectangle((x_carre_1, y_carre_2), 
                                            (x_carre_1 + longueur_cote_carre, y_carre_2 + longueur_cote_carre),
                                            fill="", width=3, tags=tag)
                    )
                
    sequence: str = "<Button-1>"
    FUNC = entree_focus_case
    for case in cases:
        case_vide: int = case[0]
        texte: int = case[1]
        canvas.tag_bind(tagOrId=case_vide, sequence=sequence, func=lambda event, case=case: 
                        FUNC(canvas=canvas, case=case, valeur_max=nb_case_cote, 
                             cases_grille=cases))
        canvas.tag_bind(tagOrId=texte, sequence=sequence, func=lambda event, case=case: 
                        FUNC(canvas=canvas, case=case, valeur_max=nb_case_cote, 
                             cases_grille=cases))
                    
    return (cases, carres)




    