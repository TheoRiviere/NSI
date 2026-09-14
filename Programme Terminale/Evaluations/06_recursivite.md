# Chapitre 6 — Récursivité
## Évaluation

*Terminale NSI — Durée : 50 min — Barème sur 20 points*

---

### Partie 1 — Questions de cours (6 points)

**Question 1 (2 pts).** Qu'est-ce qu'un cas de base dans une fonction récursive ? Pourquoi est-il indispensable ?

**Question 2 (2 pts).** Qu'appelle-t-on la pile d'appels ? Que se passe-t-il si une fonction récursive ne termine jamais ?

**Question 3 (2 pts).** Qu'est-ce qu'un variant, et à quoi sert-il ?

---

### Partie 2 — Lecture et trace (6 points)

On donne :
```python
def mystere(n):
    if n <= 1:
        return 1
    return n * mystere(n - 2)
```

**Question 4 (2 pts).** Que renvoie `mystere(6)` ? Détailler le calcul.

**Question 5 (2 pts).** Que renvoie `mystere(7)` ?

**Question 6 (2 pts).** Cette fonction termine-t-elle pour tout entier `n >= 0` ? Justifier en donnant un variant.

---

### Partie 3 — Écrire des fonctions récursives (8 points)

**Question 7 (4 pts).** Écrire une fonction récursive `multiplication(a, b)` qui calcule le produit de deux entiers naturels `a` et `b` **sans utiliser l'opérateur `*`**, uniquement à l'aide d'additions (indication : `a * b = a + a * (b - 1)`, avec `a * 0 = 0`).

**Question 8 (4 pts).** Écrire une fonction récursive `nombre_de_voyelles(mot)` qui compte le nombre de voyelles (`a, e, i, o, u, y`, minuscules) dans une chaîne de caractères.

---

## Corrigé et barème détaillé

### Partie 1 (6 pts)

**Q1 (2 pts)** — Le cas de base est le cas résolu directement, sans appel récursif (1 pt). Il est indispensable car c'est lui qui arrête la chaîne d'appels récursifs : sans lui, la fonction s'appellerait indéfiniment (1 pt).

**Q2 (2 pts)** — La pile d'appels est la structure qui mémorise, dans l'ordre, tous les appels de fonctions en cours d'exécution (avec leurs variables locales) (1 pt). Si une fonction récursive ne termine jamais, les appels s'empilent indéfiniment jusqu'à dépasser la profondeur de récursion maximale autorisée, ce qui déclenche une erreur `RecursionError` (1 pt).

**Q3 (2 pts)** — Un variant est une quantité entière qui décroît strictement à chaque appel récursif et qui, en atteignant une certaine valeur, correspond à un cas de base (1 pt). Il sert à prouver que la fonction récursive termine bien (1 pt).

### Partie 2 (6 pts)

**Q4 (2 pts)** — `mystere(6) = 6 * mystere(4) = 6 * (4 * mystere(2)) = 6 * (4 * (2 * mystere(0))) = 6 * 4 * 2 * 1 = 48`.

**Q5 (2 pts)** — `mystere(7) = 7 * mystere(5) = 7 * 5 * mystere(3) = 7 * 5 * 3 * mystere(1) = 7 * 5 * 3 * 1 = 105`.

**Q6 (2 pts)** — Oui : le variant `n` diminue de 2 à chaque appel récursif, et atteint une valeur `<= 1` (0 ou 1 selon la parité de `n`), qui correspond au cas de base.

### Partie 3 (8 pts)

**Q7 (4 pts)**
```python
def multiplication(a, b):
    if b == 0:
        return 0
    return a + multiplication(a, b - 1)
```
*(1 pt cas de base ; 2 pts cas récursif correct ; 1 pt fonction correcte sur des exemples simples.)*

**Q8 (4 pts)**
```python
def nombre_de_voyelles(mot):
    if mot == "":
        return 0
    voyelles = "aeiouy"
    premier = 1 if mot[0] in voyelles else 0
    return premier + nombre_de_voyelles(mot[1:])
```
*(1 pt cas de base ; 1 pt test d'appartenance correct ; 2 pts cas récursif et accumulation correcte.)*

---

**Barème global : 6 + 6 + 8 = 20 points.**
