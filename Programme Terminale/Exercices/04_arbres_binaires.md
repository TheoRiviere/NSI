# Chapitre 4 — Arbres binaires
## Fiche d'exercices

*Terminale NSI — Python 3*

---

### Exercice 1 — Vocabulaire

On donne l'arbre suivant :

```
        5
       / \
      2   9
     /   / \
    1   7   12
```

1. Quelle est la racine de cet arbre ?
2. Quelles sont ses feuilles ?
3. Donner la taille et la hauteur de cet arbre.
4. Quel est le sous-arbre droit de la racine ?
5. Cet arbre est-il un arbre binaire de recherche ? Justifier.

### Exercice 2 — Construire l'arbre en Python

En utilisant la classe `NoeudArbre` du cours, écrire les lignes de code Python qui construisent l'arbre de l'exercice 1.

### Exercice 3 — Parcours à la main

Pour l'arbre de l'exercice 1, donner, **sans exécuter de code**, le résultat des parcours suivants :
1. Parcours préfixe.
2. Parcours infixe.
3. Parcours suffixe.
4. Parcours en largeur.

### Exercice 4 — Compter les feuilles

Écrire une fonction récursive `compter_feuilles(arbre)` qui renvoie le nombre de feuilles d'un arbre binaire.

### Exercice 5 — Somme des valeurs

Écrire une fonction récursive `somme_arbre(arbre)` qui renvoie la somme des valeurs de tous les nœuds d'un arbre binaire d'entiers (renvoyer `0` pour un arbre vide).

### Exercice 6 — Arbre miroir

Écrire une fonction récursive `miroir(arbre)` qui renvoie un **nouvel** arbre, symétrique de `arbre` (les sous-arbres gauche et droit sont échangés à chaque nœud), sans modifier l'arbre d'origine.

### Exercice 7 — Recherche du minimum dans un ABR

Sans utiliser `parcours_infixe`, écrire une fonction `minimum(arbre)` qui renvoie la plus petite valeur d'un arbre binaire de recherche **non vide**, en utilisant la propriété des ABR (indication : dans un ABR, la plus petite valeur se trouve tout en bas à gauche).

### Exercice 8 — Hauteur équilibrée ?

Écrire une fonction `est_equilibre(arbre)` qui renvoie `True` si, pour **chaque** nœud de l'arbre, la différence de hauteur entre son sous-arbre gauche et son sous-arbre droit est au plus 1 (on pourra s'appuyer sur la fonction `hauteur` du cours, en acceptant une solution de coût non optimal).

---

## Corrigés

### Exercice 1

1. La racine est `5`.
2. Les feuilles sont `1`, `7`, `12`.
3. Taille = 6 nœuds. Hauteur = 2 (chemin `5 → 9 → 7` ou `5 → 9 → 12`, de longueur 2).
4. Le sous-arbre droit de la racine est l'arbre enraciné en `9`, avec `7` à gauche et `12` à droite.
5. Oui : en chaque nœud, toutes les valeurs à gauche sont plus petites et toutes celles à droite sont plus grandes (`2 < 5 < 9` ; `1 < 2` ; `7 < 9 < 12`).

### Exercice 2

```python
class NoeudArbre:
    def __init__(self, valeur, gauche=None, droit=None):
        self.valeur = valeur
        self.gauche = gauche
        self.droit = droit

arbre = NoeudArbre(5,
            NoeudArbre(2, NoeudArbre(1)),
            NoeudArbre(9, NoeudArbre(7), NoeudArbre(12)))
```

### Exercice 3

1. Préfixe : `5, 2, 1, 9, 7, 12`
2. Infixe : `1, 2, 5, 7, 9, 12`
3. Suffixe : `1, 2, 7, 12, 9, 5`
4. Largeur : `5, 2, 9, 1, 7, 12`

### Exercice 4

```python
def compter_feuilles(arbre):
    if arbre is None:
        return 0
    if arbre.gauche is None and arbre.droit is None:
        return 1
    return compter_feuilles(arbre.gauche) + compter_feuilles(arbre.droit)
```

### Exercice 5

```python
def somme_arbre(arbre):
    if arbre is None:
        return 0
    return arbre.valeur + somme_arbre(arbre.gauche) + somme_arbre(arbre.droit)
```

### Exercice 6

```python
def miroir(arbre):
    if arbre is None:
        return None
    return NoeudArbre(arbre.valeur, miroir(arbre.droit), miroir(arbre.gauche))
```

### Exercice 7

```python
def minimum(arbre):
    courant = arbre
    while courant.gauche is not None:
        courant = courant.gauche
    return courant.valeur
```

### Exercice 8

```python
def hauteur(arbre):
    if arbre is None:
        return -1
    return 1 + max(hauteur(arbre.gauche), hauteur(arbre.droit))

def est_equilibre(arbre):
    if arbre is None:
        return True
    difference = abs(hauteur(arbre.gauche) - hauteur(arbre.droit))
    return (difference <= 1
            and est_equilibre(arbre.gauche)
            and est_equilibre(arbre.droit))
```
