# Chapitre 10 — Tris par insertion et par sélection
## TP sur machine — Trier des objets et mesurer le temps d'exécution

*Première NSI — Python 3 — Durée indicative : 1h30 à 2h*

---

## Objectifs

- Adapter un algorithme de tri pour trier selon une clé (pas seulement des nombres bruts).
- Mesurer expérimentalement le temps d'exécution et observer la croissance quadratique.

---

## Partie A — Trier des dictionnaires selon une clé

On dispose d'une liste de dictionnaires représentant des élèves :
```python
eleves = [
    {"nom": "Alice", "moyenne": 14.5},
    {"nom": "Bob", "moyenne": 9.2},
    {"nom": "Chloé", "moyenne": 17.0},
    {"nom": "David", "moyenne": 11.8},
]
```

**A.1.** Écrire une fonction `tri_insertion_par_cle(tableau, cle)`, qui reprend le principe du tri par insertion du cours, mais où la comparaison entre deux éléments `a` et `b` se fait non pas directement (`a > b`), mais en comparant `cle(a)` et `cle(b)`, où `cle` est une **fonction** passée en paramètre (indication : c'est le même principe que le paramètre `key` de la fonction native `sorted`).

**A.2.** Utiliser cette fonction pour trier la liste `eleves` par moyenne croissante, avec `cle = lambda e: e["moyenne"]`.

**A.3.** Vérifier que le résultat obtenu commence bien par Bob (la moyenne la plus faible) et se termine par Chloé (la moyenne la plus élevée).

**A.4.** Adapter de même `tri_selection` du cours en une fonction `tri_selection_par_cle(tableau, cle)`, et vérifier qu'elle donne le même résultat sur `eleves`.

---

## Partie B — Mesurer le temps d'exécution

**B.1.** Écrire une fonction `mesurer_temps(fonction_tri, taille)` qui génère un tableau aléatoire de la taille donnée (valeurs entre 0 et 10 000, avec `random.randint`), mesure le temps d'exécution de `fonction_tri` sur ce tableau (à l'aide du module `time`, avec `time.perf_counter()` avant et après l'appel), et renvoie la durée écoulée.

**B.2.** Mesurer le temps d'exécution de `tri_selection` pour des tailles de `200`, `400`, `800`, puis `1600`. Afficher les résultats dans un tableau.

**B.3.** Que constatez-vous sur le temps d'exécution lorsque la taille double à chaque fois ? Ce constat est-il cohérent avec le coût quadratique annoncé par le cours (si le coût est en `n²`, doubler `n` devrait environ **quadrupler** le temps d'exécution) ?

**B.4. (bonus)** Refaire la même mesure pour `tri_insertion`, en testant à la fois sur un tableau **aléatoire** et sur un tableau **déjà trié** de même taille. Le tri par insertion se comporte-t-il différemment selon le cas ? Est-ce cohérent avec ce qui a été vu dans le cours sur son meilleur cas ?

---

## Corrigé indicatif

```python
import random
import time

# --- Partie A ---
def tri_insertion_par_cle(tableau, cle):
    t = tableau[:]
    n = len(t)
    for i in range(1, n):
        valeur = t[i]
        j = i - 1
        while j >= 0 and cle(t[j]) > cle(valeur):
            t[j + 1] = t[j]
            j -= 1
        t[j + 1] = valeur
    return t

def tri_selection_par_cle(tableau, cle):
    t = tableau[:]
    n = len(t)
    for i in range(n - 1):
        indice_min = i
        for j in range(i + 1, n):
            if cle(t[j]) < cle(t[indice_min]):
                indice_min = j
        t[i], t[indice_min] = t[indice_min], t[i]
    return t

eleves = [
    {"nom": "Alice", "moyenne": 14.5},
    {"nom": "Bob", "moyenne": 9.2},
    {"nom": "Chloé", "moyenne": 17.0},
    {"nom": "David", "moyenne": 11.8},
]

eleves_tries = tri_insertion_par_cle(eleves, lambda e: e["moyenne"])
print([e["nom"] for e in eleves_tries])
# ['Bob', 'David', 'Alice', 'Chloé']

eleves_tries_2 = tri_selection_par_cle(eleves, lambda e: e["moyenne"])
print([e["nom"] for e in eleves_tries_2])
# ['Bob', 'David', 'Alice', 'Chloé']  (même résultat)


# --- Partie B ---
def tri_selection(tableau):
    t = tableau[:]
    n = len(t)
    for i in range(n - 1):
        indice_min = i
        for j in range(i + 1, n):
            if t[j] < t[indice_min]:
                indice_min = j
        t[i], t[indice_min] = t[indice_min], t[i]
    return t

def tri_insertion(tableau):
    t = tableau[:]
    n = len(t)
    for i in range(1, n):
        valeur = t[i]
        j = i - 1
        while j >= 0 and t[j] > valeur:
            t[j + 1] = t[j]
            j -= 1
        t[j + 1] = valeur
    return t

def mesurer_temps(fonction_tri, taille):
    tableau = [random.randint(0, 10000) for _ in range(taille)]
    debut = time.perf_counter()
    fonction_tri(tableau)
    fin = time.perf_counter()
    return fin - debut

print(f"{'Taille':>8} | {'Temps (s)':>12}")
for taille in [200, 400, 800, 1600]:
    duree = mesurer_temps(tri_selection, taille)
    print(f"{taille:>8} | {duree:>12.5f}")

# --- Partie B.4 (bonus) ---
for taille in [800, 1600]:
    tableau_aleatoire = [random.randint(0, 10000) for _ in range(taille)]
    tableau_trie = sorted(tableau_aleatoire)

    debut = time.perf_counter()
    tri_insertion(tableau_aleatoire)
    duree_aleatoire = time.perf_counter() - debut

    debut = time.perf_counter()
    tri_insertion(tableau_trie)
    duree_triee = time.perf_counter() - debut

    print(f"Taille {taille} — aléatoire : {duree_aleatoire:.5f} s | déjà trié : {duree_triee:.5f} s")
```

**Réponse B.3 :** on observe qu'à chaque doublement de la taille, le temps d'exécution est approximativement **multiplié par 4**, ce qui est bien cohérent avec un coût quadratique (`n²`) : `(2n)² = 4 × n²`.

**Réponse B.4 :** le tri par insertion est **nettement plus rapide** sur un tableau déjà trié que sur un tableau aléatoire de même taille, car dans ce cas chaque élément à insérer est immédiatement à sa place (aucun décalage nécessaire), ce qui correspond au **meilleur cas** décrit dans le cours (coût linéaire, en `n-1`, au lieu du coût quadratique du pire des cas). Le tri par sélection, en revanche, ne présenterait pas une telle différence, puisqu'il effectue toujours le même nombre de comparaisons, quel que soit l'état initial du tableau.
