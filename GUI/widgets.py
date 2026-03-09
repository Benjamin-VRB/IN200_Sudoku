import tkinter as tk


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


def desactiver_widget(canvas: tk.Canvas, tags_or_ids: list[str]) -> None:
    """
    Desactive les interactions avec les widgets indiqués
    """
    for tag_or_id in tags_or_ids:
        canvas.itemconfig(tag_or_id, state=tk.DISABLED)


def activer_widget(canvas: tk.Canvas, tags_or_ids: list[str]) -> None:
    """
    Active les interactions avec les widgets indiqués
    """
    for tag_or_id in tags_or_ids:
        canvas.itemconfig(tag_or_id, state=tk.NORMAL)


def reset_focus_cases(canvas: tk.Canvas, *cases: tuple[int]) -> None:

    canvas.unbind_all(sequence="<KeyPress>")
    for case in cases:
        canvas.itemconfig(tagOrId=case[0], width=1)
        canvas.tag_lower(case[0])

def modifier_valeur_case(event, canvas: tk.Canvas, case: tuple[int], 
                         valeur_max: int) -> None:
    
    texte: int = case[1]
    nombre_actuel: str = canvas.itemcget(tagOrId=texte, option="text")
    if event.char in "123456789" and int(nombre_actuel + event.char) <= valeur_max:
        canvas.itemconfig(tagOrId=texte, text=nombre_actuel + event.char)
    elif event.char == "0" and int(nombre_actuel + event.char) <= valeur_max \
        and nombre_actuel != "":
        canvas.itemconfig(tagOrId=texte, text=nombre_actuel + event.char)
    elif event.keysym == "BackSpace":
        canvas.itemconfig(tagOrId=texte, text=nombre_actuel[:-1])
    elif event.keysym == "Return":
        reset_focus_cases(canvas, case)


def entree_focus_case(canvas: tk.Canvas, case: tuple[int], valeur_max: int, 
                      cases_grille: list[int]) -> None:
    
    case_vide: int = case[0]
    texte: int = case[1]
    reset_focus_cases(canvas, *cases_grille)
    canvas.tag_raise(case_vide)
    canvas.tag_raise(texte)
    canvas.itemconfig(tagOrId=case_vide, width=4)
    canvas.bind_all(sequence="<KeyPress>", func=lambda event: 
                modifier_valeur_case(event, canvas=canvas, case=case,
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
    func = entree_focus_case
    for case in cases:
        case_vide: int = case[0]
        texte: int = case[1]
        canvas.tag_bind(tagOrId=case_vide, sequence=sequence, func=lambda event, case=case: 
                        func(canvas=canvas, case=case, valeur_max=nb_case_cote, 
                             cases_grille=cases))
        canvas.tag_bind(tagOrId=texte, sequence=sequence, func=lambda event, case=case: 
                        func(canvas=canvas, case=case, valeur_max=nb_case_cote, 
                             cases_grille=cases))
                    
    return (cases, carres)