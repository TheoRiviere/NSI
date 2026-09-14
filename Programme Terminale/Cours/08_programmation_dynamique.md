# Terminale NSI — Chapitre 8
# Programmation dynamique

*Support de cours — Python 3*

---

## Objectifs du chapitre

- Comprendre le principe de la programmation dynamique (mémoïsation, tabulation).
- Résoudre le problème du rendu de monnaie.
- Résoudre un problème d'alignement de séquences.
- Discuter le compromis entre coût en temps et coût en mémoire.

**Prérequis :** récursivité (chapitre 6), diviser pour régner (chapitre 7).

---

## 8.1 Le problème des sous-problèmes qui se recoupent

Au chapitre 6, on a vu que le calcul récursif naïf de `fibonacci(n)` recalcule de nombreuses fois les mêmes sous-résultats : c'est très différent du tri fusion (chapitre 7), où les sous-problèmes (les deux moitiés du tableau) sont **indépendants** et jamais recalculés.

La **programmation dynamique** s'applique précisément aux problèmes où :

1. la solution se construit à partir de solutions de sous-problèmes plus petits (comme « diviser pour régner ») ;
2. mais ces sous-problèmes **se recoupent** : les mêmes sous-problèmes réapparaissent plusieurs fois.

L'idée centrale est de **mémoriser** (stocker) le résultat de chaque sous-problème la première fois qu'on le calcule, pour ne plus jamais avoir à le recalculer.

---

## 8.2 Deux approches : mémoïsation et tabulation

### Mémoïsation (approche descendante, *top-down*)

On garde la structure récursive naturelle, mais on stocke chaque résultat déjà calculé dans un dictionnaire.

```python
def fibonacci_memo(n, memo=None):
    if memo is None:
        memo = {}
    if n <= 1:
        return n
    if n in memo:
        return memo[n]
    resultat = fibonacci_memo(n - 1, memo) + fibonacci_memo(n - 2, memo)
    memo[n] = resultat
    return resultat
```

### Tabulation (approche ascendante, *bottom-up*)

On construit itérativement un tableau contenant la solution de chaque sous-problème, du plus petit au plus grand, sans aucune récursivité.

```python
def fibonacci_tab(n):
    if n <= 1:
        return n
    table = [0] * (n + 1)
    table[1] = 1
    for i in range(2, n + 1):
        table[i] = table[i - 1] + table[i - 2]
    return table[n]
```

Les deux approches ont un coût en **temps linéaire** (`O(n)`), contre un coût exponentiel pour la version récursive naïve — une amélioration considérable.

---

## 8.3 Le rendu de monnaie

**Problème.** Étant donné un ensemble de pièces (par exemple `1, 2, 5, 10, 20, 50` centimes) et une somme à rendre, trouver le **nombre minimal** de pièces permettant d'obtenir exactement cette somme.

### Construction de la solution par tabulation

On construit un tableau `cout[s]` donnant le nombre minimal de pièces pour rendre la somme `s`, pour `s` allant de `0` à la somme visée.

```python
def rendu_monnaie(pieces, somme):
    cout = [0] + [float("inf")] * somme   # cout[0] = 0, le reste "infini" au départ
    for s in range(1, somme + 1):
        for piece in pieces:
            if piece <= s and cout[s - piece] + 1 < cout[s]:
                cout[s] = cout[s - piece] + 1
    if cout[somme] == float("inf"):
        return None   # somme impossible à obtenir avec ces pièces
    return cout[somme]
```

**Exemple :** `rendu_monnaie([1, 2, 5, 10], 13)` renvoie `3` (par exemple `10 + 2 + 1`).

### Explication du principe

Pour rendre la somme `s`, on choisit une pièce `p` en dernier ; il reste alors `s - p` à rendre, avec un coût minimal `cout[s - p]`. On essaie toutes les pièces possibles et on garde la meilleure : `cout[s] = 1 + min(cout[s - p] pour chaque pièce p <= s)`. C'est exactement ce que fait la double boucle ci-dessus.

> **Retrouver la solution, pas seulement son coût.** Pour connaître **quelles** pièces utiliser (et pas seulement leur nombre), on peut mémoriser en plus, pour chaque somme `s`, la dernière pièce utilisée (voir exercices).

---

## 8.4 Alignement de séquences

**Problème.** Étant donné deux séquences (par exemple deux chaînes de caractères, ou deux séquences ADN représentées par des chaînes sur l'alphabet `{A, C, G, T}`), on veut mesurer leur ressemblance en calculant le nombre minimal d'opérations (insertion, suppression, substitution d'un caractère) permettant de transformer l'une en l'autre — c'est la **distance d'édition**.

```python
def distance_edition(mot1, mot2):
    n, m = len(mot1), len(mot2)
    table = [[0] * (m + 1) for _ in range(n + 1)]

    for i in range(n + 1):
        table[i][0] = i          # transformer mot1[:i] en "" : i suppressions
    for j in range(m + 1):
        table[0][j] = j          # transformer "" en mot2[:j] : j insertions

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if mot1[i - 1] == mot2[j - 1]:
                table[i][j] = table[i - 1][j - 1]        # caractères identiques, rien à faire
            else:
                table[i][j] = 1 + min(
                    table[i - 1][j],       # suppression dans mot1
                    table[i][j - 1],       # insertion dans mot1
                    table[i - 1][j - 1],   # substitution
                )
    return table[n][m]
```

**Exemple :** `distance_edition("chat", "chats")` renvoie `1` (une insertion). `distance_edition("chien", "chat")` renvoie `3` (par exemple : substituer `i` en `a`, substituer `e` en `t`, supprimer `n`).

### Pourquoi la programmation dynamique ?

Le calcul de `table[i][j]` ne dépend que de trois cases déjà calculées (`table[i-1][j]`, `table[i][j-1]`, `table[i-1][j-1]`) : en les calculant dans l'ordre (ligne par ligne, ou colonne par colonne), chaque sous-problème n'est résolu **qu'une seule fois**, alors qu'une version récursive naïve recalculerait un très grand nombre de fois les mêmes sous-séquences.

---

## 8.5 Coût en mémoire

La programmation dynamique échange souvent du **temps de calcul** contre de la **mémoire** : on accepte de stocker tous les résultats intermédiaires (le tableau `cout`, ou la table `n × m` de l'alignement) pour éviter de les recalculer.

- Pour le rendu de monnaie, le tableau `cout` occupe une mémoire proportionnelle à la somme visée : `O(somme)`.
- Pour l'alignement de séquences, la table occupe une mémoire proportionnelle à `n × m` : cela peut devenir important pour de très longues séquences (des génomes entiers, par exemple), ce qui pousse à rechercher, dans des cas avancés, des variantes économisant la mémoire (par exemple en ne conservant que les deux dernières lignes de la table, si l'on n'a besoin que du coût final et non du détail de l'alignement).

---

## 8.6 Synthèse

| Notion | Définition |
|---|---|
| Programmation dynamique | Technique qui résout un problème en mémorisant les solutions de sous-problèmes qui se recoupent |
| Mémoïsation | Approche descendante : on garde la récursivité, en stockant chaque résultat déjà calculé |
| Tabulation | Approche ascendante : on construit itérativement un tableau de solutions, des plus petits sous-problèmes vers le plus grand |
| Rendu de monnaie | Trouver le nombre minimal de pièces pour une somme donnée |
| Distance d'édition | Nombre minimal d'opérations pour transformer une séquence en une autre |

*Prochaine étape suggérée : chapitre 9, la recherche textuelle, qui aborde un autre grand problème algorithmique sur les chaînes de caractères.*
