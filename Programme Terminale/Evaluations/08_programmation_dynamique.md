# Chapitre 8 — Programmation dynamique
## Évaluation

*Terminale NSI — Durée : 55 min — Barème sur 20 points*

---

### Partie 1 — Questions de cours (6 points)

**Question 1 (2 pts).** À quelle condition sur les sous-problèmes la programmation dynamique apporte-t-elle un gain par rapport à une récursivité naïve ?

**Question 2 (2 pts).** Distinguer mémoïsation et tabulation.

**Question 3 (2 pts).** Dans le problème du rendu de monnaie, que représente `cout[s]` ? Donner la relation qui permet de le calculer à partir de valeurs déjà connues.

---

### Partie 2 — Lecture et calcul (7 points)

**Question 4 (3 pts).** On exécute `rendu_monnaie([1, 5, 6], 10)` avec la fonction du cours. Donner le résultat, en explicitant la décomposition optimale trouvée.

**Question 5 (4 pts).** On considère les mots `"lac"` et `"bac"`. Construire la table de programmation dynamique de `distance_edition("lac", "bac")`, puis donner la distance obtenue.

---

### Partie 3 — Écrire une fonction (7 points)

**Question 6 (7 pts).** On souhaite calculer, par programmation dynamique (tabulation), le nombre de façons différentes de gravir un escalier de `n` marches, sachant qu'à chaque pas on peut monter soit **une** marche, soit **deux** marches. Par exemple, pour `n = 3`, il y a 3 façons : `1+1+1`, `1+2`, `2+1`.

Écrire une fonction `nombre_facons(n)` qui calcule ce nombre par tabulation (indication : le nombre de façons d'atteindre la marche `i` est la somme du nombre de façons d'atteindre la marche `i-1` et la marche `i-2`, avec `nombre_facons(0) = 1` et `nombre_facons(1) = 1`).

---

## Corrigé et barème détaillé

### Partie 1 (6 pts)

**Q1 (2 pts)** — Lorsque les sous-problèmes **se recoupent**, c'est-à-dire que les mêmes sous-problèmes réapparaissent plusieurs fois au cours du calcul récursif : mémoriser leur résultat évite de les recalculer.

**Q2 (2 pts)** — La mémoïsation est une approche descendante qui garde la récursivité et stocke chaque résultat déjà calculé (1 pt). La tabulation est une approche ascendante, itérative, qui construit un tableau de solutions des plus petits sous-problèmes vers le plus grand, sans récursivité (1 pt).

**Q3 (2 pts)** — `cout[s]` représente le nombre minimal de pièces nécessaires pour rendre exactement la somme `s` (1 pt). Relation : `cout[s] = 1 + min(cout[s - p])` pour chaque pièce `p` telle que `p <= s` (1 pt).

### Partie 2 (7 pts)

**Q4 (3 pts)** — `rendu_monnaie([1, 5, 6], 10)` renvoie `2` : la décomposition optimale est `5 + 5` (2 pièces), alors qu'une décomposition comme `6 + 1 + 1 + 1 + 1` en demanderait 5. *(1 pt pour la valeur numérique, 2 pts pour la décomposition correcte justifiant ce nombre.)*

**Q5 (4 pts)** — Table pour `"lac"` (lignes) et `"bac"` (colonnes) :

|   |   | b | a | c |
|---|---|---|---|---|
|   | 0 | 1 | 2 | 3 |
| l | 1 | 1 | 2 | 3 |
| a | 2 | 2 | 1 | 2 |
| c | 3 | 3 | 2 | 1 |

Distance obtenue : **1** (une seule substitution : `l` devient `b`). *(2 pts pour une table correcte ou majoritairement correcte, 2 pts pour la valeur finale correcte.)*

### Partie 3 (7 pts)

**Q6 (7 pts)**
```python
def nombre_facons(n):
    if n <= 1:
        return 1
    table = [0] * (n + 1)
    table[0] = 1
    table[1] = 1
    for i in range(2, n + 1):
        table[i] = table[i - 1] + table[i - 2]
    return table[n]
```
*(1 pt cas de base ; 2 pts initialisation correcte du tableau ; 3 pts boucle de remplissage correcte ; 1 pt valeur de retour.)*

---

**Barème global : 6 + 7 + 7 = 20 points.**
