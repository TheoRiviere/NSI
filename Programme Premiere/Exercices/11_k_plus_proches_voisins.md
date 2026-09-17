# Chapitre 11 — Algorithme des k plus proches voisins
## Fiche d'exercices

*Première NSI — Python 3*

---

### Exercice 1 — Distance euclidienne

1. Calculer, à la main, la distance euclidienne entre les points `(1, 2)` et `(4, 6)`.
2. Vérifier avec `distance_euclidienne` du cours.
3. Cette fonction fonctionne-t-elle aussi pour des points à 3 coordonnées ou plus ? Justifier en observant son implémentation.

### Exercice 2 — Classer un film

On dispose des données suivantes, représentant des films par leur durée (en minutes) et leur nombre de scènes d'action, avec leur genre :
```python
films = [
    ((90, 2), "comédie"),
    ((95, 1), "comédie"),
    ((100, 3), "comédie"),
    ((140, 15), "action"),
    ((130, 18), "action"),
    ((150, 20), "action"),
]
```

1. À l'aide de `k_plus_proches_voisins` du cours, déterminer les 3 plus proches voisins du film `(135, 16)` (135 minutes, 16 scènes d'action).
2. En déduire, avec `classifier`, le genre prédit pour ce film.
3. Ce résultat vous semble-t-il cohérent avec l'intuition (un film assez long avec beaucoup de scènes d'action) ?

### Exercice 3 — Effet du choix de `k` face à une donnée aberrante

On donne le jeu de données suivant, où un point étiqueté `"B"` a été placé, par erreur ou par exception, au milieu d'un groupe de points `"A"` :
```python
donnees = [
    ((0, 0), "B"),    # donnée isolée, entourée de "A"
    ((1, 0), "A"),
    ((-1, 0), "A"),
    ((0, 1), "A"),
    ((0, -1), "A"),
    ((3, 3), "B"),
    ((3, 4), "B"),
    ((4, 3), "B"),
    ((4, 4), "B"),
]
```

1. Classer le point `(0, 0.1)` avec `k=1`. Quel résultat obtient-on ?
2. Classer ce même point avec `k=3`, puis `k=5`. Le résultat change-t-il ?
3. Expliquer pourquoi ce jeu de données illustre bien le risque d'un `k` trop petit : quel rôle joue, ici, le point `(0, 0)` étiqueté `"B"` ?

### Exercice 4 — Évaluer un classifieur

En reprenant les données `films` de l'exercice 2, on ajoute un jeu de test :
```python
films_test = [
    ((92, 2), "comédie"),
    ((145, 17), "action"),
    ((110, 10), "action"),   # cas ambigu
]
```

1. En utilisant `evaluer_precision` du cours (avec `k=3`), calculer la précision du classifieur sur ce jeu de test.
2. Sur quel(s) film(s) le classifieur se trompe-t-il, le cas échéant ? Pourquoi ce cas peut-il être difficile à classer correctement ?

---

## Corrigés

### Exercice 1

1. Distance = `√((4-1)² + (6-2)²) = √(9+16) = √25 = 5`.
2. `distance_euclidienne((1, 2), (4, 6))` renvoie bien `5.0`.
3. Oui : la fonction utilise `zip(p1, p2)` et une somme sur toutes les paires de coordonnées obtenues, ce qui fonctionne quel que soit le nombre de coordonnées des points (à condition que `p1` et `p2` en aient le même nombre).

### Exercice 2

1.
```python
k_plus_proches_voisins(films, (135, 16), 3)
# [(distance, "action"), (distance, "action"), (distance, "action")]
```
Les trois plus proches voisins de `(135, 16)` sont tous les trois étiquetés `"action"` (les points `(140,15)`, `(130,18)`, `(150,20)`, nettement plus proches que les films « comédie »).
2. `classifier(films, (135, 16), 3)` renvoie `"action"`.
3. Oui, ce résultat est cohérent : un film de 135 minutes avec 16 scènes d'action ressemble beaucoup plus, sur ces deux critères, aux films d'action du jeu de données qu'aux comédies (qui sont plus courtes et ont très peu de scènes d'action).

### Exercice 3

1. `classifier(donnees, (0, 0.1), 1)` renvoie `"B"` : le seul et unique voisin le plus proche est le point `(0,0)`, étiqueté `"B"`.
2. Avec `k=3` et `k=5`, le résultat devient `"A"` : en prenant en compte davantage de voisins, les points `(1,0)`, `(-1,0)`, `(0,1)`, `(0,-1)` (tous étiquetés `"A"`) l'emportent largement sur l'unique point `"B"` du centre.
3. Ce jeu de données illustre le risque d'un `k` trop petit (ici `k=1`) : une seule donnée « aberrante » ou mal étiquetée (le point `(0,0)` en `"B"`, isolé au milieu d'un groupe de `"A"`) suffit à fausser complètement la prédiction, puisqu'elle est prise en compte seule et sans contrepoids. Avec un `k` plus grand, cette donnée isolée est « noyée » parmi ses véritables voisins majoritaires, ce qui rend la prédiction plus robuste face à ce type d'exception dans les données d'entraînement.

### Exercice 4

1-2. En classant chaque film du jeu de test avec `k=3` :
- `(92, 2)` → très proche des comédies → prédiction `"comédie"` → **correct**.
- `(145, 17)` → très proche des films d'action → prédiction `"action"` → **correct**.
- `(110, 10)` → cas intermédiaire, à mi-chemin entre les deux groupes → la prédiction dépend précisément de la distance aux plus proches voisins de chaque catégorie, et peut se tromper.

En exécutant le code, on obtient : `(92, 2)` → prédit `"comédie"` (correct), `(145, 17)` → prédit `"action"` (correct), `(110, 10)` → prédit **`"comédie"`**, alors que la vraie étiquette est `"action"` : **erreur**. La précision obtenue est donc de `2/3 ≈ 0.67`. Ce troisième cas est difficile car ses caractéristiques (durée et nombre de scènes d'action) sont **intermédiaires** entre les deux catégories du jeu d'entraînement : il ne ressemble fortement ni aux comédies typiques ni aux films d'action typiques, ce qui est précisément le type de cas où un classifieur k-NN peut se tromper — ses plus proches voisins se trouvent finalement légèrement plus du côté « comédie » en distance, malgré l'intuition qu'on pourrait avoir.
