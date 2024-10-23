import numpy as np
import cv2

class MarchingSquares:
    def __init__(self, image_path, threshold=127):
        # Charger l'image
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError("Impossible de charger l'image")
        
        # Convertir en niveaux de gris et normaliser
        self.grid = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY).astype(float) / 255.0
        self.original_image = img
        self.threshold = threshold / 255.0
        self.rows, self.cols = self.grid.shape
        
        # Table des cas de Marching Squares (simplifié pour la lisibilité)
        self.CASES = {
            # Pas de contour
            0: [],
            15: [],
            # Contours simples
            1: [[[0.5, 0], [0, 0.5]]],    # ╝
            2: [[[1, 0.5], [0.5, 0]]],    # ╚
            3: [[[1, 0.5], [0, 0.5]]],    # ═
            4: [[[1, 0.5], [0.5, 1]]],    # ╔
            6: [[[0.5, 0], [0.5, 1]]],    # ║
            7: [[[0, 0.5], [0.5, 1]]],    # ╗
            8: [[[0, 0.5], [0.5, 1]]],    # ╝
            9: [[[0.5, 0], [0.5, 1]]],    # ║
            11: [[[1, 0.5], [0.5, 1]]],   # ╔
            12: [[[0, 0.5], [1, 0.5]]],   # ═
            13: [[[0.5, 0], [1, 0.5]]],   # ╚
            14: [[[0.5, 0], [0, 0.5]]],   # ╗
            # Cas ambigus
            5: [[[0.5, 0], [0, 0.5]], [[1, 0.5], [0.5, 1]]],
            10: [[[0.5, 0], [1, 0.5]], [[0, 0.5], [0.5, 1]]]
        }

    def get_square_value(self, row, col):
        """Détermine la configuration d'une cellule."""
        value = 0
        # Vérifier les 4 coins dans cet ordre: bas-gauche, bas-droite, haut-droite, haut-gauche
        corners = [
            (row+1, col), (row+1, col+1),
            (row, col+1), (row, col)
        ]
        
        for i, (r, c) in enumerate(corners):
            if self.grid[r, c] > self.threshold:
                value |= 1 << i
        
        return value

    def generate_contours(self):
        """Génère les segments de contour."""
        contours = []
        
        for row in range(self.rows - 1):
            for col in range(self.cols - 1):
                # Obtenir la configuration de la cellule
                case = self.get_square_value(row, col)
                
                # Générer les segments pour cette configuration
                for segment in self.CASES[case]:
                    start = [col + segment[0][0], row + segment[0][1]]
                    end = [col + segment[1][0], row + segment[1][1]]
                    contours.append([start, end])
        
        return contours

    def draw_contours(self, thickness=1):
        """Dessine les contours sur l'image."""
        result = self.original_image.copy()
        contours = self.generate_contours()
        
        for segment in contours:
            pt1 = (int(segment[0][0]), int(segment[0][1]))
            pt2 = (int(segment[1][0]), int(segment[1][1]))
            cv2.line(result, pt1, pt2, (0, 255, 0), thickness)
        
        return result

# Utilisation simple
def process_image(image_path, threshold=127):
    # Créer et exécuter l'algorithme
    ms = MarchingSquares(image_path, threshold)
    result = ms.draw_contours()
    
    # Afficher le résultat
    cv2.imshow('Contours', result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    process_image("image.jpg", threshold=127)