# Chapitre 5 — Graphes
## Évaluation

*Terminale NSI — Durée : 55 min — Barème sur 20 points*

---

### Partie 1 — Questions de cours (7 points)

**Question 1 (2 pts).** Quelle est la différence entre une arête et un arc ?

**Question 2 (3 pts).** On considère un graphe à `n` sommets. Donner, en fonction de `n`, la taille (nombre de cases) de sa matrice d'adjacence. Expliquer en une phrase pourquoi une représentation par listes de successeurs est préférable pour un graphe qui a très peu d'arêtes par rapport au nombre maximal possible.

**Question 3 (2 pts).** Quel algorithme de parcours garantit de trouver le plus court chemin (en nombre d'arêtes) entre deux sommets, dans un graphe non pondéré ? Pourquoi cette garantie n'existe-t-elle pas pour l'autre type de parcours vu en cours ?

---

### Partie 2 — Lecture de graphe (6 points)

On donne le graphe non orienté suivant sous forme de listes de successeurs :

```python
graphe = {
    "S1": ["S2", "S3"],
    "S2": ["S1", "S4"],
    "S3": ["S1", "S4"],
    "S4": ["S2", "S3", "S5"],
    "S5": ["S4"],
}
```

**Question 4 (2 pts).** Donner la matrice d'adjacence de ce graphe, en numérotant les sommets `S1(0), S2(1), S3(2), S4(3), S5(4)`.

**Question 5 (2 pts).** Ce graphe contient-il un cycle ? Si oui, en donner un.

**Question 6 (2 pts).** Donner le résultat de `parcours_largeur(graphe, "S1")` (fonction du cours).

---

### Partie 3 — Écrire des fonctions (7 points)

**Question 7 (3 pts).** Écrire une fonction `voisins_communs(graphe, s1, s2)` qui renvoie la liste des sommets qui sont à la fois voisins de `s1` et de `s2`.

**Question 8 (4 pts).** Écrire une fonction `est_complet(graphe)` qui renvoie `True` si le graphe non orienté est **complet**, c'est-à-dire si chaque sommet est relié directement à tous les autres sommets du graphe.

---

## Corrigé et barème détaillé

### Partie 1 (7 pts)

**Q1 (2 pts)** — Une arête relie deux sommets **sans orientation** (dans un graphe non orienté) ; un arc relie deux sommets **avec un sens** précis, d'un sommet de départ vers un sommet d'arrivée (dans un graphe orienté).

**Q2 (3 pts)** — La matrice a `n × n = n²` cases (2 pts). Si le graphe a peu d'arêtes, la matrice contient une grande majorité de zéros et gaspille de la mémoire, alors que les listes de successeurs n'occupent qu'un espace proportionnel au nombre réel d'arêtes (1 pt).

**Q3 (2 pts)** — Le parcours en **largeur** (BFS), car il visite les sommets par ordre croissant de distance (en nombre d'arêtes) depuis le sommet de départ, si bien que le premier chemin trouvé jusqu'à un sommet est nécessairement le plus court. Le parcours en profondeur (DFS) peut s'enfoncer arbitrairement loin dans une branche avant d'en explorer une autre plus courte, donc il ne garantit pas cette propriété.

### Partie 2 (6 pts)

**Q4 (2 pts)**
```python
matrice = [
    [0, 1, 1, 0, 0],  # S1
    [1, 0, 0, 1, 0],  # S2
    [1, 0, 0, 1, 0],  # S3
    [0, 1, 1, 0, 1],  # S4
    [0, 0, 0, 1, 0],  # S5
]
```

**Q5 (2 pts)** — Oui : par exemple `S1 → S2 → S4 → S3 → S1`.

**Q6 (2 pts)** — `["S1", "S2", "S3", "S4", "S5"]`.

### Partie 3 (7 pts)

**Q7 (3 pts)**
```python
def voisins_communs(graphe, s1, s2):
    return [s for s in graphe[s1] if s in graphe[s2]]
```
*(1 pt parcours des voisins de s1 ; 1 pt test d'appartenance aux voisins de s2 ; 1 pt construction correcte de la liste.)*

**Q8 (4 pts)**
```python
def est_complet(graphe):
    sommets = list(graphe.keys())
    for sommet in sommets:
        for autre in sommets:
            if autre != sommet and autre not in graphe[sommet]:
                return False
    return True
```
*(1 pt parcours de tous les couples de sommets ; 1 pt exclusion correcte du sommet lui-même ; 1 pt test d'appartenance correct ; 1 pt valeurs de retour correctes.)*

---

**Barème global : 7 + 6 + 7 = 20 points.**
