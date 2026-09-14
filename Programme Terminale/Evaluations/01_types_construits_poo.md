# Chapitre 1 — Types construits & POO
## Évaluation

*Terminale NSI — Durée : 55 min — Barème sur 20 points*

*Document et calculatrice non autorisés. Rédiger le code en Python 3.*

---

### Partie 1 — Questions de cours (6 points)

**Question 1 (2 pts).** Pour chacune des affirmations suivantes, dire si elle est vraie ou fausse (aucune justification demandée) :

a) Un n-uplet est mutable.
b) Une liste (tableau) est mutable.
c) Un dictionnaire permet d'accéder à une valeur par une clé plutôt que par un indice.
d) `self` désigne la classe elle-même, et non un objet particulier.

**Question 2 (2 pts).** Définir en une phrase chacune des notions suivantes : *attribut*, *méthode*.

**Question 3 (2 pts).** Expliquer, en deux ou trois phrases, la différence entre l'**interface** et l'**implémentation** d'une classe. Donner un exemple.

---

### Partie 2 — Types construits (6 points)

On dispose du tableau de dictionnaires suivant, représentant des relevés météo :

```python
releves = [
    {"ville": "Lyon", "temperature": 18, "pluie": False},
    {"ville": "Brest", "temperature": 14, "pluie": True},
    {"ville": "Nice", "temperature": 24, "pluie": False},
]
```

**Question 4 (3 pts).** Écrire une fonction `villes_sans_pluie(releves)` qui renvoie la liste des noms des villes où il ne pleut pas.

**Question 5 (3 pts).** Écrire une fonction `temperature_moyenne(releves)` qui renvoie la température moyenne de l'ensemble des relevés (on pourra renvoyer un `float`).

---

### Partie 3 — Programmation orientée objet (8 points)

On souhaite modéliser des figures géométriques simples pour un logiciel de dessin.

**Question 6 (5 pts).** Écrire une classe `Cercle` telle que :
- le constructeur prend en paramètre un `rayon` (positif) ;
- une méthode `aire()` renvoie l'aire du cercle (formule : π × rayon², on utilisera `3.14` pour π) ;
- une méthode `perimetre()` renvoie le périmètre (formule : 2 × π × rayon) ;
- une méthode `agrandir(facteur)` multiplie le rayon par `facteur`.

**Question 7 (3 pts).** On ajoute à la classe `Cercle` l'attribut privé suivant :

```python
class Cercle:
    def __init__(self, rayon):
        self.__rayon = rayon
```

a) (1 pt) Pourquoi l'instruction `mon_cercle.__rayon` provoque-t-elle une erreur à l'extérieur de la classe ?
b) (2 pts) Proposer une méthode `obtenir_rayon(self)` permettant d'accéder malgré tout à la valeur du rayon depuis l'extérieur, en respectant l'esprit de l'encapsulation.

---

## Corrigé et barème détaillé

### Partie 1 (6 pts)

**Q1 (2 pts — 0,5 pt/item)**
a) Faux — b) Vrai — c) Vrai — d) Faux (`self` désigne l'objet/l'instance sur lequel la méthode est appelée, pas la classe).

**Q2 (2 pts — 1 pt/item)**
- *Attribut* : une donnée (une variable) associée à un objet, stockée dans son état interne.
- *Méthode* : une fonction associée à une classe, qui agit sur les objets de cette classe (et prend `self` en premier paramètre).

**Q3 (2 pts)**
L'interface d'une classe est l'ensemble des méthodes (et éventuellement attributs) accessibles depuis l'extérieur, c'est-à-dire ce que doit connaître un utilisateur de la classe pour s'en servir. L'implémentation est la façon dont ces méthodes sont effectivement codées en interne. On peut changer l'implémentation sans changer l'interface : par exemple, une classe `Pile` peut être implémentée avec une liste Python ou avec un tableau de taille fixe, sans que cela change la façon dont on utilise `empiler()` et `depiler()`. *(1 pt pour la définition, 1 pt pour l'exemple pertinent.)*

### Partie 2 (6 pts)

**Q4 (3 pts)**
```python
def villes_sans_pluie(releves):
    return [r["ville"] for r in releves if not r["pluie"]]
```
*(1 pt : parcours correct ; 1 pt : condition correcte ; 1 pt : renvoi du bon champ.)*

**Q5 (3 pts)**
```python
def temperature_moyenne(releves):
    total = 0
    for r in releves:
        total = total + r["temperature"]
    return total / len(releves)
```
*(1 pt : accumulation correcte ; 1 pt : division par le bon effectif ; 1 pt : gestion correcte des accès aux dictionnaires.)*

### Partie 3 (8 pts)

**Q6 (5 pts)**
```python
class Cercle:
    def __init__(self, rayon):
        self.rayon = rayon

    def aire(self):
        return 3.14 * self.rayon ** 2

    def perimetre(self):
        return 2 * 3.14 * self.rayon

    def agrandir(self, facteur):
        self.rayon = self.rayon * facteur
```
*(1 pt constructeur ; 1,5 pt aire ; 1,5 pt périmètre ; 1 pt agrandir.)*

**Q7 (3 pts)**
a) (1 pt) `__rayon` est un attribut « privé » : Python applique un *name mangling* (renommage automatique en `_Cercle__rayon`), ce qui rend l'accès direct par `mon_cercle.__rayon` impossible depuis l'extérieur de la classe et lève une `AttributeError`.

b) (2 pts)
```python
    def obtenir_rayon(self):
        return self.__rayon
```
On expose une méthode publique qui contrôle l'accès en lecture, sans autoriser de modification directe de l'attribut : c'est le principe même de l'encapsulation.

---

**Barème global : 6 + 6 + 8 = 20 points.**
