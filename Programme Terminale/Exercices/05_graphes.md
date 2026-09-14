# Chapitre 5 — Graphes
## Fiche d'exercices

*Terminale NSI — Python 3*

---

### Exercice 1 — Vocabulaire

On considère le réseau social suivant, où une flèche `X -> Y` signifie « X suit Y » :

```
Alice -> Bob
Bob -> Claire
Claire -> Alice
Claire -> David
```

1. Ce graphe est-il orienté ou non orienté ? Justifier.
2. Donner la liste des sommets et la liste des arcs.
3. Quels sont les successeurs de `Claire` ?
4. Ce graphe contient-il un cycle ? Si oui, lequel ?

### Exercice 2 — Représentations

Pour le graphe de l'exercice 1 :

1. Donner sa représentation sous forme de dictionnaire de listes de successeurs.
2. Donner sa matrice d'adjacence, en numérotant les sommets dans l'ordre `Alice(0), Bob(1), Claire(2), David(3)`.

### Exercice 3 — Degré d'un sommet

Dans un graphe **non orienté**, le **degré** d'un sommet est son nombre de voisins.

1. Écrire une fonction `degre(graphe, sommet)` qui renvoie le degré d'un sommet, à partir d'une représentation en dictionnaire de listes.
2. Écrire une fonction `sommet_isole(graphe)` qui renvoie `True` si le graphe contient au moins un sommet de degré 0.

### Exercice 4 — Parcours à la main

On donne le graphe non orienté `graphe = {"1": ["2", "3"], "2": ["1", "4"], "3": ["1", "4"], "4": ["2", "3", "5"], "5": ["4"]}`.

1. Donner, sans exécuter de code, le résultat de `parcours_profondeur(graphe, "1")`.
2. Donner, sans exécuter de code, le résultat de `parcours_largeur(graphe, "1")`.
3. Ce graphe contient-il un cycle ?

### Exercice 5 — Composantes connexes

Un graphe non orienté peut être formé de plusieurs morceaux séparés (**composantes connexes**), non reliés entre eux.

Écrire une fonction `composantes_connexes(graphe)` qui renvoie la liste des composantes connexes d'un graphe non orienté (chaque composante étant la liste des sommets qui la composent), en réutilisant `parcours_profondeur` du cours.

### Exercice 6 — Nombre minimal de correspondances

On modélise un réseau de bus par un graphe non orienté où chaque sommet est un arrêt, et une arête relie deux arrêts desservis par la même ligne directe.

Expliquer, en une phrase, quel algorithme du cours permet de calculer le nombre minimal de correspondances pour aller d'un arrêt à un autre, et pourquoi.

---

## Corrigés

### Exercice 1

1. Orienté : « suivre » n'est pas symétrique (Alice suit Bob, mais rien n'indique que Bob suit Alice).
2. Sommets : `Alice, Bob, Claire, David`. Arcs : `Alice→Bob, Bob→Claire, Claire→Alice, Claire→David`.
3. Successeurs de `Claire` : `Alice, David`.
4. Oui : `Alice → Bob → Claire → Alice` est un cycle.

### Exercice 2

```python
graphe = {
    "Alice": ["Bob"],
    "Bob": ["Claire"],
    "Claire": ["Alice", "David"],
    "David": [],
}

matrice = [
    [0, 1, 0, 0],   # Alice
    [0, 0, 1, 0],   # Bob
    [1, 0, 0, 1],   # Claire
    [0, 0, 0, 0],   # David
]
```

### Exercice 3

```python
def degre(graphe, sommet):
    return len(graphe[sommet])

def sommet_isole(graphe):
    for sommet in graphe:
        if degre(graphe, sommet) == 0:
            return True
    return False
```

### Exercice 4

1. Parcours en profondeur depuis `"1"` : `["1", "2", "4", "3", "5"]`.
2. Parcours en largeur depuis `"1"` : `["1", "2", "3", "4", "5"]`.
3. Oui : par exemple `1 → 2 → 4 → 3 → 1` est un cycle.

### Exercice 5

```python
def parcours_profondeur(graphe, depart):
    visites = []
    def explorer(sommet):
        if sommet not in visites:
            visites.append(sommet)
            for voisin in graphe[sommet]:
                explorer(voisin)
    explorer(depart)
    return visites

def composantes_connexes(graphe):
    deja_vus = set()
    composantes = []
    for sommet in graphe:
        if sommet not in deja_vus:
            composante = parcours_profondeur(graphe, sommet)
            composantes.append(composante)
            deja_vus.update(composante)
    return composantes
```

### Exercice 6

Le parcours en **largeur** (BFS), car il visite les sommets par distance croissante (en nombre d'arêtes) depuis le point de départ : le nombre de correspondances correspond exactement à la distance (en arêtes) entre les deux arrêts dans ce graphe, ce que `plus_court_chemin` (basé sur un parcours en largeur) calcule directement.
