# Terminale NSI — Chapitre 6
# Récursivité

*Support de cours — Python 3*

---

## Objectifs du chapitre

- Écrire une fonction récursive correcte (cas de base, cas récursif).
- Analyser le fonctionnement d'un programme récursif à l'aide de la pile d'appels.
- Justifier la terminaison d'une fonction récursive.
- Comparer une version récursive et une version itérative d'un même algorithme.

**Prérequis :** notions de base de la récursivité (première NSI), fonctions.

---

## 6.1 Principe

Une fonction est **récursive** lorsqu'elle s'appelle elle-même, directement ou indirectement, pour résoudre un problème en le ramenant à un ou plusieurs problèmes **plus petits** de même nature.

Toute fonction récursive correcte doit comporter :

1. un ou plusieurs **cas de base** (ou *cas d'arrêt*), qui se résolvent directement, sans appel récursif ;
2. un ou plusieurs **cas récursifs**, qui ramènent le problème à une instance **strictement plus petite** du même problème.

### Exemple : la factorielle

```python
def factorielle(n):
    if n == 0:           # cas de base
        return 1
    else:                 # cas récursif
        return n * factorielle(n - 1)
```

`factorielle(4)` se déroule ainsi :

```
factorielle(4) = 4 * factorielle(3)
                    = 4 * (3 * factorielle(2))
                    = 4 * (3 * (2 * factorielle(1)))
                    = 4 * (3 * (2 * (1 * factorielle(0))))
                    = 4 * (3 * (2 * (1 * 1)))
                    = 24
```

---

## 6.2 La pile d'appels

Chaque appel de fonction (récursif ou non) est empilé dans la **pile d'appels** de l'interpréteur Python, avec ses variables locales. Quand la fonction se termine, son appel est dépilé et le résultat est transmis à l'appel précédent.

```python
def compte_a_rebours(n):
    if n == 0:
        print("Décollage !")
    else:
        print(n)
        compte_a_rebours(n - 1)
        print(f"(retour à l'appel {n})")

compte_a_rebours(3)
```

Affiche :
```
3
2
1
Décollage !
(retour à l'appel 1)
(retour à l'appel 2)
(retour à l'appel 3)
```

Ceci montre bien deux phases : la **descente** (les appels s'empilent jusqu'au cas de base) puis la **remontée** (chaque appel se termine, dans l'ordre inverse de son démarrage — comportement LIFO, comme une pile, chapitre 2).

> **Limite pratique.** La pile d'appels a une taille limitée. Un appel récursif qui ne termine jamais (ou une récursion trop profonde) lève une `RecursionError: maximum recursion depth exceeded`.

```python
def boucle_infinie(n):
    return boucle_infinie(n + 1)   # pas de cas de base : erreur garantie
```

---

## 6.3 Exemples classiques

### Recherche dichotomique récursive

```python
def recherche_dichotomique(tableau_trie, cible, gauche, droite):
    if gauche > droite:
        return False   # cas de base : intervalle vide, cible absente
    milieu = (gauche + droite) // 2
    if tableau_trie[milieu] == cible:
        return True     # cas de base : cible trouvée
    elif tableau_trie[milieu] < cible:
        return recherche_dichotomique(tableau_trie, cible, milieu + 1, droite)
    else:
        return recherche_dichotomique(tableau_trie, cible, gauche, milieu - 1)
```

### Palindrome

```python
def est_palindrome(mot):
    if len(mot) <= 1:
        return True                     # cas de base
    if mot[0] != mot[-1]:
        return False                    # cas de base
    return est_palindrome(mot[1:-1])    # cas récursif
```

### Suite de Fibonacci (et son piège)

```python
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
```

Cette version, bien que correcte, recalcule de nombreuses fois les mêmes valeurs (par exemple `fibonacci(2)` est recalculé plusieurs fois pour `fibonacci(5)`), ce qui la rend très coûteuse pour `n` grand : son coût croît **exponentiellement** avec `n`. *(Ce problème sera résolu au chapitre sur la programmation dynamique, qui propose une solution en coût linéaire.)*

---

## 6.4 Terminaison d'une fonction récursive

Pour être sûr qu'une fonction récursive termine, il faut identifier une quantité — appelée **variant** — qui :

1. est un entier naturel (ou peut se ramener à un tel entier) ;
2. **diminue strictement** à chaque appel récursif ;
3. atteint une valeur pour laquelle on est dans un **cas de base**.

Dans `factorielle(n)`, le variant est `n` : il diminue de 1 à chaque appel et atteint 0, qui est le cas de base. Dans `recherche_dichotomique`, le variant est `droite - gauche` : il diminue strictement à chaque appel (l'intervalle de recherche se réduit de moitié), et l'intervalle finit par devenir vide (`gauche > droite`).

> **Attention.** Un appel comme `factorielle(-1)` ne termine jamais : `n` ne fait alors que décroître sans jamais atteindre `0`. Une fonction récursive doit être appelée dans le domaine pour lequel son variant est valide.

---

## 6.5 Récursivité et itération

Toute fonction récursive peut se réécrire avec une boucle (et réciproquement), mais les deux versions n'ont pas toujours le même coût en mémoire.

```python
# Version récursive
def somme_recursive(n):
    if n == 0:
        return 0
    return n + somme_recursive(n - 1)

# Version itérative
def somme_iterative(n):
    total = 0
    for i in range(1, n + 1):
        total = total + i
    return total
```

Les deux fonctions calculent la même chose, mais `somme_recursive` empile `n` appels sur la pile d'appels (occupant une mémoire proportionnelle à `n`), alors que `somme_iterative` n'utilise qu'une seule variable `total`, quelle que soit la taille de `n`.

> **Pourquoi utiliser la récursivité malgré ce coût ?** Certains problèmes — en particulier ceux qui portent sur des structures elles-mêmes récursives, comme les arbres (chapitre 4) ou les graphes (chapitre 5) — s'expriment beaucoup plus naturellement et plus simplement avec des fonctions récursives qu'avec des boucles.

---

## 6.6 Synthèse

| Notion | Définition |
|---|---|
| Fonction récursive | Fonction qui s'appelle elle-même pour résoudre une instance plus petite du même problème |
| Cas de base | Cas résolu directement, sans appel récursif |
| Cas récursif | Cas ramené à une instance plus petite via un appel récursif |
| Pile d'appels | Structure LIFO qui mémorise les appels de fonctions en cours et leurs variables locales |
| Variant | Quantité entière qui décroît strictement à chaque appel récursif, garantissant la terminaison |

*Prochaine étape suggérée : chapitre 7, la méthode « diviser pour régner », qui structure et généralise l'usage de la récursivité pour concevoir des algorithmes efficaces.*
