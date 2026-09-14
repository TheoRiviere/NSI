# Chapitre 8 — Programmation dynamique
## TP sur machine — Du naïf au dynamique

*Terminale NSI — Python 3 — Durée indicative : 1h30 à 2h*

---

## Objectifs

- Mesurer expérimentalement le gain apporté par la mémoïsation.
- Implémenter le rendu de monnaie et l'alignement de séquences.
- Manipuler des tables de programmation dynamique à deux dimensions.

---

## Partie A — Fibonacci : mesurer le gain

**A.1.** Recopier `fibonacci` (version récursive naïve, chapitre 6), `fibonacci_memo` et `fibonacci_tab` du cours.

**A.2.** À l'aide du module `time`, comparer les temps d'exécution des trois versions pour `n = 30`. Que constatez-vous ?

**A.3.** Essayer `fibonacci_tab(500)`. Cela fonctionne-t-il avec la version naïve `fibonacci(500)` dans un temps raisonnable ? Pourquoi ?

---

## Partie B — Rendu de monnaie

**B.1.** Recopier `rendu_monnaie` du cours. Tester avec le système de pièces en euros `[1, 2, 5, 10, 20, 50, 100, 200]` (centimes) pour rendre `2,78 €` (soit 278 centimes).

**B.2.** Tester avec un système de pièces « pathologique » `[1, 3, 4]` pour rendre `6` : vérifier que l'algorithme trouve bien la solution optimale (`2` pièces : `3 + 3`), alors qu'une approche « gloutonne » (qui prendrait d'abord la plus grande pièce possible, ici `4`, puis compléterait avec `1 + 1`) donnerait `3` pièces, un résultat non optimal. Expliquer en une phrase pourquoi cette approche gloutonne échoue ici.

---

## Partie C — Alignement de séquences ADN

On représente deux courtes séquences ADN par des chaînes sur l'alphabet `{A, C, G, T}`.

**C.1.** Recopier `distance_edition` du cours.

**C.2.** Calculer la distance d'édition entre `"ACGTACGT"` et `"ACGTTCGA"`.

**C.3.** Écrire une fonction `afficher_table(table, mot1, mot2)` qui affiche la table de programmation dynamique de façon lisible, avec les lettres de `mot1` et `mot2` en en-têtes de lignes et de colonnes.

**C.4. (bonus)** Modifier `distance_edition` pour qu'elle renvoie, en plus de la distance, une des séquences d'opérations optimales (en remontant la table depuis `table[n][m]` jusqu'à `table[0][0]`).

---

## Corrigé indicatif

```python
import time

def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

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

def fibonacci_tab(n):
    if n <= 1:
        return n
    table = [0] * (n + 1)
    table[1] = 1
    for i in range(2, n + 1):
        table[i] = table[i - 1] + table[i - 2]
    return table[n]


def rendu_monnaie(pieces, somme):
    cout = [0] + [float("inf")] * somme
    for s in range(1, somme + 1):
        for piece in pieces:
            if piece <= s and cout[s - piece] + 1 < cout[s]:
                cout[s] = cout[s - piece] + 1
    if cout[somme] == float("inf"):
        return None
    return cout[somme]

print(rendu_monnaie([1, 2, 5, 10, 20, 50, 100, 200], 278))
print(rendu_monnaie([1, 3, 4], 6))   # doit valoir 2 (3 + 3), le glouton donnerait 3 (4 + 1 + 1)


def distance_edition(mot1, mot2):
    n, m = len(mot1), len(mot2)
    table = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        table[i][0] = i
    for j in range(m + 1):
        table[0][j] = j
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if mot1[i - 1] == mot2[j - 1]:
                table[i][j] = table[i - 1][j - 1]
            else:
                table[i][j] = 1 + min(table[i - 1][j], table[i][j - 1], table[i - 1][j - 1])
    return table


def afficher_table(table, mot1, mot2):
    entete = "    " + "  ".join(" " + c for c in ("" + mot2))
    print("      " + "  ".join(list(" " + mot2)))
    for i, ligne in enumerate(table):
        lettre = (" " + mot1)[i]
        print(lettre, ligne)
```

**B.2.** Une approche gloutonne choisit `4` (la plus grande pièce possible), puis doit compléter les `2` restants avec deux pièces de `1`, soit `3` pièces au total (`4 + 1 + 1`). Or la solution optimale n'utilise que `2` pièces (`3 + 3`). Le choix glouton de la plus grande pièce à chaque étape n'est donc pas toujours optimal : il ne tient pas compte des combinaisons restant possibles avec les pièces restantes, contrairement à la programmation dynamique, qui explore systématiquement toutes les décompositions et garantit toujours la solution optimale.
