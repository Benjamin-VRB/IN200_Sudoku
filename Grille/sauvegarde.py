import json 

fichier_sauvergarde = "Sauvegardes/grilles_jouees.json"

def sauvegarde (grille, temps, difficulte, score):
    
    #On charge l'historique
    lecture=open(fichier_sauvergarde, "r")
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
    ecriture = open(fichier_sauvergarde,"w")
    json.dump(liste_parties,ecriture,indent=4)
    ecriture.close()

    return 