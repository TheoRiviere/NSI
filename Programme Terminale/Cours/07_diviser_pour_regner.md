# Terminale NSI — Chapitre 7
# Méthode « diviser pour régner »

*Support de cours — Python 3*

---

## Objectifs du chapitre

- Comprendre le principe général de la méthode « diviser pour régner ».
- Écrire un algorithme de tri fusion.
- Analyser intuitivement le coût d'un algorithme « diviser pour régner ».
- Appliquer la méthode à un exemple de traitement d'image.

**Prérequis :** récursivité (chapitre 6).

---

## 7.1 Principe général

La méthode **« diviser pour régner »** (*divide and conquer*) résout un problème en trois étapes :

1. **Diviser** : découper le problème en plusieurs sous-problèmes plus petits, de même nature ;
2. **Régner** : résoudre chaque sous-problème, en général récursivement ;
3. **Combiner** : assembler les solutions des sous-problèmes pour obtenir la solution du problème initial.

C'est une application structurée de la récursivité : les sous-problèmes sont résolus par des appels récursifs, jusqu'à atteindre des cas suffisamment petits pour être résolus directement.

---

## 7.2 Exemple : le tri fusion (*merge sort*)

### Principe

Pour trier un tableau :
1. **Diviser** : le couper en deux moitiés ;
2. **Régner** : trier récursivement chaque moitié ;
3. **Combiner** : fusionner les deux moitiés triées en un seul tableau trié.

### La fusion de deux tableaux triés

```python
def fusionner(gauche, droite):
    resultat = []
    i, j = 0, 0
    while i < len(gauche) and j < len(droite):
        if gauche[i] <= droite[j]:
            resultat.append(gauche[i])
            i += 1
        else:
            resultat.append(droite[j])
            j += 1
    resultat.extend(gauche[i:])
    resultat.extend(droite[j:])
    return resultat
```

### Le tri fusion complet

```python
def tri_fusion(tableau):
    if len(tableau) <= 1:
        return tableau                       # cas de base
    milieu = len(tableau) // 2
    gauche = tri_fusion(tableau[:milieu])    # diviser + régner (partie gauche)
    droite = tri_fusion(tableau[milieu:])    # diviser + régner (partie droite)
    return fusionner(gauche, droite)          # combiner
```

**Exemple :** `tri_fusion([5, 3, 8, 1, 9, 2])` renvoie `[1, 2, 3, 5, 8, 9]`.

### Déroulement schématique

```
[5, 3, 8, 1, 9, 2]
        |
   divise en 2
   /            \
[5, 3, 8]      [1, 9, 2]
   |               |
 divise         divise
 /    \          /   \
[5]  [3,8]     [1]  [9,2]
      /  \           /  \
    [3]  [8]       [9]  [2]

  ... puis on fusionne en remontant :
[3,8] fusionné, [9,2] -> [2,9], etc.
```

---

## 7.3 Analyse du coût

Pour un tableau de taille `n`, le tri fusion effectue :

- 2 appels récursifs sur des tableaux de taille `n/2` ;
- une fusion, dont le coût est proportionnel à `n` (on parcourt une fois chaque élément).

On peut représenter ce coût par la relation `T(n) = 2 T(n/2) + n` (approximativement). En développant cette relation (c'est-à-dire en comptant le travail effectué à chaque niveau de récursion), on obtient un coût total en **`n log₂ n`** : à chaque niveau de la récursion, le travail total de fusion est d'environ `n` ; et il y a environ `log₂ n` niveaux (puisque la taille est divisée par 2 à chaque niveau).

> **À comparer.** Le tri par sélection ou le tri par insertion (vus en première) ont un coût en `n²`. Pour `n = 1 000 000`, `n log₂ n` vaut environ 20 millions, alors que `n²` vaut 1 000 milliards : la différence est considérable en pratique.

---

## 7.4 Un autre exemple : rotation d'une image bitmap

On représente une image carrée par un tableau de tableaux de pixels (chapitre 1). On veut la faire pivoter d'un quart de tour (90°) **sans utiliser de tableau auxiliaire de même taille**, c'est-à-dire avec un coût en mémoire supplémentaire **constant** (on dit qu'on travaille *en place*).

### Rotation en place, par couches concentriques

L'idée « diviser pour régner » consiste ici à voir l'image comme une suite de **couches carrées concentriques** (le bord extérieur, puis le carré immédiatement à l'intérieur, etc.) : faire pivoter l'image revient à faire pivoter chaque couche indépendamment, et chaque couche se traite en échangeant ses valeurs quatre par quatre.

```python
def rotation_90_degres(image):
    n = len(image)
    for couche in range(n // 2):
        premier = couche
        dernier = n - 1 - couche
        for i in range(premier, dernier):
            decalage = i - premier
            # on sauvegarde le haut
            haut = image[premier][i]
            # gauche -> haut
            image[premier][i] = image[dernier - decalage][premier]
            # bas -> gauche
            image[dernier - decalage][premier] = image[dernier][dernier - decalage]
            # droite -> bas
            image[dernier][dernier - decalage] = image[i][dernier]
            # haut (sauvegardé) -> droite
            image[i][dernier] = haut
    return image
```

**Exemple :**

```python
image = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
]
rotation_90_degres(image)
# [[7, 4, 1],
#  [8, 5, 2],
#  [9, 6, 3]]
```

Ce traitement ne crée aucun tableau auxiliaire de la taille de l'image : seules quelques variables (`haut`, `premier`, `dernier`, `decalage`) sont utilisées, quel que soit `n`. C'est un bon exemple où l'esprit « diviser pour régner » (traiter indépendamment des sous-parties du problème — ici, les couches) permet d'obtenir un algorithme économe en mémoire.

---

## 7.5 Synthèse

| Étape | Rôle |
|---|---|
| Diviser | Découper le problème en sous-problèmes plus petits, de même nature |
| Régner | Résoudre chaque sous-problème, généralement par récursivité |
| Combiner | Assembler les solutions des sous-problèmes |

| Notion | Point clé |
|---|---|
| Tri fusion | Diviser en deux moitiés, trier récursivement, fusionner ; coût en `n log₂ n` |
| Rotation d'image en place | Illustration d'un traitement « diviser pour régner » à coût mémoire constant |

*Prochaine étape suggérée : chapitre 8, la programmation dynamique, qui optimise les problèmes où les sous-problèmes se recoupent (contrairement au tri fusion, où ils sont indépendants).*
