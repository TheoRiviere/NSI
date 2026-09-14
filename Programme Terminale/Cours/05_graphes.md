# Terminale NSI — Chapitre 5
# Graphes : structures et algorithmes

*Support de cours — Python 3*

---

## Objectifs du chapitre

- Connaître le vocabulaire des graphes (sommet, arête, arc, orienté/non orienté).
- Représenter un graphe par une matrice d'adjacence ou par des listes de successeurs.
- Parcourir un graphe en profondeur et en largeur.
- Détecter un cycle, rechercher un chemin.

**Prérequis :** chapitre 4 (arbres, récursivité, notion de file).

---

## 5.1 Vocabulaire

Un **graphe** est constitué de **sommets** (ou *nœuds*) reliés par des **arêtes** (graphe **non orienté**) ou des **arcs** (graphe **orienté**, où chaque liaison a un sens).

- Graphe **non orienté** : les liaisons sont symétriques (ex. le réseau routier, les réseaux sociaux d'amitié réciproque).
- Graphe **orienté** : les liaisons ont un sens (ex. les liens d'abonnement sur un réseau social, le routage sur internet).

```
Non orienté :        Orienté :
   A --- B               A --> B
   |     |                ^     \
   C --- D                |      v
                           D <-- C
```

On appelle **voisins** (ou **successeurs**, dans un graphe orienté) d'un sommet les sommets directement reliés à lui.

---

## 5.2 Représenter un graphe

### Matrice d'adjacence

On numérote les sommets de `0` à `n-1` et on construit un tableau `n × n` où la case `[i][j]` vaut `1` (ou `True`) s'il existe une arête/un arc de `i` vers `j`, `0` sinon.

```python
# Graphe non orienté à 4 sommets : A(0)-B(1), A(0)-C(2), B(1)-D(3), C(2)-D(3)
matrice = [
    [0, 1, 1, 0],   # A
    [1, 0, 0, 1],   # B
    [1, 0, 0, 1],   # C
    [0, 1, 1, 0],   # D
]
```

Pour un graphe **non orienté**, la matrice est **symétrique** (`matrice[i][j] == matrice[j][i]`).

**Avantage :** tester l'existence d'une arête entre deux sommets est immédiat (`matrice[i][j]`). **Inconvénient :** la matrice occupe `n²` cases, même si le graphe a peu d'arêtes.

### Listes de successeurs (ou d'adjacence)

On associe à chaque sommet la liste de ses voisins (ou de ses successeurs, pour un graphe orienté) :

```python
# Le même graphe non orienté, sous forme de dictionnaire de listes
graphe = {
    "A": ["B", "C"],
    "B": ["A", "D"],
    "C": ["A", "D"],
    "D": ["B", "C"],
}
```

**Avantage :** occupe une place proportionnelle au nombre d'arêtes, ce qui est plus économique pour un graphe **peu dense** (peu d'arêtes par rapport au nombre maximal possible). **Inconvénient :** tester l'existence d'une arête précise nécessite de parcourir une liste.

### Passer d'une représentation à l'autre

```python
def matrice_vers_listes(matrice, sommets):
    graphe = {s: [] for s in sommets}
    for i in range(len(sommets)):
        for j in range(len(sommets)):
            if matrice[i][j] == 1:
                graphe[sommets[i]].append(sommets[j])
    return graphe

def listes_vers_matrice(graphe, sommets):
    n = len(sommets)
    matrice = [[0] * n for _ in range(n)]
    index = {s: i for i, s in enumerate(sommets)}
    for sommet, voisins in graphe.items():
        for voisin in voisins:
            matrice[index[sommet]][index[voisin]] = 1
    return matrice
```

> **Quel choix ?** On privilégie la matrice d'adjacence si le graphe est **dense** (beaucoup d'arêtes) ou si l'on doit tester très fréquemment l'existence d'une arête précise ; on privilégie les listes de successeurs si le graphe est **peu dense** (cas fréquent en pratique : réseau routier, réseau social...) ou si l'on doit surtout parcourir les voisins d'un sommet — ce qui est le cas des algorithmes de parcours étudiés ci-dessous.

---

## 5.3 Parcours d'un graphe

On utilise la représentation par listes de successeurs (dictionnaire). Contrairement à un arbre, un graphe peut contenir des **cycles** : il faut donc mémoriser les sommets déjà visités pour ne pas boucler indéfiniment.

### Parcours en profondeur (DFS)

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
```

### Parcours en largeur (BFS)

Comme pour les arbres (chapitre 4), on utilise une **file** :

```python
def parcours_largeur(graphe, depart):
    visites = [depart]
    file = [depart]
    while len(file) > 0:
        sommet = file.pop(0)
        for voisin in graphe[sommet]:
            if voisin not in visites:
                visites.append(voisin)
                file.append(voisin)
    return visites
```

Sur le graphe `A: [B, C], B: [A, D], C: [A, D], D: [B, C]`, en partant de `"A"` :
- `parcours_profondeur` donne `["A", "B", "D", "C"]` ;
- `parcours_largeur` donne `["A", "B", "C", "D"]`.

---

## 5.4 Détecter un cycle

Un **cycle** est un chemin qui part d'un sommet et y revient sans repasser deux fois par la même arête. On peut détecter un cycle dans un graphe non orienté en adaptant le parcours en profondeur, en retenant d'où l'on vient :

```python
def contient_cycle(graphe):
    visites = set()

    def explorer(sommet, parent):
        visites.add(sommet)
        for voisin in graphe[sommet]:
            if voisin not in visites:
                if explorer(voisin, sommet):
                    return True
            elif voisin != parent:
                return True   # on retombe sur un sommet déjà visité, autre que le parent direct
        return False

    for sommet in graphe:
        if sommet not in visites:
            if explorer(sommet, None):
                return True
    return False
```

---

## 5.5 Recherche d'un chemin

Pour trouver **un** chemin entre deux sommets (pas nécessairement le plus court), on adapte le parcours en profondeur en mémorisant le chemin parcouru :

```python
def chercher_chemin(graphe, depart, arrivee, visites=None):
    if visites is None:
        visites = set()
    if depart == arrivee:
        return [depart]
    visites.add(depart)
    for voisin in graphe[depart]:
        if voisin not in visites:
            chemin = chercher_chemin(graphe, voisin, arrivee, visites)
            if chemin is not None:
                return [depart] + chemin
    return None
```

Pour trouver le **plus court chemin** (en nombre d'arêtes) dans un graphe non pondéré, on utilise un parcours en **largeur**, qui garantit de visiter les sommets dans l'ordre croissant de leur distance au départ :

```python
def plus_court_chemin(graphe, depart, arrivee):
    file = [depart]
    predecesseur = {depart: None}
    while len(file) > 0:
        sommet = file.pop(0)
        if sommet == arrivee:
            chemin = []
            while sommet is not None:
                chemin.append(sommet)
                sommet = predecesseur[sommet]
            chemin.reverse()
            return chemin
        for voisin in graphe[sommet]:
            if voisin not in predecesseur:
                predecesseur[voisin] = sommet
                file.append(voisin)
    return None
```

> **Application concrète.** Le parcours d'un labyrinthe et le routage sur internet sont deux exemples classiques d'utilisation des algorithmes de parcours de graphes (voir aussi le chapitre sur les réseaux, où l'on relie cette idée aux protocoles de routage).

---

## 5.6 Synthèse

| Notion | Définition |
|---|---|
| Sommet | Élément de base d'un graphe |
| Arête / arc | Liaison non orientée / orientée entre deux sommets |
| Matrice d'adjacence | Tableau `n × n` indiquant les liaisons ; pratique pour tester une liaison précise |
| Liste de successeurs | Association sommet → liste de voisins ; économique pour un graphe peu dense |
| Parcours en profondeur (DFS) | Explore aussi loin que possible avant de revenir en arrière (récursif ou pile) |
| Parcours en largeur (BFS) | Explore niveau par niveau (file) ; donne le plus court chemin en nombre d'arêtes |
| Cycle | Chemin qui revient à son point de départ |

*Prochaine étape suggérée : chapitre 6, la récursivité, pour formaliser et approfondir les techniques utilisées dans ce chapitre.*
