# Chapitre 10 — Tris par insertion et par sélection
## Évaluation

*Première NSI — Durée : 55 min — Barème sur 20 points*

---

### Partie 1 — Questions de cours (7 points)

**Question 1 (3 pts).** Décrire, en une phrase pour chacun, le principe du tri par sélection et celui du tri par insertion.

**Question 2 (2 pts).** Quel est le coût (nombre de comparaisons), dans le pire des cas, de chacun de ces deux algorithmes, pour un tableau de taille `n` ?

**Question 3 (2 pts).** Quelle est la différence essentielle de comportement entre les deux algorithmes lorsqu'on les applique à un tableau **déjà trié** ?

---

### Partie 2 — Tracer les deux tris (8 points)

On donne le tableau `[6, 2, 9, 4]`.

**Question 4 (4 pts).** Dérouler à la main le tri par sélection sur ce tableau : donner l'état du tableau après chaque étape de la boucle externe.

**Question 5 (4 pts).** Dérouler à la main le tri par insertion sur ce même tableau : donner l'état du tableau après chaque insertion.

---

### Partie 3 — Écrire du code (5 points)

**Question 6 (5 pts).** Écrire une fonction `est_trie(tableau)` qui renvoie `True` si le tableau donné est trié par ordre croissant, et `False` sinon (sans utiliser `sorted`). Cette fonction pourrait être utile, par exemple, pour vérifier automatiquement le résultat d'un algorithme de tri dans un jeu de tests.

---

## Corrigé et barème détaillé

### Partie 1 (7 pts)

**Q1 (3 pts)** — Le tri par sélection recherche, à chaque étape, le minimum parmi les éléments non encore triés, et l'échange avec le premier élément de cette zone (1,5 pt). Le tri par insertion considère le début du tableau comme déjà trié, et insère chaque nouvel élément à sa bonne place parmi les éléments déjà triés, en décalant si besoin (1,5 pt).

**Q2 (2 pts)** — Les deux algorithmes ont un coût, dans le pire des cas, de l'ordre de `n(n-1)/2`, c'est-à-dire **quadratique** (de l'ordre de `n²`).

**Q3 (2 pts)** — Sur un tableau déjà trié, le tri par **insertion** effectue très peu d'opérations (une seule comparaison par élément, car aucun décalage n'est nécessaire) : c'est son **meilleur cas**, de coût linéaire (1 pt). Le tri par **sélection**, en revanche, effectue **toujours** le même nombre de comparaisons (il recherche systématiquement le minimum restant, indépendamment de l'état du tableau), donc il ne bénéficie d'aucune accélération sur un tableau déjà trié (1 pt).

### Partie 2 (8 pts)

**Q4 (4 pts)** — `[6, 2, 9, 4]` : étape `i=0`, minimum = 2 (indice 1), échange avec indice 0 → `[2, 6, 9, 4]` ; étape `i=1`, minimum parmi `[6,9,4]` = 4 (indice 3), échange avec indice 1 → `[2, 4, 9, 6]` ; étape `i=2`, minimum parmi `[9,6]` = 6 (indice 3), échange avec indice 2 → `[2, 4, 6, 9]`. *(un peu plus d'1 pt par étape correcte.)*

**Q5 (4 pts)** — `[6, 2, 9, 4]` : insertion de `2` (i=1) : `2 < 6`, décalage → `[2, 6, 9, 4]` ; insertion de `9` (i=2) : `9 > 6`, pas de décalage → `[2, 6, 9, 4]` ; insertion de `4` (i=3) : `4 < 9`, décalage, `4 < 6`, décalage, `4 > 2`, arrêt → `[2, 4, 6, 9]`. *(un peu plus d'1 pt par étape correcte.)*

### Partie 3 (5 pts)

**Q6 (5 pts)**
```python
def est_trie(tableau):
    for i in range(len(tableau) - 1):
        if tableau[i] > tableau[i + 1]:
            return False
    return True
```
*(3 pts pour la comparaison correcte d'éléments consécutifs, 2 pts pour la gestion correcte des bornes de la boucle — éviter un dépassement d'indice.)*

---

**Barème global : 7 + 8 + 5 = 20 points.**
