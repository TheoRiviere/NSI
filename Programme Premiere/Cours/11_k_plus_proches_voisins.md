# Chapitre 11 — Algorithme des k plus proches voisins

## Objectifs

- Comprendre le principe de la classification par apprentissage supervisé.
- Écrire l'algorithme des k plus proches voisins (k-NN).
- Comprendre l'influence du choix de `k` sur le résultat.
- Évaluer la performance d'un classifieur sur un jeu de test.

## Prérequis

- Distance euclidienne, tableaux et tris — chapitres 2, 9, 10.

---

## 1. Le problème de la classification

**Classifier** une donnée consiste à lui attribuer une **catégorie** (une étiquette) parmi un ensemble de catégories possibles, en se basant sur ses caractéristiques. Par exemple : classer un fruit comme « pomme » ou « banane » à partir de son poids et de son diamètre ; classer un courriel comme « spam » ou « non spam » ; reconnaître le chiffre manuscrit représenté par une image.

L'algorithme des **k plus proches voisins** (*k-nearest neighbors*, k-NN) est une méthode simple d'**apprentissage supervisé** : on dispose d'un ensemble de données déjà étiquetées (les **données d'entraînement**), et on souhaite prédire l'étiquette d'une **nouvelle** donnée, encore inconnue.

---

## 2. Représenter les données et mesurer une distance

### 2.1 Représentation

Chaque donnée est représentée par un **point** dans un espace à plusieurs dimensions (une dimension par caractéristique mesurée), accompagné de son étiquette :

```python
donnees_entrainement = [
    ((150, 7.0), "pomme"),
    ((170, 7.5), "pomme"),
    ((140, 6.5), "pomme"),
    ((130, 20.0), "banane"),
    ((120, 18.0), "banane"),
    ((135, 19.5), "banane"),
]
# chaque point : (poids en grammes, diamètre en cm)
```

### 2.2 La distance euclidienne

Pour déterminer si deux points se « ressemblent », on mesure la **distance** entre eux. La distance euclidienne généralise le théorème de Pythagore à un nombre quelconque de dimensions :

```python
import math

def distance_euclidienne(p1, p2):
    """Distance euclidienne entre deux points de même dimension."""
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(p1, p2)))

distance_euclidienne((0, 0), (3, 4))          # 5.0
distance_euclidienne((0, 0, 0), (1, 1, 1))    # racine de 3, environ 1.73
```

`zip(p1, p2)` associe chaque coordonnée de `p1` à la coordonnée correspondante de `p2`, ce qui permet à cette fonction de fonctionner quel que soit le nombre de dimensions des points (2, 3, ou davantage).

---

## 3. L'algorithme des k plus proches voisins

### 3.1 Principe

Pour classer une nouvelle donnée :

1. Calculer la **distance** entre la nouvelle donnée et **chacune** des données d'entraînement.
2. Sélectionner les **k** données d'entraînement les plus proches (les « k plus proches voisins »).
3. Attribuer à la nouvelle donnée l'étiquette **majoritaire** parmi ces k voisins (un vote).

```python
def k_plus_proches_voisins(donnees, nouveau_point, k):
    """Renvoie les k couples (distance, étiquette) les plus proches de nouveau_point."""
    distances = []
    for point, etiquette in donnees:
        d = distance_euclidienne(point, nouveau_point)
        distances.append((d, etiquette))
    distances.sort(key=lambda x: x[0])
    return distances[:k]


from collections import Counter

def classifier(donnees, nouveau_point, k):
    """Prédit l'étiquette de nouveau_point par vote majoritaire des k plus proches voisins."""
    voisins = k_plus_proches_voisins(donnees, nouveau_point, k)
    etiquettes = [etiquette for distance, etiquette in voisins]
    compteur = Counter(etiquettes)
    return compteur.most_common(1)[0][0]   # l'étiquette la plus fréquente
```

`Counter` (du module `collections`) compte automatiquement les occurrences de chaque élément d'une liste ; `.most_common(1)` renvoie une liste contenant le couple `(élément, nombre d'occurrences)` le plus fréquent.

### 3.2 Exemple

```python
classifier(donnees_entrainement, (145, 7.2), 3)    # 'pomme'
classifier(donnees_entrainement, (125, 19.0), 3)    # 'banane'
```

Le point `(145, 7.2)` (poids proche de 145g, diamètre proche de 7.2cm) se trouve, en distance, beaucoup plus proche des trois points étiquetés « pomme » que des points « banane » : le vote majoritaire parmi ses 3 plus proches voisins donne donc « pomme ».

---

## 4. L'influence du choix de `k`

Le choix de la valeur de `k` a une influence importante sur le comportement du classifieur :

- Un `k` **trop petit** (par exemple `k=1`) rend la prédiction très sensible aux données individuelles, y compris à d'éventuelles erreurs ou valeurs aberrantes dans les données d'entraînement (on dit que le modèle **sur-apprend**, ou *overfitte*).
- Un `k` **trop grand** risque au contraire de « diluer » l'information utile en prenant en compte des voisins trop éloignés, parfois majoritairement d'une autre catégorie, ce qui peut dégrader la prédiction.
- En pratique, on choisit souvent une valeur de `k` **impaire** (pour éviter les égalités de vote lors d'une classification à deux catégories), et l'on teste plusieurs valeurs pour déterminer celle qui donne les meilleurs résultats sur des données de test.

---

## 5. Évaluer un classifieur : jeu de test et précision

Pour savoir si un classifieur fonctionne bien, on l'évalue sur un **jeu de test** : un ensemble de données dont on connaît la vraie étiquette, mais qui n'a **pas** été utilisé pour l'apprentissage (sinon l'évaluation serait faussée, le modèle ayant déjà « vu » la réponse).

```python
def evaluer_precision(donnees_entrainement, donnees_test, k):
    """Calcule la proportion de bonnes prédictions sur le jeu de test."""
    bonnes_predictions = 0
    for point, vraie_etiquette in donnees_test:
        prediction = classifier(donnees_entrainement, point, k)
        if prediction == vraie_etiquette:
            bonnes_predictions += 1
    return bonnes_predictions / len(donnees_test)
```

La **précision** (proportion de prédictions correctes) est une mesure simple, mais essentielle, de la qualité d'un classifieur — un modèle qui n'obtiendrait que 50% de précision sur une classification à deux catégories ne ferait pas mieux qu'un tirage au hasard.

---

## Synthèse

| Notion | Point clé à retenir |
|---|---|
| Classification | Attribuer une étiquette à une donnée à partir de ses caractéristiques |
| Distance euclidienne | Mesure de « ressemblance » entre deux points |
| k-NN | Trouver les k voisins les plus proches, puis voter pour l'étiquette majoritaire |
| Choix de `k` | Trop petit : sensible au bruit ; trop grand : dilue l'information |
| Jeu de test | Données non utilisées pour l'apprentissage, servant à évaluer le modèle |
| Précision | Proportion de prédictions correctes sur le jeu de test |

*Prochaine étape suggérée : Chapitre 12 — Algorithmes gloutons.*
