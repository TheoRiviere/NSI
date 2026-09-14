# Chapitre 8 — Programmation dynamique
## Fiche d'exercices

*Terminale NSI — Python 3*

---

### Exercice 1 — Vocabulaire

1. Quelle est la différence entre la mémoïsation et la tabulation ?
2. Pourquoi le tri fusion (chapitre 7) ne relève-t-il pas de la programmation dynamique, alors qu'il utilise aussi la récursivité et des sous-problèmes ?

### Exercice 2 — Coefficients binomiaux

Le triangle de Pascal donne les coefficients binomiaux `C(n, k)`, définis par `C(n, 0) = C(n, n) = 1` et, pour `0 < k < n`, `C(n, k) = C(n-1, k-1) + C(n-1, k)`.

1. Écrire une version récursive naïve `binom_recursif(n, k)`.
2. Écrire une version avec mémoïsation `binom_memo(n, k, memo=None)`.
3. Expliquer en une phrase pourquoi la version naïve devient très lente pour des valeurs de `n` autour de 30.

### Exercice 3 — Rendu de monnaie : retrouver les pièces

En reprenant `rendu_monnaie` du cours, modifier la fonction pour qu'elle renvoie, en plus du nombre minimal de pièces, la **liste des pièces utilisées**. *(Indication : à chaque étape, mémoriser dans un tableau `derniere_piece[s]` la pièce qui a permis d'atteindre le coût minimal pour la somme `s`, puis remonter ce tableau depuis `somme` jusqu'à `0`.)*

### Exercice 4 — Somme maximale d'un sous-tableau

Étant donné un tableau d'entiers (pouvant contenir des valeurs négatives), on veut trouver la somme maximale d'un **sous-tableau contigu** (une suite d'éléments consécutifs).

1. Justifier que ce problème se prête à la programmation dynamique : si `meilleur[i]` est la somme maximale d'un sous-tableau contigu se terminant exactement à l'indice `i`, exprimer `meilleur[i]` en fonction de `meilleur[i-1]` et `tableau[i]`.
2. En déduire une fonction `somme_max_sous_tableau(tableau)` qui calcule la réponse (le maximum de tous les `meilleur[i]`), par tabulation.

### Exercice 5 — Table de l'alignement

Dérouler à la main la construction de la table de `distance_edition("abc", "adc")`, en donnant le tableau complet `4 × 4` obtenu, et en déduire la valeur de `distance_edition("abc", "adc")`.

---

## Corrigés

### Exercice 1

1. La mémoïsation garde la structure récursive naturelle du problème et stocke chaque résultat déjà calculé au fur et à mesure des appels (approche descendante). La tabulation construit itérativement, sans récursivité, un tableau de solutions des plus petits sous-problèmes vers le plus grand (approche ascendante).
2. Dans le tri fusion, les sous-problèmes (les deux moitiés du tableau à chaque étape) sont **disjoints** : ils ne se recoupent jamais, donc il n'y a rien à mémoriser pour éviter des recalculs — ce qui est la caractéristique essentielle de la programmation dynamique.

### Exercice 2

```python
def binom_recursif(n, k):
    if k == 0 or k == n:
        return 1
    return binom_recursif(n - 1, k - 1) + binom_recursif(n - 1, k)

def binom_memo(n, k, memo=None):
    if memo is None:
        memo = {}
    if k == 0 or k == n:
        return 1
    if (n, k) in memo:
        return memo[(n, k)]
    resultat = binom_memo(n - 1, k - 1, memo) + binom_memo(n - 1, k, memo)
    memo[(n, k)] = resultat
    return resultat
```

3. La version naïve recalcule un très grand nombre de fois les mêmes couples `(n, k)` intermédiaires : le nombre total d'appels croît de façon exponentielle avec `n`, ce qui devient très coûteux dès que `n` dépasse une trentaine.

### Exercice 3

```python
def rendu_monnaie_detaille(pieces, somme):
    cout = [0] + [float("inf")] * somme
    derniere_piece = [None] * (somme + 1)
    for s in range(1, somme + 1):
        for piece in pieces:
            if piece <= s and cout[s - piece] + 1 < cout[s]:
                cout[s] = cout[s - piece] + 1
                derniere_piece[s] = piece
    if cout[somme] == float("inf"):
        return None, []
    pieces_utilisees = []
    s = somme
    while s > 0:
        p = derniere_piece[s]
        pieces_utilisees.append(p)
        s -= p
    return cout[somme], pieces_utilisees
```

### Exercice 4

1. Un sous-tableau contigu se terminant à l'indice `i` est soit réduit à l'élément `tableau[i]` seul, soit le prolongement d'un sous-tableau se terminant à l'indice `i-1` : `meilleur[i] = max(tableau[i], meilleur[i-1] + tableau[i])`.

```python
def somme_max_sous_tableau(tableau):
    meilleur = [0] * len(tableau)
    meilleur[0] = tableau[0]
    for i in range(1, len(tableau)):
        meilleur[i] = max(tableau[i], meilleur[i - 1] + tableau[i])
    return max(meilleur)
```

### Exercice 5

Table pour `distance_edition("abc", "adc")` (lignes = `"abc"`, colonnes = `"adc"`) :

|   |   | a | d | c |
|---|---|---|---|---|
|   | 0 | 1 | 2 | 3 |
| a | 1 | 0 | 1 | 2 |
| b | 2 | 1 | 1 | 2 |
| c | 3 | 2 | 2 | 1 |

`distance_edition("abc", "adc")` vaut donc **1** (une seule substitution : `b` devient `d`).
