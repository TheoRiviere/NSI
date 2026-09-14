# Terminale NSI — Types construits & Programmation orientée objet

*Support de cours — Python 3*

---

## Objectifs du chapitre

À l'issue de ce chapitre, les élèves doivent être capables de :

- choisir, créer et manipuler un n-uplet, un n-uplet nommé, un tableau, un tableau de tableaux et un enregistrement ;
- distinguer les types mutables des types immuables et en anticiper les conséquences ;
- définir une classe Python simple (attributs, constructeur, méthodes) ;
- expliquer les notions d'objet, d'encapsulation et d'interface ;
- utiliser une classe existante en s'appuyant uniquement sur son interface, sans connaître son implémentation.

**Prérequis (Première NSI) :** types simples (`int`, `float`, `bool`, `str`), listes, fonctions, notion de mutabilité de base.

---

## Partie 1 — Les types construits

### 1.1 Pourquoi des types construits ?

Un type construit permet de regrouper plusieurs valeurs — de même type ou de types différents — au sein d'une seule structure de données. On distingue quatre types construits au programme :

| Type | Exemple Python | Mutable ? | Accès |
|---|---|---|---|
| n-uplet (tuple) | `(3, 5)` | non | par indice |
| n-uplet nommé | `Point(x=3, y=5)` | non | par indice ou par nom |
| tableau (liste) | `[3, 5, 8]` | oui | par indice |
| enregistrement (dictionnaire) | `{"nom": "Ada", "age": 36}` | oui | par clé |

### 1.2 Les n-uplets (`tuple`)

Un **n-uplet** est une séquence *ordonnée* et *immuable* de valeurs, pas nécessairement de même type.

```python
point = (3, 5)          # un couple : 2-uplet
rgb = (255, 128, 0)      # un triplet : 3-uplet
etudiant = ("Ada", 17, "Terminale NSI")

# Accès par indice
print(point[0])   # 3
print(point[1])   # 5

# Affectation multiple (déballage / "unpacking")
x, y = point
print(x, y)        # 3 5
```

**Immutabilité.** Un n-uplet ne peut pas être modifié après sa création :

```python
point[0] = 10   # lève une erreur : TypeError: 'tuple' object does not support item assignment
```

Un n-uplet permet en revanche de renvoyer plusieurs valeurs depuis une fonction :

```python
def coordonnees_min_max(valeurs):
    return min(valeurs), max(valeurs)   # renvoie un 2-uplet

mini, maxi = coordonnees_min_max([4, 1, 9, 2])
```

### 1.3 Les n-uplets nommés (`namedtuple`)

Accéder à un élément par son indice (`point[0]`) nuit à la lisibilité : que représente `point[0]` ? Le **n-uplet nommé** associe un nom à chaque champ tout en conservant l'immutabilité et la légèreté d'un tuple.

```python
from collections import namedtuple

Point = namedtuple("Point", ["x", "y"])
p = Point(3, 5)

print(p.x, p.y)   # 3 5
print(p[0], p[1]) # 3 5  (l'accès par indice reste possible)
```

> **Remarque pédagogique.** Le n-uplet nommé est souvent introduit en comparaison avec l'enregistrement (1.5) : il permet de nommer des champs comme un dictionnaire, tout en restant immuable comme un tuple.

### 1.4 Les tableaux (listes Python)

En NSI, le **tableau** désigne une séquence *ordonnée*, *indexée* et *mutable* d'éléments. En Python, cette structure est représentée par le type `list`.

```python
notes = [12, 15, 8, 17, 10]

notes[2] = 9            # modification d'un élément
notes.append(14)         # ajout en fin de tableau
print(len(notes))        # taille du tableau

# Parcours par indice
for i in range(len(notes)):
    print(i, notes[i])

# Parcours par valeur
for note in notes:
    print(note)
```

**Attention à la mutabilité.** Contrairement au n-uplet, une liste peut être modifiée « en place », ce qui a des conséquences importantes lors du passage en paramètre d'une fonction :

```python
def vider(tableau):
    tableau.clear()

t = [1, 2, 3]
vider(t)
print(t)   # [] : la fonction a modifié l'objet original
```

#### Tableaux de tableaux (matrices)

Un tableau peut contenir d'autres tableaux : on obtient un **tableau à deux dimensions**, utile pour représenter une grille, une image ou une matrice.

```python
grille = [
    [0, 1, 0],
    [1, 1, 0],
    [0, 0, 1],
]

print(grille[1][2])   # ligne 1, colonne 2 -> 0

# Parcours complet
for i in range(len(grille)):
    for j in range(len(grille[i])):
        print(grille[i][j], end=" ")
    print()
```

> **Piège classique à signaler aux élèves :** `[[0] * 3] * 3` crée trois références vers **la même** sous-liste. Modifier `grille[0][0]` modifie alors aussi `grille[1][0]` et `grille[2][0]`. La construction correcte est une compréhension de liste :
>
> ```python
> grille = [[0 for _ in range(3)] for _ in range(3)]
> ```

### 1.5 Les enregistrements (dictionnaires)

Un **enregistrement** regroupe des champs identifiés par un nom (une *clé*) plutôt que par une position. En Python, on utilise le type `dict`.

```python
etudiant = {
    "nom": "Lovelace",
    "prenom": "Ada",
    "age": 17,
    "classe": "Terminale NSI",
}

print(etudiant["nom"])        # accès par clé
etudiant["age"] = 18            # modification
etudiant["moyenne"] = 15.5      # ajout d'un nouveau champ

for cle in etudiant:
    print(cle, "->", etudiant[cle])
```

On peut combiner tableaux et enregistrements pour représenter une base de données simple :

```python
classe = [
    {"nom": "Lovelace", "age": 17},
    {"nom": "Turing", "age": 18},
]

for eleve in classe:
    print(eleve["nom"])
```

### 1.6 Synthèse — quel type choisir ?

- Je veux regrouper des valeurs **hétérogènes**, en petit nombre, qui ne changeront pas → **n-uplet**, ou **n-uplet nommé** si la lisibilité par nom de champ est utile.
- Je veux une **collection homogène**, de taille variable, que je vais modifier → **tableau (liste)**.
- Je veux une grille / une matrice → **tableau de tableaux**.
- Je veux identifier chaque valeur par un **nom explicite** (comme une fiche) → **enregistrement (dictionnaire)**.

---

## Partie 2 — Programmation orientée objet

### 2.1 Motivation

Jusqu'ici, les données (types construits) et les traitements (fonctions) sont séparés. La **programmation orientée objet (POO)** propose de regrouper au sein d'une même structure, appelée **classe**, les données (les **attributs**) et les traitements associés (les **méthodes**).

Un **objet** est une *instance* d'une classe : la classe est le modèle (le plan), l'objet est une réalisation concrète de ce modèle.

> **Analogie à donner en classe :** la classe `Voiture` est comme le plan d'un constructeur automobile ; chaque voiture qui sort de l'usine (chaque objet) est une instance de ce plan, avec ses propres valeurs (couleur, plaque d'immatriculation…) mais le même comportement (démarrer, freiner…).

### 2.2 Définir une classe

```python
class Point:
    """Représente un point du plan."""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance_origine(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def deplacer(self, dx, dy):
        self.x = self.x + dx
        self.y = self.y + dy
```

- `class Point:` déclare la classe.
- `__init__` est le **constructeur** : il est appelé automatiquement à la création d'un objet et initialise ses attributs.
- `self` désigne l'objet en cours de manipulation ; c'est toujours le premier paramètre d'une méthode.
- `self.x` et `self.y` sont les **attributs** de l'objet.
- `distance_origine` et `deplacer` sont des **méthodes** : des fonctions attachées à la classe.

**Créer et utiliser des objets (instanciation) :**

```python
p1 = Point(3, 4)
p2 = Point(0, 0)

print(p1.x, p1.y)              # 3 4
print(p1.distance_origine())    # 5.0

p1.deplacer(1, 1)
print(p1.x, p1.y)              # 4 5
```

`p1` et `p2` sont deux **instances** distinctes de la classe `Point`, chacune avec ses propres valeurs d'attributs.

### 2.3 Un exemple filé : la classe `CompteBancaire`

Cet exemple, plus riche, permet d'introduire l'encapsulation.

```python
class CompteBancaire:
    def __init__(self, titulaire, solde_initial=0):
        self.titulaire = titulaire
        self._solde = solde_initial          # attribut "protégé" par convention

    def deposer(self, montant):
        if montant <= 0:
            raise ValueError("Le montant doit être positif")
        self._solde = self._solde + montant

    def retirer(self, montant):
        if montant > self._solde:
            raise ValueError("Solde insuffisant")
        self._solde = self._solde - montant

    def consulter_solde(self):
        return self._solde


compte = CompteBancaire("Ada Lovelace", 100)
compte.deposer(50)
compte.retirer(30)
print(compte.consulter_solde())   # 120
```

### 2.4 Encapsulation

L'**encapsulation** consiste à protéger les attributs d'un objet en n'autorisant leur modification que par l'intermédiaire de méthodes contrôlées (ici `deposer` et `retirer`), plutôt que par un accès direct comme `compte._solde = -1000`.

- En Python, il n'existe pas de véritable attribut privé (contrairement à Java ou C++). La convention est d'utiliser :
  - `_attribut` : « protégé », ne devrait pas être manipulé directement en dehors de la classe (convention, non imposée par le langage) ;
  - `__attribut` : « privé », le nom est automatiquement transformé (*name mangling*) pour compliquer l'accès direct.

```python
class CompteBancaire:
    def __init__(self, titulaire, solde_initial=0):
        self.titulaire = titulaire
        self.__solde = solde_initial   # attribut privé

    def consulter_solde(self):
        return self.__solde
```

```python
compte = CompteBancaire("Ada", 100)
print(compte.__solde)   # AttributeError : accès direct impossible
print(compte.consulter_solde())   # 100 : accès contrôlé via une méthode
```

### 2.5 Notion d'interface

L'**interface** d'une classe est l'ensemble de ses méthodes (et éventuellement attributs) accessibles depuis l'extérieur : c'est ce que l'utilisateur de la classe a besoin de connaître pour l'utiliser, **sans avoir à connaître son implémentation** (le code à l'intérieur des méthodes).

Un utilisateur de `CompteBancaire` doit seulement savoir que `deposer`, `retirer` et `consulter_solde` existent et ce qu'elles font — pas comment le solde est stocké en interne. Cela permet de modifier l'implémentation d'une classe (par exemple stocker l'historique des opérations) **sans changer le code qui l'utilise**, tant que l'interface reste la même.

> **Point de vigilance pour le cours :** insister sur la différence entre *interface* (le « quoi », le contrat) et *implémentation* (le « comment »). C'est une idée réutilisée plus tard avec les structures de données abstraites (piles, files, listes chaînées).

### 2.6 Synthèse

| Notion | Définition |
|---|---|
| Classe | Modèle décrivant la structure (attributs) et le comportement (méthodes) d'un ensemble d'objets |
| Objet / instance | Réalisation concrète d'une classe, avec ses propres valeurs d'attributs |
| Attribut | Donnée associée à un objet |
| Méthode | Fonction associée à une classe, agissant sur ses objets (premier paramètre `self`) |
| Constructeur (`__init__`) | Méthode spéciale appelée à la création d'un objet |
| Encapsulation | Protection des attributs, accès contrôlé via des méthodes |
| Interface | Ensemble des méthodes/attributs exposés à l'utilisateur d'une classe |

---

## Pour aller plus loin (pistes de prolongement)

- Réécrire la classe `Point` avec une méthode spéciale `__str__` pour un affichage lisible (`print(p1)`).
- Comparer un `namedtuple` `Point(x, y)` immuable à une classe `Point` mutable : quand préférer l'un ou l'autre ?
- Introduire une deuxième classe qui utilise des objets de la première (ex. `PortefeuilleDeComptes` qui contient une liste de `CompteBancaire`), pour préparer l'agrégation d'objets.

*Prochaine étape suggérée : une fiche d'exercices d'application sur ces deux notions, puis un TP de synthèse combinant tableaux d'objets et enregistrements.*
