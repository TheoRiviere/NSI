# Chapitre 11 — Algorithme des k plus proches voisins
## Évaluation

*Première NSI — Durée : 50 min — Barème sur 20 points*

---

On donne le jeu de données d'entraînement suivant :
```python
points_entrainement = [
    ((1, 1), "rouge"),
    ((2, 1), "rouge"),
    ((1, 2), "rouge"),
    ((5, 5), "bleu"),
    ((6, 5), "bleu"),
    ((5, 6), "bleu"),
]
```

---

### Partie 1 — Questions de cours (7 points)

**Question 1 (2 pts).** Décrire, en trois étapes, le principe de l'algorithme des k plus proches voisins.

**Question 2 (2 pts).** Pourquoi choisit-on généralement une valeur de `k` **impaire** lorsqu'il n'y a que deux catégories possibles ?

**Question 3 (3 pts).** Qu'est-ce qu'un jeu de test, et pourquoi ne doit-il jamais être identique (ou même partiellement superposé) au jeu d'entraînement lors de l'évaluation d'un classifieur ?

---

### Partie 2 — Calculs et classification (8 points)

**Question 4 (3 pts).** Calculer la distance euclidienne entre le point `(2, 2)` et chacun des 6 points de `points_entrainement`.

**Question 5 (3 pts).** En déduire les 3 plus proches voisins du point `(2, 2)`, et la catégorie qui lui serait attribuée avec `k=3`.

**Question 6 (2 pts).** Cette prédiction change-t-elle avec `k=1` ? Justifier.

---

### Partie 3 — Écrire du code (5 points)

**Question 7 (5 pts).** Écrire une fonction `distance_maximale(donnees, nouveau_point, k)` qui renvoie la plus grande distance parmi celles des `k` plus proches voisins d'un point donné (c'est-à-dire la distance du `k`-ième voisin le plus proche). Cette valeur peut être utile pour estimer si un point est vraiment « proche » de données connues, ou au contraire isolé.

---

## Corrigé et barème détaillé

### Partie 1 (7 pts)

**Q1 (2 pts)** — Calculer la distance entre le nouveau point et chaque point du jeu d'entraînement (0,7 pt) ; sélectionner les `k` points les plus proches (0,7 pt) ; attribuer au nouveau point l'étiquette majoritaire parmi ces `k` voisins (0,6 pt).

**Q2 (2 pts)** — Avec un `k` pair et deux catégories, un vote peut aboutir à une **égalité stricte** (par exemple 2 voisins d'une catégorie contre 2 de l'autre), ce qui ne permet pas de trancher clairement ; un `k` impair garantit qu'une des deux catégories sera toujours strictement majoritaire.

**Q3 (3 pts)** — Un jeu de test est un ensemble de données, dont on connaît la vraie étiquette, mais qui n'a pas servi à l'apprentissage (1,5 pt). S'il chevauchait le jeu d'entraînement, le classifieur pourrait « reconnaître » des données déjà vues (voire les retrouver comme leur propre plus proche voisin, à distance nulle), ce qui donnerait une précision artificiellement élevée, ne reflétant pas la capacité réelle du modèle à généraliser à des données nouvelles (1,5 pt).

### Partie 2 (8 pts)

**Q4 (3 pts)** — Distances entre `(2,2)` et chaque point : `(1,1)` → `√2 ≈ 1.41` ; `(2,1)` → `1.0` ; `(1,2)` → `1.0` ; `(5,5)` → `√18 ≈ 4.24` ; `(6,5)` → `5.0` ; `(5,6)` → `5.0`. *(0,5 pt par distance correcte.)*

**Q5 (3 pts)** — Les 3 plus proches voisins sont `(2,1)` (distance 1.0, "rouge"), `(1,2)` (distance 1.0, "rouge"), `(1,1)` (distance ≈1.41, "rouge") (2 pts). Les trois voisins sont "rouge" : la catégorie prédite est donc **"rouge"** (1 pt).

**Q6 (2 pts)** — Avec `k=1`, on ne considère que le voisin le plus proche parmi `(2,1)` et `(1,2)` (tous deux à distance exactement `1.0` — cas d'égalité de distance, un seul est retenu selon l'implémentation), qui est de toute façon étiqueté "rouge" : la prédiction reste donc **"rouge"**, inchangée.

### Partie 3 (5 pts)

**Q7 (5 pts)**
```python
def distance_maximale(donnees, nouveau_point, k):
    voisins = k_plus_proches_voisins(donnees, nouveau_point, k)
    return voisins[-1][0]
```
*(3 pts pour la récupération correcte des k plus proches voisins, 2 pts pour l'extraction correcte de la plus grande distance parmi eux — le dernier élément d'une liste triée par distance croissante.)*

---

**Barème global : 7 + 8 + 5 = 20 points.**
