# Générateur de Contours d'Images par Marching Squares

![License](https://img.shields.io/badge/license-MIT-green)

Cette implémentation Python de l'algorithme Marching Squares génère des lignes de contour à partir d'images. Elle crée des dessins en noir et blanc épurés qui capturent les formes et les frontières essentielles de l'image d'entrée.

## Fonctionnalités

- Conversion de n'importe quelle image en lignes de contour
- Sélection automatique ou manuelle du seuil
- Épaisseur des lignes réglable
- Sortie en lignes noires sur fond blanc
- Implémentation simple et efficace

## Structure du Projet

```
marching_squares/
│
├── marching_squares.py     # Fichier principal contenant l'algorithme (ancien main.py)
├── image.png               # Image d'entrée qui sera traitée par Marching Squares
└── README.md              # Ce fichier
```

## Installation

### Prérequis

```bash
pip install numpy opencv-python
```

### Dépendances

- Python 3.6+
- NumPy
- OpenCV (cv2)

### Utilisation

```python
from marching_squares import process_image

# Utilisation du seuil automatique
process_image("entree.jpg", "sortie.png")

# Utilisation du seuil manuel (0-255)
process_image("entree.jpg", "sortie.png", threshold=127)

# Ajustement de l'épaisseur des lignes (1 par défaut)
process_image("entree.jpg", "sortie.png", threshold=127, thickness=2)
```

### Sélection du Seuil

- **Automatique** : Utilise la valeur moyenne de l'image comme seuil
- **Manuel** : Accepte une valeur entre 0-255 pour définir le seuil manuellement

## Fonctionnement

L'algorithme Marching Squares fonctionne en :

1. Convertissant l'image d'entrée en niveaux de gris
2. Appliquant un seuil (automatique ou manuel) pour créer une image binaire
3. Analysant des grilles de 2x2 pixels pour déterminer les motifs de contour
4. Dessinant les segments de ligne correspondants
5. Combinant tous les segments pour créer le dessin final des contours

## Sortie

Le programme génère :
- Une image PNG avec des lignes de contour noires sur fond blanc
- Une sortie console indiquant la valeur du seuil utilisée

## Licence

Ce projet est sous licence MIT. Consultez le fichier [LICENSE](LICENSE) pour plus d’informations.

## Auteur

**Luriot** - [GitHub](https://github.com/Luriot)
