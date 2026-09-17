# Chapitre 5 — Architecture séquentielle (von Neumann)
## Évaluation

*Première NSI — Durée : 50 min — Barème sur 20 points*

---

### Partie 1 — Questions de cours (8 points)

**Question 1 (2 pts).** Citer les quatre grands composants de l'architecture de von Neumann.

**Question 2 (2 pts).** Quelle est la caractéristique principale qui donne son nom à l'architecture de « von Neumann », par opposition à une architecture où les instructions et les données seraient stockées séparément ?

**Question 3 (2 pts).** Décrire les trois étapes du cycle fetch-decode-execute.

**Question 4 (2 pts).** Quel est le rôle de l'unité arithmétique et logique (UAL) ? Quel est le rôle de l'unité de commande ?

---

### Partie 2 — Tracer un programme (7 points)

On donne le jeu d'instructions du cours (`LOAD`, `STORE`, `ADD`, `SUB`, `JUMP`, `JUMPIFZERO`, `HALT`) et le programme suivant :
```python
programme = [
    ("LOAD", 0),
    ("SUB", 1),
    ("STORE", 2),
    ("LOAD", 2),
    ("ADD", 1),
    ("STORE", 3),
    ("HALT",),
]
memoire = {0: 20, 1: 8, 2: 0, 3: 0}
```

**Question 5 (5 pts).** Dérouler l'exécution de ce programme à la main : donner la valeur de l'accumulateur après chacune des instructions `LOAD`, `SUB`, `STORE`, `LOAD`, `ADD`, `STORE`.

**Question 6 (2 pts).** Donner les valeurs finales de `memoire[2]` et `memoire[3]`.

---

### Partie 3 — Écrire un programme machine (5 points)

**Question 7 (5 pts).** Écrire un programme (une liste d'instructions, avec le jeu d'instructions du cours) qui calcule le **triple** de `memoire[0]` et le stocke dans `memoire[1]` (sans utiliser de boucle : on pourra simplement additionner `memoire[0]` à lui-même le nombre de fois nécessaire).

---

## Corrigé et barème détaillé

### Partie 1 (8 pts)

**Q1 (2 pts)** — L'unité centrale de traitement (processeur), la mémoire principale, les bus, les périphériques d'entrée-sortie. *(0,5 pt par élément correct.)*

**Q2 (2 pts)** — Dans l'architecture de von Neumann, les **instructions du programme et les données qu'il manipule sont stockées dans la même mémoire**, sous la même forme binaire, sans distinction physique entre les deux.

**Q3 (2 pts)** — **Fetch** (chercher) : le processeur lit, en mémoire, l'instruction pointée par le compteur ordinal. **Decode** (décoder) : l'instruction est interprétée pour déterminer l'opération à effectuer. **Execute** (exécuter) : l'opération est réalisée (éventuellement via l'UAL), et le compteur ordinal est mis à jour (incrémenté, ou modifié directement en cas de saut). *(Environ 0,7 pt par étape correctement décrite.)*

**Q4 (2 pts)** — L'UAL effectue les calculs (opérations arithmétiques et logiques) (1 pt). L'unité de commande pilote le déroulement du programme : elle lit les instructions, les décode, et coordonne les autres composants pour les exécuter (1 pt).

### Partie 2 (7 pts)

**Q5 (5 pts)** — `LOAD 0` : accumulateur = `memoire[0]` = `20`. `SUB 1` : accumulateur = `20 - memoire[1]` = `20 - 8` = `12`. `STORE 2` : (l'accumulateur ne change pas, il reste `12` ; c'est `memoire[2]` qui devient `12`). `LOAD 2` : accumulateur = `memoire[2]` = `12`. `ADD 1` : accumulateur = `12 + memoire[1]` = `12 + 8` = `20`. `STORE 3` : (l'accumulateur reste `20` ; `memoire[3]` devient `20`). *(1 pt par valeur d'accumulateur correcte pour LOAD, SUB, LOAD, ADD ; 1 pt pour la bonne compréhension que STORE ne modifie pas l'accumulateur.)*

**Q6 (2 pts)** — `memoire[2]` vaut `12` (1 pt), `memoire[3]` vaut `20` (1 pt).

### Partie 3 (5 pts)

**Q7 (5 pts)**
```python
programme = [
    ("LOAD", 0),
    ("ADD", 0),
    ("ADD", 0),
    ("STORE", 1),
    ("HALT",),
]
```
*(1 pt pour le `LOAD` initial, 2 pts pour les deux `ADD` successifs (nécessaires pour obtenir 3 fois la valeur), 1 pt pour le `STORE` final, 1 pt pour le `HALT`.)* Toute solution équivalente donnant le bon résultat est acceptée (par exemple avec une boucle utilisant `JUMPIFZERO`, si l'élève choisit une approche plus générale).

---

**Barème global : 8 + 7 + 5 = 20 points.**
