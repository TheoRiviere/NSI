# Chapitre 2 — Types construits : p-uplets, tableaux, dictionnaires

## Objectifs

- Utiliser le type p-uplet (tuple) et le p-uplet nommé pour regrouper des données hétérogènes.
- Manipuler des tableaux (listes) et des tableaux de tableaux (matrices).
- Utiliser un dictionnaire pour associer des clés à des valeurs.

## Prérequis

- Types de base (`int`, `float`, `bool`, `str`) — chapitre 1.
- Boucles `for` et `while`, indexation.

---

## 1. Pourquoi des types construits ?

Les types de base (`int`, `float`, `bool`, `str`) permettent de représenter une seule valeur isolée. Or, en pratique, on a très souvent besoin de regrouper plusieurs valeurs ensemble pour représenter une donnée plus complexe : les coordonnées d'un point, les notes d'un élève, le carnet d'adresses d'un utilisateur... C'est le rôle des **types construits**, qui permettent d'assembler des valeurs (éventuellement de types différents) en une seule structure de données.

---

## 2. Les p-uplets (tuples)

### 2.1 Définition et usage

Un **p-uplet** (en anglais *tuple*) est une séquence **ordonnée** et **non modifiable** (on dit *immuable*) de *p* valeurs, pas nécessairement du même type.

```python
point = (3, 5)          # un 2-uplet (couple)
personne = ("Dupont", "Alice", 17)   # un 3-uplet (triplet)
```

On accède à un élément par son indice, comme pour une chaîne de caractères :

```python
point[0]   # 3
point[1]   # 5
```

### 2.2 Le déballage (unpacking)

Une opération très fréquente consiste à « déballer » un p-uplet directement dans plusieurs variables :

```python
x, y = point
# x vaut 3, y vaut 5
```

Cette syntaxe est notamment utilisée pour qu'une fonction renvoie **plusieurs valeurs à la fois** (en réalité, un seul p-uplet) :

```python
def division_euclidienne(a, b):
    return a // b, a % b   # renvoie le tuple (quotient, reste)

q, r = division_euclidienne(17, 5)
# q vaut 3, r vaut 2
```

### 2.3 Immuabilité

Un p-uplet ne peut pas être modifié après sa création : toute tentative de modification lève une erreur.

```python
point[0] = 10   # lève TypeError: 'tuple' object does not support item assignment
```

Cette immuabilité est une caractéristique essentielle : elle garantit qu'un p-uplet, une fois créé, représente une donnée fixe et fiable (on peut par exemple l'utiliser comme clé de dictionnaire, ce qui est impossible avec une liste, comme on le verra plus loin).

### 2.4 Les p-uplets nommés (named tuples)

Accéder à `personne[1]` pour obtenir le prénom n'est pas très lisible : il faut se souvenir de l'ordre des champs. Le module `collections` propose les **p-uplets nommés**, qui permettent de nommer chaque champ tout en conservant l'immuabilité et la légèreté d'un tuple :

```python
from collections import namedtuple

Point = namedtuple('Point', ['x', 'y'])
p = Point(3, 5)

p.x       # 3  (accès par nom, plus lisible)
p.y       # 5
p[0]      # 3  (l'accès par indice reste aussi possible)
```

---

## 3. Les tableaux (listes)

### 3.1 Définition

Un **tableau**, réalisé en Python par le type `list`, est une séquence **ordonnée** et **modifiable** (dite *mutable*) de valeurs. Contrairement au p-uplet, on peut ajouter, retirer ou modifier des éléments après la création de la liste.

```python
notes = [12, 15, 8, 17]
```

### 3.2 Opérations courantes

```python
notes.append(20)        # ajoute 20 à la fin : [12, 15, 8, 17, 20]
notes[0] = 13            # modifie l'élément d'indice 0 : [13, 15, 8, 17, 20]
notes.insert(1, 100)     # insère 100 à l'indice 1 : [13, 100, 15, 8, 17, 20]
notes.remove(100)        # retire la première occurrence de 100
len(notes)                # nombre d'éléments
notes[1:3]                 # extrait une sous-liste (slicing)
```

**Attention à la distinction fondamentale entre p-uplet et liste :** on choisit un p-uplet lorsque la donnée représente un ensemble **fixe** de valeurs de nature différente (les coordonnées d'un point, les champs d'un enregistrement), et une liste lorsque l'on manipule une **collection homogène** de valeurs dont le nombre ou le contenu peut évoluer (les notes d'un élève au fil de l'année).

### 3.3 Parcours d'un tableau

```python
for note in notes:
    print(note)

for indice in range(len(notes)):
    print(indice, notes[indice])
```

---

## 4. Les tableaux de tableaux (matrices)

Un tableau de tableaux permet de représenter une structure à deux dimensions, comme un tableau à lignes et colonnes (une matrice, une grille, une image en niveaux de gris...).

```python
matrice = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
]
```

On accède à l'élément de la ligne `i` et de la colonne `j` avec `matrice[i][j]` :

```python
matrice[1][2]   # 6  (ligne d'indice 1, colonne d'indice 2)
```

Le nombre de lignes est `len(matrice)`, et le nombre de colonnes (en supposant la matrice « rectangulaire », c'est-à-dire que toutes les lignes ont la même longueur) est `len(matrice[0])`.

### 4.1 Exemple : transposer une matrice

Transposer une matrice consiste à échanger ses lignes et ses colonnes.

```python
def transposer(m):
    """Renvoie la transposée de la matrice m (liste de listes)."""
    lignes = len(m)
    colonnes = len(m[0])
    resultat = [[0] * lignes for _ in range(colonnes)]
    for i in range(lignes):
        for j in range(colonnes):
            resultat[j][i] = m[i][j]
    return resultat

transposer([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
# [[1, 4, 7], [2, 5, 8], [3, 6, 9]]
```

**Point de vigilance important :** pour créer une matrice de zéros, il faut écrire `[[0] * lignes for _ in range(colonnes)]` (une **compréhension de liste**, qui crée une nouvelle liste indépendante à chaque itération), et surtout **pas** `[[0] * lignes] * colonnes`, qui créerait plusieurs références vers la **même** ligne interne : modifier un élément d'une ligne modifierait alors, par erreur, la ligne correspondante de toutes les autres lignes.

---

## 5. Les dictionnaires (enregistrements)

### 5.1 Définition

Un **dictionnaire** (type `dict`) associe des **clés** à des **valeurs**. Contrairement à une liste où l'on accède aux éléments par un indice numérique, on accède aux éléments d'un dictionnaire par leur clé (qui peut être une chaîne de caractères, un entier, un tuple...).

```python
eleve = {"nom": "Dupont", "prenom": "Alice", "age": 17}
```

### 5.2 Opérations courantes

```python
eleve["nom"]              # "Dupont"  (accès par clé)
eleve["classe"] = "Terminale"   # ajoute une nouvelle paire clé/valeur
del eleve["age"]           # supprime la paire associée à la clé "age"
"nom" in eleve              # True (teste la présence d'une clé)
eleve.get("age", "inconnu") # "inconnu" (valeur par défaut si la clé n'existe pas, sans lever d'erreur)
```

### 5.3 Parcourir un dictionnaire

Trois méthodes essentielles permettent de parcourir un dictionnaire :

```python
eleve.keys()     # les clés : dict_keys(['nom', 'prenom', 'classe'])
eleve.values()   # les valeurs : dict_values(['Dupont', 'Alice', 'Terminale'])
eleve.items()    # les paires (clé, valeur) : dict_items([('nom', 'Dupont'), ...])

for cle, valeur in eleve.items():
    print(cle, "->", valeur)
```

### 5.4 Dictionnaire vs p-uplet nommé

Un dictionnaire et un p-uplet nommé se ressemblent (tous deux associent un nom à une valeur), mais leurs usages diffèrent : un p-uplet nommé décrit une structure **fixe**, connue à l'avance (les champs ne changent jamais d'un `Point` à l'autre), alors qu'un dictionnaire est adapté lorsque l'ensemble des clés peut varier d'une donnée à l'autre, ou n'est pas connu à l'avance (par exemple, un dictionnaire qui compte les occurrences de mots dans un texte : on ne connaît pas à l'avance la liste des mots qui serviront de clés).

---

## Synthèse

| Type construit | Ordonné ? | Modifiable ? | Accès | Usage typique |
|---|---|---|---|---|
| p-uplet (`tuple`) | Oui | Non | par indice | données hétérogènes fixes (coordonnées) |
| p-uplet nommé (`namedtuple`) | Oui | Non | par indice ou par nom | comme le tuple, mais plus lisible |
| tableau (`list`) | Oui | Oui | par indice | collection homogène de taille variable |
| tableau de tableaux | Oui | Oui | par deux indices | matrices, grilles, tables |
| dictionnaire (`dict`) | Non* | Oui | par clé | association clé → valeur, clés variables |

*\*Depuis Python 3.7, l'ordre d'insertion des clés est conservé en pratique, mais l'accès se fait conceptuellement par clé et non par position.*

*Prochaine étape suggérée : Chapitre 3 — Traitement de données en tables.*
