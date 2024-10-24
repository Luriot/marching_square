# Générateur de Contours d'Images par Marching Squares

Cette implémentation Python de l'algorithme Marching Squares génère des lignes de contour à partir d'images. Elle crée des dessins en noir et blanc épurés qui capturent les formes et les frontières essentielles de l'image d'entrée.

## Fonctionnalités

- Conversion de n'importe quelle image en lignes de contour
- Sélection automatique ou manuelle du seuil
- Épaisseur des lignes réglable
- Sortie en lignes noires sur fond blanc
- Implémentation simple et efficace

## Installation

### Prérequis

```bash
pip install numpy opencv-python
```

### Dépendances

- Python 3.6+
- NumPy
- OpenCV (cv2)

## Utilisation

### Utilisation Simple

```python
from marching_squares import process_image

# Utilisation du seuil automatique
process_image("entree.jpg", "sortie.png")

# Utilisation du seuil manuel (0-255)
process_image("entree.jpg", "sortie.png", threshold=127)

# Ajustement de l'épaisseur des lignes
process_image("entree.jpg", "sortie.png", threshold=127, thickness=2)
```

### Utilisation Avancée

```python
from marching_squares import MarchingSquares

# Création d'une instance avec seuil automatique
ms = MarchingSquares("entree.jpg")

# Création d'une instance avec seuil manuel
ms = MarchingSquares("entree.jpg", threshold=127)

# Génération et sauvegarde des contours
result = ms.draw_contours(thickness=1)
cv2.imwrite("sortie.png", result)
```

## Fonctionnement

L'algorithme Marching Squares fonctionne en :

1. Convertissant l'image d'entrée en niveaux de gris
2. Appliquant un seuil (automatique ou manuel) pour créer une image binaire
3. Analysant des grilles de 2x2 pixels pour déterminer les motifs de contour
4. Dessinant les segments de ligne correspondants
5. Combinant tous les segments pour créer le dessin final des contours

### Sélection du Seuil

- **Automatique** : Utilise la valeur moyenne de l'image comme seuil
- **Manuel** : Accepte une valeur entre 0-255 pour définir le seuil manuellement

## Exemples

Voici comment différentes valeurs de seuil affectent la sortie :

```python
# Contours très détaillés
process_image("image.jpg", "detaille.png", threshold=64)

# Contours équilibrés (automatique)
process_image("image.jpg", "equilibre.png")

# Contours minimaux
process_image("image.jpg", "minimal.png", threshold=192)
```

## Sortie

Le programme génère :
- Une image PNG avec des lignes de contour noires sur fond blanc
- Une sortie console indiquant la valeur du seuil utilisée

## Licence

Ce projet est sous licence MIT - voir le fichier LICENSE pour plus de détails.

## Auteur

[Luriot]
