import numpy as np
import matplotlib.pyplot as plt
import cv2

class MarchingSquares:
    def __init__(self, image_path, threshold=127):
        # Charger et prétraiter l'image
        self.original_image = cv2.imread(image_path)
        if self.original_image is None:
            raise ValueError("Impossible de charger l'image")
            
        # Convertir en niveaux de gris si l'image est en couleur
        if len(self.original_image.shape) == 3:
            self.grid = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
        else:
            self.grid = self.original_image.copy()
            
        # Normaliser les valeurs entre 0 et 1
        self.grid = self.grid.astype(float) / 255.0
        
        self.threshold = threshold / 255.0  # Normaliser le seuil aussi
        self.rows, self.cols = self.grid.shape
        self.contours = []
        
        # Table de correspondance des cas
        self.CASES = {
            0: [],
            1: [[[0.5, 0], [0, 0.5]]],
            2: [[[1, 0.5], [0.5, 0]]],
            3: [[[1, 0.5], [0, 0.5]]],
            4: [[[1, 0.5], [0.5, 1]]],
            5: [[[0.5, 0], [0, 0.5]], [[1, 0.5], [0.5, 1]]],
            6: [[[0.5, 0], [0.5, 1]]],
            7: [[[0, 0.5], [0.5, 1]]],
            8: [[[0, 0.5], [0.5, 1]]],
            9: [[[0.5, 0], [0.5, 1]]],
            10: [[[0.5, 0], [1, 0.5]], [[0, 0.5], [0.5, 1]]],
            11: [[[1, 0.5], [0.5, 1]]],
            12: [[[0, 0.5], [1, 0.5]]],
            13: [[[0.5, 0], [1, 0.5]]],
            14: [[[0.5, 0], [0, 0.5]]],
            15: []
        }

    def preprocess_image(self, blur_size=5, use_adaptive_threshold=False):
        """Prétraitement de l'image pour améliorer la détection des contours"""
        # Appliquer un flou gaussien pour réduire le bruit
        self.grid = cv2.GaussianBlur(self.grid, (blur_size, blur_size), 0)
        
        if use_adaptive_threshold:
            # Utiliser un seuillage adaptatif
            binary = cv2.adaptiveThreshold(
                (self.grid * 255).astype(np.uint8),
                255,
                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY,
                11,
                2
            )
            self.grid = binary.astype(float) / 255.0

    def get_cell_configuration(self, row, col):
        """Calcule la configuration d'une cellule basée sur ses quatre coins."""
        value = 0
        corners = [
            self.grid[row+1, col],     # Coin bas gauche
            self.grid[row+1, col+1],   # Coin bas droit
            self.grid[row, col+1],     # Coin haut droit
            self.grid[row, col]        # Coin haut gauche
        ]
        
        for i, corner in enumerate(corners):
            if corner > self.threshold:
                value |= 1 << i
        
        return value

    def generate_contours(self):
        """Génère les contours pour toute la grille."""
        self.contours = []  # Réinitialiser les contours
        
        for row in range(self.rows - 1):
            for col in range(self.cols - 1):
                cell_value = self.get_cell_configuration(row, col)
                segments = self.CASES[cell_value]
                
                for segment in segments:
                    start = [col + segment[0][0], row + segment[0][1]]
                    end = [col + segment[1][0], row + segment[1][1]]
                    self.contours.append([start, end])
        
        return self.contours

    def draw_result(self, line_thickness=1):
        """Dessine les contours sur l'image originale."""
        # Créer une copie de l'image originale
        result = self.original_image.copy()
        
        # Convertir les coordonnées des contours en points pour OpenCV
        for segment in self.contours:
            start_point = (int(segment[0][0]), int(segment[0][1]))
            end_point = (int(segment[1][0]), int(segment[1][1]))
            
            cv2.line(result, start_point, end_point, (0, 255, 0), line_thickness)
        
        return result

    def plot_debug(self):
        """Affiche les différentes étapes du traitement pour le débogage."""
        plt.figure(figsize=(15, 5))
        
        # Image originale
        plt.subplot(131)
        plt.imshow(cv2.cvtColor(self.original_image, cv2.COLOR_BGR2RGB))
        plt.title('Image originale')
        
        # Grille en niveaux de gris
        plt.subplot(132)
        plt.imshow(self.grid, cmap='gray')
        plt.title('Grille normalisée')
        
        # Résultat avec contours
        plt.subplot(133)
        result = self.draw_result()
        plt.imshow(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
        plt.title('Contours détectés')
        
        plt.tight_layout()
        plt.show()

# Exemple d'utilisation
def process_image(image_path, threshold=127, blur_size=5, use_adaptive_threshold=False):
    """Fonction utilitaire pour traiter une image."""
    # Créer l'instance de MarchingSquares
    ms = MarchingSquares(image_path, threshold)
    
    # Prétraiter l'image
    ms.preprocess_image(blur_size, use_adaptive_threshold)
    
    # Générer les contours
    ms.generate_contours()
    
    # Afficher les résultats
    ms.plot_debug()
    
    # Retourner l'image avec les contours
    return ms.draw_result()

# Exemple d'utilisation
if __name__ == "__main__":
    # Remplacer par le chemin de votre image
    image_path = "votre_image.jpg"
    result = process_image(
        image_path,
        threshold=127,  # Seuil pour la binarisation (0-255)
        blur_size=5,    # Taille du flou gaussien
        use_adaptive_threshold=False  # Utiliser ou non le seuillage adaptatif
    )
    
    # Afficher le résultat dans une fenêtre OpenCV
    cv2.imshow('Résultat', result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()