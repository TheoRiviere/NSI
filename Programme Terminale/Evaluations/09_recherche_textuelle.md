# Chapitre 9 — Recherche textuelle
## Évaluation

*Terminale NSI — Durée : 50 min — Barème sur 20 points*

---

### Partie 1 — Questions de cours (7 points)

**Question 1 (2 pts).** Dans l'algorithme naïf, dans quel ordre compare-t-on les caractères ? Et dans l'algorithme de Boyer-Moore ?

**Question 2 (3 pts).** Expliquer, en quelques phrases, le principe de la règle du mauvais caractère.

**Question 3 (2 pts).** Qu'appelle-t-on le prétraitement du motif dans l'algorithme de Boyer-Moore ? Pourquoi n'est-il effectué qu'une seule fois ?

---

### Partie 2 — Application (7 points)

**Question 4 (3 pts).** Construire la table des dernières occurrences du motif `"BANANE"`.

**Question 5 (4 pts).** On recherche le motif `"BANANE"` dans un texte, aligné à une certaine position. La comparaison, effectuée de droite à gauche, échoue sur le caractère `'E'` du motif (indice 5) car le texte contient à cette position le caractère `'A'`. Calculer le décalage qui sera appliqué, en utilisant la table de la question 4.

---

### Partie 3 — Écrire du code (6 points)

**Question 6 (6 pts).** Écrire une fonction `premiere_occurrence(texte, motif)` qui utilise l'algorithme de recherche **naïve** pour renvoyer l'indice de la **première** occurrence du motif dans le texte, ou `-1` si le motif n'apparaît pas (contrairement à `recherche_naive` du cours, qui renvoie toutes les positions, on s'arrêtera dès la première trouvée).

---

## Corrigé et barème détaillé

### Partie 1 (7 pts)

**Q1 (2 pts)** — Dans l'algorithme naïf, on compare les caractères du motif au texte de **gauche à droite** (1 pt). Dans Boyer-Moore, on compare de **droite à gauche** (1 pt).

**Q2 (3 pts)** — Lorsque la comparaison échoue sur un caractère `c` du texte, on recherche la dernière occurrence de `c` dans le motif (1 pt). Si `c` n'apparaît pas dans le motif, on décale le motif pour qu'il passe entièrement après la position de `c` (1 pt). Si `c` apparaît dans le motif, on décale le motif de façon à aligner cette dernière occurrence avec la position de l'échec dans le texte (1 pt).

**Q3 (2 pts)** — Le prétraitement consiste à construire, avant de parcourir le texte, la table des dernières occurrences de chaque caractère du motif (1 pt). Il n'est effectué qu'une seule fois car cette table ne dépend que du motif, pas de la position testée dans le texte : elle reste valable pour toute la recherche (1 pt).

### Partie 2 (7 pts)

**Q4 (3 pts)** — `"BANANE"` → `{"B": 0, "A": 3, "N": 4, "E": 5}`.

**Q5 (4 pts)** — Le caractère du texte est `'A'`, dont la dernière occurrence dans le motif est à l'indice 3 (table de la Q4). L'échec a lieu à l'indice `j = 5`. Décalage = `j - table["A"] = 5 - 3 = 2`. *(2 pts pour la lecture correcte de la table, 2 pts pour le calcul du décalage.)*

### Partie 3 (6 pts)

**Q6 (6 pts)**
```python
def premiere_occurrence(texte, motif):
    n, m = len(texte), len(motif)
    for i in range(n - m + 1):
        if texte[i:i + m] == motif:
            return i
    return -1
```
*(2 pts parcours correct des positions possibles ; 2 pts test de correspondance correct ; 1 pt arrêt dès la première occurrence trouvée (return immédiat) ; 1 pt valeur -1 si absent.)*

---

**Barème global : 7 + 7 + 6 = 20 points.**
