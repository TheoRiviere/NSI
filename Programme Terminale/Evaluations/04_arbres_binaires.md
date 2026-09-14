# Chapitre 4 — Arbres binaires
## Évaluation

*Terminale NSI — Durée : 55 min — Barème sur 20 points*

---

### Partie 1 — Questions de cours (6 points)

On donne l'arbre suivant :

```
        6
       / \
      3   8
     / \    \
    1   4    9
```

**Question 1 (3 pts).** Donner : la racine, la liste des feuilles, la taille, la hauteur de cet arbre.

**Question 2 (1 pt).** Cet arbre est-il un arbre binaire de recherche ? Justifier en une phrase.

**Question 3 (2 pts).** Donner le résultat du parcours infixe, puis du parcours en largeur de cet arbre.

---

### Partie 2 — Écrire des fonctions récursives (8 points)

On rappelle la classe :
```python
class NoeudArbre:
    def __init__(self, valeur, gauche=None, droit=None):
        self.valeur = valeur
        self.gauche = gauche
        self.droit = droit
```

**Question 4 (4 pts).** Écrire une fonction récursive `profondeur_max_valeur(arbre)` qui renvoie la plus grande valeur contenue dans un arbre binaire d'entiers **non vide** (on ne suppose **pas** qu'il s'agit d'un ABR : il faut examiner tous les nœuds).

**Question 5 (4 pts).** Écrire une fonction récursive `contient(arbre, valeur)` qui renvoie `True` si `valeur` apparaît dans l'arbre, `False` sinon (là encore, on ne suppose pas que l'arbre est un ABR : il faut chercher dans tout l'arbre).

---

### Partie 3 — Arbre binaire de recherche (6 points)

**Question 6 (6 pts).** On insère, dans cet ordre, les valeurs `15, 6, 18, 3, 7, 17, 20` dans un arbre binaire de recherche initialement vide, à l'aide de la fonction `inserer` du cours.

a) (3 pts) Dessiner (ou décrire précisément, niveau par niveau) l'arbre obtenu.
b) (2 pts) Donner le résultat du parcours infixe de cet arbre.
c) (1 pt) Quelle est la hauteur de cet arbre ?

---

## Corrigé et barème détaillé

### Partie 1 (6 pts)

**Q1 (3 pts, 0,75 pt/item)** — Racine : `6`. Feuilles : `1`, `4`, `9`. Taille : `6`. Hauteur : `2`.

**Q2 (1 pt)** — Oui : en chaque nœud, toutes les valeurs du sous-arbre gauche lui sont inférieures et toutes celles du sous-arbre droit lui sont supérieures (`1 < 3 < 4 < 6 < 8 < 9`, et la propriété se vérifie nœud par nœud : `1 < 3 < 4` autour de `3`, `8 < 9` à droite de `6`).

**Q3 (2 pts, 1 pt/parcours)** — Infixe : `1, 3, 4, 6, 8, 9`. Largeur : `6, 3, 8, 1, 4, 9`.

### Partie 2 (8 pts)

**Q4 (4 pts)**
```python
def profondeur_max_valeur(arbre):
    maximum = arbre.valeur
    if arbre.gauche is not None:
        maximum = max(maximum, profondeur_max_valeur(arbre.gauche))
    if arbre.droit is not None:
        maximum = max(maximum, profondeur_max_valeur(arbre.droit))
    return maximum
```
*(1 pt cas de base implicite correct ; 1,5 pt traitement du sous-arbre gauche ; 1,5 pt traitement du sous-arbre droit.)*

**Q5 (4 pts)**
```python
def contient(arbre, valeur):
    if arbre is None:
        return False
    if arbre.valeur == valeur:
        return True
    return contient(arbre.gauche, valeur) or contient(arbre.droit, valeur)
```
*(1 pt cas de base (arbre vide) ; 1 pt cas trouvé ; 2 pts appel récursif correct sur les deux sous-arbres avec `or`.)*

### Partie 3 (6 pts)

**Q6a (3 pts)**
```
            15
           /  \
          6    18
         / \   / \
        3   7 17  20
```

**Q6b (2 pts)** — Parcours infixe : `3, 6, 7, 15, 17, 18, 20` (toujours trié, propriété de l'ABR).

**Q6c (1 pt)** — Hauteur : `2`.

---

**Barème global : 6 + 8 + 6 = 20 points.**
