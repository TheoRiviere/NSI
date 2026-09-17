# Chapitre 5 — Architecture séquentielle (von Neumann)
## Fiche d'exercices

*Première NSI — Python 3*

---

### Exercice 1 — Questions de compréhension

1. Dans l'architecture de von Neumann, où sont stockées les instructions d'un programme ? Et les données qu'il manipule ?
2. Quel est le rôle du compteur ordinal (*program counter*) ?
3. À quelle étape du cycle fetch-decode-execute le compteur ordinal est-il normalement modifié ? Que se passe-t-il de particulier lors de l'exécution d'une instruction de saut (`JUMP`) ?

### Exercice 2 — Tracer un programme à la main

On donne le programme suivant (avec le jeu d'instructions du cours) et la mémoire initiale `memoire = {0: 10, 1: 4, 2: 0}` :
```python
programme = [
    ("LOAD", 0),
    ("SUB", 1),
    ("STORE", 2),
    ("HALT",),
]
```

1. Dérouler à la main l'exécution de ce programme : donner la valeur de l'accumulateur après chaque instruction.
2. Quelle est la valeur finale de `memoire[2]` ? Vérifier avec `executer_programme` du cours.

### Exercice 3 — Écrire un programme machine : doubler une valeur

1. Écrire un programme (une liste d'instructions) qui calcule le double de `memoire[0]` et le stocke dans `memoire[1]`, sans utiliser deux fois la valeur `2` comme une constante en mémoire (indication : on peut additionner `memoire[0]` à lui-même).
2. Vérifier que pour `memoire = {0: 9, 1: 0}`, le programme donne bien `memoire[1] == 18`.

### Exercice 4 — Une boucle : multiplication par additions répétées

On souhaite calculer `memoire[0] × memoire[1]` en n'utilisant que des additions (pas de multiplication directe, qui n'existe pas dans notre jeu d'instructions), en additionnant `memoire[0]` un nombre de fois égal à `memoire[1]`.

On dispose de la mémoire initiale suivante :
```python
memoire = {0: 4, 1: 3, 2: 0, 3: 1}
# memoire[0] = a (la valeur à multiplier)
# memoire[1] = n (le nombre de répétitions, qui sera décompté jusqu'à 0)
# memoire[2] = somme (le résultat, initialisé à 0)
# memoire[3] = la constante 1 (utile pour décrémenter n avec SUB)
```

1. En vous inspirant de l'exemple de boucle du cours (qui décompte `memoire[0]` jusqu'à 0), écrire un programme qui, à chaque tour de boucle, ajoute `memoire[0]` (la valeur `a`) à `memoire[2]` (la somme), et décrémente `memoire[1]` (le compteur `n`), jusqu'à ce que `n` atteigne 0.
2. Vérifier que le résultat final dans `memoire[2]` est bien `4 × 3 = 12`.
3. Combien de tours de boucle ce programme effectue-t-il pour cet exemple ? Qu'en serait-il si `memoire[1]` valait `0` dès le départ ?

---

## Corrigés

### Exercice 1

1. Les instructions et les données sont stockées dans la **même mémoire** (principe fondamental de l'architecture de von Neumann), sous la même forme (des suites de bits) ; c'est le contexte d'utilisation (interprété comme instruction ou comme donnée) qui détermine comment une case mémoire est utilisée.
2. Le compteur ordinal contient l'**adresse de la prochaine instruction à exécuter** : c'est lui qui indique au processeur où chercher, en mémoire, l'instruction suivante.
3. Le compteur ordinal est normalement **incrémenté** à l'étape « execute » (après l'exécution de l'instruction courante, pour passer à la suivante). Lors d'un saut (`JUMP`), le compteur ordinal n'est **pas simplement incrémenté** : il est directement remplacé par l'adresse cible du saut, ce qui permet au flux d'exécution de « bondir » ailleurs dans le programme (et donc de réaliser des boucles ou des branchements).

### Exercice 2

1. `LOAD 0` : accumulateur ← `memoire[0]` = `10`. `SUB 1` : accumulateur ← `10 - memoire[1]` = `10 - 4` = `6`. `STORE 2` : `memoire[2]` ← `6`.
2. `memoire[2]` vaut finalement `6`.

### Exercice 3

1-2.
```python
programme = [
    ("LOAD", 0),
    ("ADD", 0),      # accumulateur = memoire[0] + memoire[0] = 2 * memoire[0]
    ("STORE", 1),
    ("HALT",),
]
memoire = {0: 9, 1: 0}
# memoire[1] vaut ensuite 18
```

### Exercice 4

1-2.
```python
programme = [
    ("LOAD", 1),          # 0: charge n
    ("JUMPIFZERO", 8),    # 1: si n == 0, fin
    ("SUB", 3),           # 2: n = n - 1
    ("STORE", 1),         # 3: sauvegarde n
    ("LOAD", 2),          # 4: charge la somme
    ("ADD", 0),           # 5: somme = somme + a
    ("STORE", 2),         # 6: sauvegarde la somme
    ("JUMP", 0),          # 7: retourne au début de la boucle
    ("HALT",),            # 8: fin
]
memoire = {0: 4, 1: 3, 2: 0, 3: 1}
# memoire[2] vaut ensuite 12 (= 4 * 3)
```
3. Le programme effectue **3 tours de boucle** (un par unité de `memoire[1]`, qui vaut initialement 3). Si `memoire[1]` valait `0` dès le départ, l'instruction `JUMPIFZERO` à l'adresse 1 sauterait **immédiatement** vers la fin (adresse 8) dès le premier passage : aucun tour de boucle ne serait effectué, et la somme resterait à sa valeur initiale (`0`), ce qui est le comportement attendu (« multiplier par 0 »).
