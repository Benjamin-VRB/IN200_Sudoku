import numpy as np
import tensorflow as tf

def predict_sudoku(grid_str):
    # 1. Charger le modèle
    model = tf.keras.models.load_model('sudoku_model.h5')
    
    # 2. Préparer la grille (chaîne de 81 chiffres -> matrice 9x9)
    grid = np.array([int(c) for c in grid_str]).reshape(1, 9, 9, 1)
    grid = grid / 9.0  # Même normalisation que pendant l'entraînement
    
    # 3. Prédiction
    prediction = model.predict(grid)
    
    # 4. Transformer les probabilités en chiffres (on prend l'index le plus probable + 1)
    # prediction a la forme (1, 9, 9, 9)
    result = np.argmax(prediction, axis=-1).reshape(9, 9) + 1
    
    return result

# Exemple avec une grille réelle (remplace par une de ton dataset pour tester)
grille_test = "500004700930000060000720000070053090300000006000400000400000000026170000001000500" 
# Ou mets une vraie grille de 81 chiffres ici

print("Résolution en cours...")
solution = predict_sudoku(grille_test)
print("Voici la solution proposée par l'IA :\n")
print(solution)