# Chapitre 2 — Types construits : p-uplets, tableaux, dictionnaires
## Fiche d'exercices

*Première NSI — Python 3*

---

### Exercice 1 — P-uplets et déballage

1. Écrire une fonction `distance(p1, p2)` qui prend deux points sous forme de tuples `(x, y)` et renvoie la distance euclidienne entre eux (on utilisera le déballage pour récupérer `x1, y1` et `x2, y2`).
2. Vérifier que `distance((0, 0), (3, 4))` renvoie `5.0`.
3. Écrire une fonction `milieu(p1, p2)` qui renvoie le point milieu de deux points, sous forme d'un tuple `(x, y)`.

### Exercice 2 — P-uplets nommés

On définit :
```python
from collections import namedtuple
Etudiant = namedtuple('Etudiant', ['nom', 'moyenne'])
```

1. Créer une liste de 3 `Etudiant` de votre choix.
2. En utilisant la fonction native `max` avec le paramètre `key`, écrire une expression qui renvoie l'étudiant ayant la meilleure moyenne.
3. Pourquoi un p-uplet nommé est-il préférable à un simple dictionnaire `{"nom": ..., "moyenne": ...}` dans ce contexte, où chaque étudiant possède exactement les mêmes deux champs ?

### Exercice 3 — Matrices

1. Écrire une fonction `somme_matrices(a, b)` qui renvoie la matrice somme de deux matrices `a` et `b` de mêmes dimensions (on utilisera une compréhension de liste imbriquée).
2. Vérifier avec `a = [[1,2],[3,4]]` et `b = [[5,6],[7,8]]` que le résultat est `[[6,8],[10,12]]`.
3. Écrire une fonction `produit_matrices(a, b)` qui calcule le produit matriciel de `a` (de dimensions `n×p`) et `b` (de dimensions `p×m`), en suivant la formule : l'élément en ligne `i`, colonne `j` du résultat vaut la somme, pour `k` de `0` à `p-1`, de `a[i][k] * b[k][j]`.
4. Vérifier que le produit de `[[1,2],[3,4]]` par `[[5,6],[7,8]]` donne `[[19,22],[43,50]]`.

### Exercice 4 — Dictionnaires

1. Écrire une fonction `compter_mots(texte)` qui prend une chaîne de caractères et renvoie un dictionnaire associant chaque mot (en minuscules) à son nombre d'occurrences (indication : `texte.lower().split()` découpe le texte en mots ; la méthode `.get(cle, 0)` permet d'obtenir 0 si la clé n'existe pas encore).
2. Vérifier que `compter_mots("le chat mange le chat dort")` renvoie `{"le": 2, "chat": 2, "mange": 1, "dort": 1}`.
3. En utilisant l'opérateur de fusion `{**d1, **d2}`, fusionner les dictionnaires `d1 = {"a": 1, "b": 2}` et `d2 = {"b": 3, "c": 4}`. Quelle valeur obtient-on pour la clé `"b"` ? Pourquoi ?

---

## Corrigés

### Exercice 1

1-2.
```python
def distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return ((x2 - x1)**2 + (y2 - y1)**2) ** 0.5

distance((0, 0), (3, 4))   # 5.0
```
3.
```python
def milieu(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return ((x1 + x2) / 2, (y1 + y2) / 2)
```

### Exercice 2

1.
```python
etudiants = [
    Etudiant("Alice", 15.2),
    Etudiant("Bob", 12.8),
    Etudiant("Chloé", 17.5),
]
```
2.
```python
meilleur = max(etudiants, key=lambda e: e.moyenne)
# Etudiant(nom='Chloé', moyenne=17.5)
```
3. Un p-uplet nommé est plus adapté ici car la structure des données (exactement deux champs, `nom` et `moyenne`, présents pour chaque étudiant) est **fixe et connue à l'avance** : on gagne en lisibilité (`e.moyenne` plutôt que `e["moyenne"]`), tout en garantissant que chaque `Etudiant` possède bien tous les champs attendus, contrairement à un dictionnaire où rien n'empêcherait d'oublier une clé pour l'un des étudiants.

### Exercice 3

1-2.
```python
def somme_matrices(a, b):
    lignes = len(a)
    colonnes = len(a[0])
    return [[a[i][j] + b[i][j] for j in range(colonnes)] for i in range(lignes)]

somme_matrices([[1,2],[3,4]], [[5,6],[7,8]])   # [[6, 8], [10, 12]]
```
3-4.
```python
def produit_matrices(a, b):
    n = len(a)
    p = len(b)
    m = len(b[0])
    resultat = [[0] * m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            resultat[i][j] = sum(a[i][k] * b[k][j] for k in range(p))
    return resultat

produit_matrices([[1,2],[3,4]], [[5,6],[7,8]])   # [[19, 22], [43, 50]]
```

### Exercice 4

1-2.
```python
def compter_mots(texte):
    mots = texte.lower().split()
    compte = {}
    for mot in mots:
        compte[mot] = compte.get(mot, 0) + 1
    return compte

compter_mots("le chat mange le chat dort")
# {'le': 2, 'chat': 2, 'mange': 1, 'dort': 1}
```
3. `{**d1, **d2}` donne `{"a": 1, "b": 3, "c": 4}`. Pour la clé `"b"`, on obtient `3` (la valeur venant de `d2`), car lorsqu'une même clé apparaît plusieurs fois lors de la fusion, c'est la **dernière** valeur rencontrée (celle du dictionnaire placé le plus à droite) qui l'emporte.
