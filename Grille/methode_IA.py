#full IA : 
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '1'

import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models

def solve_sudoku_ia():
    # --- 1. CHARGEMENT ET PRÉPARATION DES DONNÉES ---
    print("Chargement du dataset...")
    # On prend 100 000 grilles pour commencer 
    df = pd.read_csv('sudoku.csv', nrows=1000000)
    
    def prepare_data(data_column):
        # Transforme les strings de 81 chiffres en matrices (100000, 9, 9, 1)
        arrays = np.array([np.array([int(c) for c in s]).reshape(9, 9, 1) for s in data_column])
        return arrays

    # X = Grilles à trous (Entrées), Y = Grilles résolues (Cibles)
    X = prepare_data(df['quizzes']) / 9.0  # Normalisation (0 à 1) pour aider 
    Y = prepare_data(df['solutions']) - 1   # On décale de 1 (0-8) pour la classification
    
    print(f"Données prêtes : {X.shape[0]} grilles chargées.")

    # --- 2. ARCHITECTURE DU RÉSEAU DE NEURONES (CNN) ---
    model = models.Sequential([
        # Couche d'entrée : reçoit une image 9x9 en noir et blanc (1 canal)
        layers.Input(shape=(9, 9, 1)),
        
        # Bloc de Convolution 1 : Détecte les chiffres proches
        layers.Conv2D(64, kernel_size=(3,3), activation='relu', padding='same'),
        layers.BatchNormalization(), # Stabilise l'apprentissage
        
        # Bloc de Convolution 2 : Analyse les lignes et colonnes
        layers.Conv2D(128, kernel_size=(3,3), activation='relu', padding='same'),
        layers.BatchNormalization(),
        
        # Bloc de Convolution 3 : Compréhension globale de la grille
        layers.Conv2D(128, kernel_size=(3,3), activation='relu', padding='same'),
        layers.BatchNormalization(),

        # Couche de sortie : On veut 81 cases, et pour chaque case, 9 probabilités (chiffres 1 à 9)
        layers.Flatten(),
        layers.Dense(81 * 9), 
        layers.Reshape((9, 9, 9)), # On redonne la forme d'un Sudoku 3D
        layers.Activation('softmax') # Donne un score de confiance (ex: 0.98 pour le chiffre 5)
    ])

    # --- 3. COMPILATION ---
    model.compile(
        optimizer='adam', 
        loss='sparse_categorical_crossentropy', 
        metrics=['accuracy']
    )

    # --- 4. ENTRAÎNEMENT SUR GPU ---
    model.fit(X, Y, batch_size=64, epochs=10, validation_split=0.1)

    # --- 5. SAUVEGARDE ---
    model.save('sudoku_model.h5')
    print("\nModèle sauvegardé sous 'sudoku_model.h5' !")

# Lancer la fonction
if __name__ == "__main__":
    solve_sudoku_ia()