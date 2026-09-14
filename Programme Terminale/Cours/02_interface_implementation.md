# Terminale NSI — Chapitre 2
# Interface et implémentation des structures de données

*Support de cours — Python 3*

---

## Objectifs du chapitre

- Distinguer la spécification (interface) d'une structure de données de sa réalisation concrète (implémentation).
- Spécifier une structure de données abstraite par son interface.
- Écrire plusieurs implémentations différentes d'une même structure de données.
- Comprendre l'intérêt pratique de cette séparation.

**Prérequis :** chapitre 1 (classes, attributs, méthodes, encapsulation).

---

## 2.1 Une structure de données abstraite, qu'est-ce que c'est ?

Une **structure de données abstraite** (ou *type abstrait*) est définie uniquement par :

- les **opérations** qu'on peut effectuer sur elle (son *interface*) ;
- le **comportement attendu** de ces opérations (ce qu'elles font, pas comment) ;

et **pas** par la façon dont les données sont effectivement stockées en mémoire (son *implémentation*).

> **Analogie.** Le volant, les pédales et le levier de vitesse d'une voiture forment son *interface* de conduite : n'importe quel conducteur sait s'en servir. Ce qu'il y a sous le capot — moteur thermique, électrique, hybride — est l'*implémentation* : elle peut varier sans que l'interface change.

### Interface vs implémentation

| | Interface | Implémentation |
|---|---|---|
| Ce qu'elle décrit | *Quoi* : les opérations disponibles et leur effet | *Comment* : le code qui réalise ces opérations |
| Visible pour l'utilisateur ? | Oui, c'est tout ce qu'il a besoin de connaître | Non, ou pas nécessairement |
| Peut-elle changer sans casser le code utilisateur ? | Non (sinon le code utilisateur ne fonctionne plus) | Oui, tant que l'interface est respectée |

---

## 2.2 Exemple filé : la pile (*stack*)

### Spécification (interface)

Une **pile** est une structure de données qui range les éléments selon le principe **LIFO** (*Last In, First Out* : le dernier entré est le premier sorti). On la spécifie par les opérations suivantes :

| Opération | Rôle |
|---|---|
| `empiler(e)` | ajoute l'élément `e` au sommet de la pile |
| `depiler()` | retire et renvoie l'élément au sommet de la pile |
| `sommet()` | renvoie (sans le retirer) l'élément au sommet |
| `est_vide()` | renvoie `True` si la pile ne contient aucun élément |

Cette spécification **ne dit rien** sur la façon dont la pile est stockée en mémoire : c'est justement le rôle de l'implémentation.

### Implémentation 1 — avec une liste Python

```python
class PileListe:
    def __init__(self):
        self._elements = []

    def empiler(self, e):
        self._elements.append(e)

    def depiler(self):
        if self.est_vide():
            raise IndexError("dépiler sur une pile vide")
        return self._elements.pop()

    def sommet(self):
        if self.est_vide():
            raise IndexError("sommet sur une pile vide")
        return self._elements[-1]

    def est_vide(self):
        return len(self._elements) == 0
```

### Implémentation 2 — avec un tableau de taille fixe

Une seconde implémentation, plus proche de ce qu'on trouverait dans un langage bas niveau, utilise un tableau de capacité fixée à l'avance et un indice `_taille` qui suit le nombre d'éléments réellement utilisés.

```python
class PileTableauFixe:
    def __init__(self, capacite):
        self._capacite = capacite
        self._tableau = [None] * capacite
        self._taille = 0

    def empiler(self, e):
        if self._taille == self._capacite:
            raise OverflowError("pile pleine")
        self._tableau[self._taille] = e
        self._taille += 1

    def depiler(self):
        if self.est_vide():
            raise IndexError("dépiler sur une pile vide")
        self._taille -= 1
        return self._tableau[self._taille]

    def sommet(self):
        if self.est_vide():
            raise IndexError("sommet sur une pile vide")
        return self._tableau[self._taille - 1]

    def est_vide(self):
        return self._taille == 0
```

### Ce que montre cet exemple

Les deux classes `PileListe` et `PileTableauFixe` ont **exactement la même interface** (`empiler`, `depiler`, `sommet`, `est_vide`) mais des implémentations totalement différentes. Un code qui utilise une pile peut être écrit **une seule fois**, indépendamment de l'implémentation choisie :

```python
def tester_pile(pile):
    pile.empiler(1)
    pile.empiler(2)
    pile.empiler(3)
    print(pile.depiler())   # 3
    print(pile.sommet())    # 2

tester_pile(PileListe())
tester_pile(PileTableauFixe(10))
```

Ce code fonctionne à l'identique avec les deux implémentations : c'est tout l'intérêt de raisonner par interface.

---

## 2.3 Exemple filé : la file (*queue*)

Une **file** range les éléments selon le principe **FIFO** (*First In, First Out* : le premier entré est le premier sorti — comme une file d'attente).

| Opération | Rôle |
|---|---|
| `enfiler(e)` | ajoute l'élément `e` en fin de file |
| `defiler()` | retire et renvoie l'élément en tête de file |
| `est_vide()` | renvoie `True` si la file est vide |

### Implémentation naïve avec une liste

```python
class FileListe:
    def __init__(self):
        self._elements = []

    def enfiler(self, e):
        self._elements.append(e)

    def defiler(self):
        if self.est_vide():
            raise IndexError("défiler sur une file vide")
        return self._elements.pop(0)   # coûteux : décale tous les éléments

    def est_vide(self):
        return len(self._elements) == 0
```

> **Remarque sur le coût.** `self._elements.pop(0)` doit décaler tous les éléments restants d'un cran : cette opération a un coût proportionnel à la taille de la file. C'est une implémentation simple, mais peu efficace pour de grandes files.

### Implémentation avec deux piles

Une idée plus subtile consiste à utiliser **deux piles** : une pile `_entree` pour les arrivées, une pile `_sortie` pour les départs. Lorsqu'on doit défiler et que `_sortie` est vide, on transfère tous les éléments de `_entree` vers `_sortie` (ce qui inverse leur ordre, et retrouve ainsi l'ordre FIFO).

```python
class FileDeuxPiles:
    def __init__(self):
        self._entree = PileListe()
        self._sortie = PileListe()

    def enfiler(self, e):
        self._entree.empiler(e)

    def defiler(self):
        if self.est_vide():
            raise IndexError("défiler sur une file vide")
        if self._sortie.est_vide():
            while not self._entree.est_vide():
                self._sortie.empiler(self._entree.depiler())
        return self._sortie.depiler()

    def est_vide(self):
        return self._entree.est_vide() and self._sortie.est_vide()
```

Là encore, `FileListe` et `FileDeuxPiles` partagent exactement la même interface (`enfiler`, `defiler`, `est_vide`), pour deux implémentations très différentes — la seconde réutilisant même une autre structure de données (la pile) pour se construire.

---

## 2.4 Pourquoi séparer interface et implémentation ?

1. **Remplacer une implémentation sans casser le reste du programme.** Si l'on découvre une implémentation plus efficace, on peut la substituer sans modifier tout le code qui utilise la structure — à condition que l'interface reste identique.
2. **Comparer les performances.** Différentes implémentations d'une même interface peuvent avoir des coûts très différents (temps d'exécution, mémoire utilisée) : c'est le cas de `FileListe` (coût de `defiler` proportionnel à la taille) contre `FileDeuxPiles` (coût amorti constant).
3. **Raisonner à un niveau d'abstraction adapté.** Un programme qui utilise une pile pour évaluer une expression n'a pas besoin de savoir comment cette pile est représentée en mémoire.
4. **Travailler en équipe.** Une personne peut écrire l'implémentation pendant qu'une autre écrit le code qui utilise la structure, dès lors que l'interface est fixée à l'avance.

---

## 2.5 Synthèse

| Notion | Définition |
|---|---|
| Structure de données abstraite | Structure définie uniquement par ses opérations et leur comportement, indépendamment de tout stockage concret |
| Interface | Spécification des opérations disponibles (leur nom, leurs paramètres, leur effet attendu) |
| Implémentation | Réalisation concrète du stockage et du code des opérations |
| Pile (LIFO) | `empiler`, `depiler`, `sommet`, `est_vide` — dernier entré, premier sorti |
| File (FIFO) | `enfiler`, `defiler`, `est_vide` — premier entré, premier sorti |

*Prochaine étape suggérée : chapitre 3, structures linéaires (listes chaînées, piles, files, dictionnaires), pour approfondir l'implémentation de structures liées entre elles.*
