# Chapitre 6 — Récursivité
## TP sur machine — Explorer, tracer, comparer

*Terminale NSI — Python 3 — Durée indicative : 1h30*

---

## Objectifs

- Écrire plusieurs fonctions récursives sur des types de données variés.
- Observer concrètement la pile d'appels et ses limites.
- Comparer expérimentalement le coût d'une version récursive et d'une version itérative.

---

## Partie A — Récursivité sur les nombres et les chaînes

**A.1.** Écrire une fonction récursive `est_croissante(tableau)` qui renvoie `True` si les éléments d'un tableau (liste Python) sont rangés par ordre croissant, `False` sinon.

*Indication :* le cas de base peut être un tableau de longueur 0 ou 1 ; le cas récursif compare les deux premiers éléments puis se ramène au reste du tableau.

**A.2.** Écrire une fonction récursive `compte_occurrences(chaine, caractere)` qui compte le nombre d'occurrences d'un caractère dans une chaîne.

**A.3.** Écrire une fonction récursive `est_trie_partiellement` *(bonus)* qui vérifie qu'un tableau est trié en ignorant la casse pour des chaînes de caractères.

---

## Partie B — Observer la pile d'appels

**B.1.** Ajouter des `print` de trace à la fonction `factorielle` du cours, pour afficher, à chaque appel, sa profondeur (nombre d'appels imbriqués) et la valeur de `n` :

```python
def factorielle_tracee(n, profondeur=0):
    print("  " * profondeur + f"appel factorielle_tracee({n})")
    if n == 0:
        print("  " * profondeur + "-> renvoie 1")
        return 1
    resultat = n * factorielle_tracee(n - 1, profondeur + 1)
    print("  " * profondeur + f"-> renvoie {resultat}")
    return resultat
```

Exécuter `factorielle_tracee(5)` et observer l'affichage : identifier la phase de descente et la phase de remontée.

**B.2.** Chercher la profondeur de récursion maximale autorisée par défaut avec `sys.getrecursionlimit()`. Écrire une fonction qui provoque volontairement une `RecursionError`, et capturer cette erreur avec un `try`/`except` pour afficher un message clair plutôt que de laisser planter le programme.

---

## Partie C — Comparer récursif et itératif

**C.1.** Écrire une version itérative `fibonacci_iteratif(n)` de la suite de Fibonacci, en coût linéaire (une seule boucle, sans recalculs redondants).

**C.2.** À l'aide du module `time`, comparer les temps d'exécution de `fibonacci` (récursif naïf, vu en cours) et `fibonacci_iteratif` pour `n = 28`. Que constatez-vous ?

**C.3.** Expliquer, en une phrase, pourquoi la différence est si importante entre les deux versions, en reliant votre réponse au nombre d'appels effectués par la version récursive naïve.

---

## Corrigé indicatif

```python
def est_croissante(tableau):
    if len(tableau) <= 1:
        return True
    if tableau[0] > tableau[1]:
        return False
    return est_croissante(tableau[1:])


def compte_occurrences(chaine, caractere):
    if chaine == "":
        return 0
    premier = 1 if chaine[0] == caractere else 0
    return premier + compte_occurrences(chaine[1:], caractere)


def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


def fibonacci_iteratif(n):
    if n <= 1:
        return n
    precedent, courant = 0, 1
    for _ in range(n - 1):
        precedent, courant = courant, precedent + courant
    return courant


import time

debut = time.perf_counter()
resultat_recursif = fibonacci(28)
duree_recursive = time.perf_counter() - debut

debut = time.perf_counter()
resultat_iteratif = fibonacci_iteratif(28)
duree_iterative = time.perf_counter() - debut

print("Récursif :", resultat_recursif, "en", duree_recursive, "s")
print("Itératif :", resultat_iteratif, "en", duree_iterative, "s")
```

**C.3.** La version récursive naïve de `fibonacci` recalcule de très nombreuses fois les mêmes sous-résultats (par exemple `fibonacci(10)` est recalculé séparément à chaque branche de l'arbre d'appels) : le nombre total d'appels croît **exponentiellement** avec `n`. La version itérative ne calcule chaque terme qu'une seule fois, d'où un coût linéaire, bien plus rapide en pratique pour `n` grand.
