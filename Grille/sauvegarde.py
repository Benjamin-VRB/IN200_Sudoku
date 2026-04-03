import json 

FICHIER_SAUVEGARDE = "Sauvegardes/grilles_jouees.json"
FICHIER_SAUVEGARDE_TEMPO = "Sauvegardes/grilles_en_cours.json"

def sauvegarde (grille, temps, difficulte, score):
    
    #On charge l'historique
    lecture=open(FICHIER_SAUVEGARDE, "r")
    liste_parties = json.load(lecture)
    lecture.close()
    
    #Les données de la partie qu'on va sauvegarder 
    nouvelle_partie={
        "difficulte" : difficulte,
        "grille" : grille,
        "temps" : temps,
        "score" : score,
    }

    #On ajoute notre nouvelle partie au début de la pile
    liste_parties.insert(0,nouvelle_partie)

    #On garde les 100 dernieres parties 
    liste_parties=liste_parties[:100]

    #On sauvegarde notre fichier 
    ecriture = open(FICHIER_SAUVEGARDE,"w")
    json.dump(liste_parties,ecriture,indent=4)
    ecriture.close()

    return 

def sauvegarde_progression(grille_actuelle,grille_solution,temps):
    
    donnee = {
        "grille_actuelle" : grille_actuelle,
        "grille_solution" : grille_solution,
        "temps" : temps,
        "etat" : "en_cours"
    }
    
    ecriture = open(FICHIER_SAUVEGARDE_TEMPO,"w")
    json.dump(donnee,ecriture)
    ecriture.close()
    
    return

def reinitialisation():
    
    donnee = {
        "grille_actuelle" : None,
        "grille_solution" : None,
        "temps" : None,
        "etat" : "vide"
    }

    ecriture = open(FICHIER_SAUVEGARDE_TEMPO,"w")
    json.dump(donnee,ecriture)
    ecriture.close()

    return

def charger_sauvegarde():

    lecture=open(FICHIER_SAUVEGARDE_TEMPO, "r")
    donnee = json.load(lecture)
    lecture.close()

    if donnee["etat"] == "vide" : 
        return None
    return donnee
