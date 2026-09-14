# Chapitre 6 — Récursivité
## Fiche d'exercices

*Terminale NSI — Python 3*

---

### Exercice 1 — Identifier cas de base et cas récursif

Pour chacune des fonctions du cours (`factorielle`, `recherche_dichotomique`, `est_palindrome`, `fibonacci`), identifier précisément le(s) cas de base et le(s) cas récursif.

### Exercice 2 — Puissance récursive

Écrire une fonction récursive `puissance(base, exposant)` qui calcule `base ** exposant` (avec `exposant` un entier naturel), sans utiliser l'opérateur `**`.

### Exercice 3 — Somme des chiffres

Écrire une fonction récursive `somme_chiffres(n)` qui renvoie la somme des chiffres d'un entier naturel `n` (par exemple `somme_chiffres(1234)` doit renvoyer `10`).

*Indication :* le dernier chiffre de `n` est `n % 10`, et le reste est `n // 10`.

### Exercice 4 — Inverser une chaîne

Écrire une fonction récursive `inverser(chaine)` qui renvoie la chaîne inversée, sans utiliser `chaine[::-1]` ni aucune boucle.

### Exercice 5 — PGCD (algorithme d'Euclide)

Écrire une fonction récursive `pgcd(a, b)` qui calcule le plus grand commun diviseur de deux entiers naturels, en utilisant la propriété : `pgcd(a, b) = pgcd(b, a % b)`, avec `pgcd(a, 0) = a`.

### Exercice 6 — Trace d'exécution

On donne :
```python
def mystere(n):
    if n == 0:
        return ""
    return mystere(n - 1) + str(n)
```
1. Sans exécuter le code, donner la valeur de `mystere(4)`.
2. Combien d'appels récursifs sont effectués au total pour calculer `mystere(4)` (cas de base inclus) ?

### Exercice 7 — Terminaison

Pour chacune des fonctions suivantes, dire si elle termine toujours, et si oui, donner un variant qui le justifie ; sinon, expliquer pourquoi elle ne termine pas.

```python
def a(n):
    if n <= 0:
        return 0
    return 1 + a(n - 1)

def b(n):
    if n == 0:
        return 0
    return 1 + b(n + 1)

def c(n):
    if n <= 1:
        return n
    return c(n // 2) + 1
```

### Exercice 8 — Récursivité vs itération

1. Écrire une version **itérative** de `puissance` (exercice 2), avec une boucle `for`.
2. Pour `puissance(2, 100000)`, laquelle des deux versions (récursive ou itérative) risque de provoquer une erreur en Python ? Pourquoi ?

---

## Corrigés

### Exercice 1

- `factorielle` : cas de base `n == 0` (renvoie 1) ; cas récursif `n * factorielle(n-1)`.
- `recherche_dichotomique` : cas de base `gauche > droite` (False) et `tableau_trie[milieu] == cible` (True) ; cas récursif : appel sur la moitié gauche ou droite.
- `est_palindrome` : cas de base `len(mot) <= 1` (True) et `mot[0] != mot[-1]` (False) ; cas récursif : appel sur `mot[1:-1]`.
- `fibonacci` : cas de base `n <= 1` (renvoie `n`) ; cas récursif : somme de deux appels sur `n-1` et `n-2`.

### Exercice 2

```python
def puissance(base, exposant):
    if exposant == 0:
        return 1
    return base * puissance(base, exposant - 1)
```

### Exercice 3

```python
def somme_chiffres(n):
    if n < 10:
        return n
    return n % 10 + somme_chiffres(n // 10)
```

### Exercice 4

```python
def inverser(chaine):
    if len(chaine) <= 1:
        return chaine
    return inverser(chaine[1:]) + chaine[0]
```

### Exercice 5

```python
def pgcd(a, b):
    if b == 0:
        return a
    return pgcd(b, a % b)
```

### Exercice 6

1. `mystere(4)` renvoie `"1234"`.
2. 5 appels au total : `mystere(4)`, `mystere(3)`, `mystere(2)`, `mystere(1)`, `mystere(0)`.

### Exercice 7

- `a(n)` : **termine toujours**, quel que soit l'entier `n` de départ. Si `n <= 0`, c'est immédiatement le cas de base. Si `n > 0`, le variant `n` décroît strictement de 1 à chaque appel et finit donc par atteindre une valeur `<= 0`.
- `b(n)` : **termine si `n <= 0`**, mais **ne termine jamais si `n > 0`**. Pour `n == 0`, c'est le cas de base. Pour `n < 0`, l'appel se fait sur `n + 1`, qui se rapproche de 0 et finit par l'atteindre (variant : `-n`, qui décroît strictement). Pour `n > 0` en revanche, `n + 1` s'éloigne indéfiniment de 0 sans jamais l'atteindre : la récursion ne s'arrête jamais.
- `c(n)` : **termine toujours**, quel que soit l'entier `n`. Si `n <= 1`, c'est immédiatement le cas de base (vrai en particulier pour tout `n` négatif). Si `n > 1`, le variant `n` est divisé par 2 à chaque appel (division entière), donc décroît strictement, et finit par atteindre une valeur `<= 1`.

### Exercice 8

```python
def puissance_iterative(base, exposant):
    resultat = 1
    for _ in range(exposant):
        resultat = resultat * base
    return resultat
```

2. La version **récursive** risque de provoquer une `RecursionError` : elle empile 100 000 appels sur la pile d'appels, ce qui dépasse la profondeur de récursion maximale autorisée par défaut en Python (généralement de l'ordre de 1000). La version itérative, elle, n'utilise qu'une seule variable `resultat` réutilisée à chaque tour de boucle et ne pose donc pas ce problème.
