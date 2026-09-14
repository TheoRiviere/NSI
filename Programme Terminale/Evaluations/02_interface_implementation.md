# Chapitre 2 — Interface et implémentation
## Évaluation

*Terminale NSI — Durée : 50 min — Barème sur 20 points*

---

### Partie 1 — Questions de cours (7 points)

**Question 1 (3 pts).** Définir *interface* et *implémentation* d'une structure de données, puis expliquer en une phrase le lien entre les deux.

**Question 2 (2 pts).** Donner l'interface (liste des opérations, sans code) d'une pile, puis celle d'une file. En quoi diffèrent-elles ?

**Question 3 (2 pts).** Citer deux avantages concrets à séparer interface et implémentation dans la conception d'un programme.

---

### Partie 2 — Lecture de code (5 points)

On donne la classe suivante :

```python
class Mystere:
    def __init__(self):
        self._d = []

    def op1(self, e):
        self._d.append(e)

    def op2(self):
        return self._d.pop(0)

    def op3(self):
        return len(self._d) == 0
```

**Question 4 (2 pts).** À quelle structure de données connue correspond l'interface de cette classe (`op1`, `op2`, `op3`) ? Justifier en expliquant l'ordre dans lequel les éléments ressortent.

**Question 5 (3 pts).** On exécute :
```python
m = Mystere()
m.op1("a")
m.op1("b")
m.op1("c")
print(m.op2())
m.op1("d")
print(m.op2())
```
Donner les deux valeurs affichées, dans l'ordre.

---

### Partie 3 — Écrire une implémentation (8 points)

On souhaite implémenter l'interface suivante d'une structure **Deque** (file à double entrée), qui permet d'ajouter et de retirer des éléments **des deux côtés** :

- `ajouter_debut(e)` : ajoute `e` au début.
- `ajouter_fin(e)` : ajoute `e` à la fin.
- `retirer_debut()` : retire et renvoie l'élément du début.
- `retirer_fin()` : retire et renvoie l'élément de la fin.
- `est_vide()` : renvoie `True` si la structure est vide.

**Question 6 (8 pts).** Écrire une classe `DequeListe` qui implémente cette interface à l'aide d'une simple liste Python (les méthodes `insert(0, x)`, `append(x)`, `pop(0)` et `pop()` sont autorisées).

---

## Corrigé et barème détaillé

### Partie 1 (7 pts)

**Q1 (3 pts)** — L'interface est l'ensemble des opérations proposées par la structure, avec leur signature et leur effet attendu (1 pt). L'implémentation est la réalisation concrète du stockage et du code de ces opérations (1 pt). Une même interface peut avoir plusieurs implémentations différentes, tant que chacune respecte le comportement attendu (1 pt).

**Q2 (2 pts)** — Pile : `empiler`, `depiler`, `sommet`, `est_vide` (LIFO). File : `enfiler`, `defiler`, `est_vide` (FIFO). Elles diffèrent par l'ordre de sortie des éléments : dernier entré/premier sorti pour la pile, premier entré/premier sorti pour la file (1 pt pour chaque interface correcte, ou 1 pt liste + 1 pt distinction FIFO/LIFO).

**Q3 (2 pts, 1 pt/avantage parmi)** — Pouvoir remplacer une implémentation par une autre plus efficace sans modifier le code qui l'utilise ; pouvoir comparer les performances de plusieurs implémentations ; permettre à plusieurs personnes de travailler en parallèle sur l'implémentation et sur le code client ; raisonner à un niveau d'abstraction adapté sans se soucier des détails de stockage.

### Partie 2 (5 pts)

**Q4 (2 pts)** — Il s'agit d'une **file (FIFO)** : `op2` retire l'élément le plus ancien (`pop(0)`), donc le premier ajouté est le premier retiré.

**Q5 (3 pts)** — Premier affichage : `"a"` (premier ajouté). Deuxième affichage : `"b"`. *(1,5 pt par bonne réponse.)*

### Partie 3 (8 pts)

```python
class DequeListe:
    def __init__(self):
        self._elements = []

    def ajouter_debut(self, e):
        self._elements.insert(0, e)

    def ajouter_fin(self, e):
        self._elements.append(e)

    def retirer_debut(self):
        return self._elements.pop(0)

    def retirer_fin(self):
        return self._elements.pop()

    def est_vide(self):
        return len(self._elements) == 0
```

*Barème :* 1,5 pt par méthode correcte (5 méthodes = 7,5 pts) + 0,5 pt pour l'initialisation correcte dans `__init__`. Toute implémentation alternative correcte et fonctionnelle (par exemple avec `collections.deque`) est acceptée avec le même barème.

---

**Barème global : 7 + 5 + 8 = 20 points.**
