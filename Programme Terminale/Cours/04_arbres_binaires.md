# Terminale NSI — Chapitre 4
# Arbres binaires : structures et algorithmes

*Support de cours — Python 3*

---

## Objectifs du chapitre

- Connaître le vocabulaire des arbres binaires (nœud, racine, feuille, sous-arbre).
- Calculer la taille et la hauteur d'un arbre binaire.
- Parcourir un arbre binaire (infixe, préfixe, suffixe, en largeur).
- Rechercher et insérer une clé dans un arbre binaire de recherche.

**Prérequis :** récursivité de base (première NSI), classes (chapitre 1).

---

## 4.1 Vocabulaire

Un **arbre binaire** est une structure hiérarchique où chaque **nœud** possède au plus deux enfants : un **sous-arbre gauche** et un **sous-arbre droit**.

- La **racine** est le nœud du sommet, qui n'a pas de parent.
- Une **feuille** est un nœud sans aucun enfant.
- Un nœud sans sous-arbre gauche (ou droit) a un sous-arbre gauche (ou droit) **vide**, noté `None` en Python.

```
        8
       / \
      3   10
     / \    \
    1   6    14
       / \   /
      4   7 13
```

Ici, `8` est la racine ; `1`, `4`, `7`, `13` sont des feuilles ; le sous-arbre gauche de `8` est enraciné en `3`.

### Implémentation en Python

```python
class NoeudArbre:
    def __init__(self, valeur, gauche=None, droit=None):
        self.valeur = valeur
        self.gauche = gauche
        self.droit = droit
```

Un arbre est simplement représenté par une référence vers son nœud racine (`None` pour un arbre vide) :

```python
arbre = NoeudArbre(8,
            NoeudArbre(3,
                NoeudArbre(1),
                NoeudArbre(6, NoeudArbre(4), NoeudArbre(7))),
            NoeudArbre(10,
                None,
                NoeudArbre(14, NoeudArbre(13))))
```

---

## 4.2 Taille et hauteur

- La **taille** d'un arbre est son nombre total de nœuds.
- La **hauteur** d'un arbre est la longueur du plus long chemin de la racine à une feuille (un arbre vide a une hauteur de -1 par convention ; une feuille seule a une hauteur de 0).

```python
def taille(arbre):
    if arbre is None:
        return 0
    return 1 + taille(arbre.gauche) + taille(arbre.droit)

def hauteur(arbre):
    if arbre is None:
        return -1
    return 1 + max(hauteur(arbre.gauche), hauteur(arbre.droit))
```

> **Remarque.** Un arbre binaire de hauteur `h` contient au maximum `2^(h+1) - 1` nœuds. Inversement, un arbre de `n` nœuds a une hauteur d'au moins `log₂(n+1) - 1`. Cet encadrement est essentiel pour comprendre pourquoi les arbres bien équilibrés permettent des recherches rapides (voir 4.4).

---

## 4.3 Parcours d'un arbre binaire

Parcourir un arbre, c'est visiter chacun de ses nœuds selon un certain ordre. On distingue quatre parcours classiques.

### Parcours en profondeur (récursifs)

| Parcours | Ordre de visite | Principe |
|---|---|---|
| **Préfixe** | racine, gauche, droite | on traite la racine avant ses sous-arbres |
| **Infixe** | gauche, racine, droite | on traite la racine entre ses deux sous-arbres |
| **Suffixe** | gauche, droite, racine | on traite la racine après ses sous-arbres |

```python
def parcours_prefixe(arbre, resultat=None):
    if resultat is None:
        resultat = []
    if arbre is not None:
        resultat.append(arbre.valeur)
        parcours_prefixe(arbre.gauche, resultat)
        parcours_prefixe(arbre.droit, resultat)
    return resultat

def parcours_infixe(arbre, resultat=None):
    if resultat is None:
        resultat = []
    if arbre is not None:
        parcours_infixe(arbre.gauche, resultat)
        resultat.append(arbre.valeur)
        parcours_infixe(arbre.droit, resultat)
    return resultat

def parcours_suffixe(arbre, resultat=None):
    if resultat is None:
        resultat = []
    if arbre is not None:
        parcours_suffixe(arbre.gauche, resultat)
        parcours_suffixe(arbre.droit, resultat)
        resultat.append(arbre.valeur)
    return resultat
```

Sur l'arbre de l'exemple : `parcours_prefixe` donne `[8, 3, 1, 6, 4, 7, 10, 14, 13]`, `parcours_infixe` donne `[1, 3, 4, 6, 7, 8, 10, 13, 14]`, `parcours_suffixe` donne `[1, 4, 7, 6, 3, 13, 14, 10, 8]`.

> **Remarque importante.** Sur un **arbre binaire de recherche** (voir 4.4), le parcours infixe donne toujours les valeurs **triées par ordre croissant** — c'est une propriété très utile.

### Parcours en largeur

Le **parcours en largeur** (ou *BFS*, *Breadth-First Search*) visite les nœuds niveau par niveau, de gauche à droite. On l'implémente avec une **file** (chapitre 3) :

```python
def parcours_largeur(arbre):
    if arbre is None:
        return []
    resultat = []
    file = [arbre]           # on utilise une simple liste Python comme file
    while len(file) > 0:
        noeud = file.pop(0)
        resultat.append(noeud.valeur)
        if noeud.gauche is not None:
            file.append(noeud.gauche)
        if noeud.droit is not None:
            file.append(noeud.droit)
    return resultat
```

Sur l'arbre de l'exemple, ce parcours donne `[8, 3, 10, 1, 6, 14, 4, 7, 13]`.

---

## 4.4 Arbres binaires de recherche (ABR)

Un **arbre binaire de recherche** est un arbre binaire qui respecte, en **chaque** nœud, la propriété suivante :

> toutes les valeurs du sous-arbre **gauche** sont **strictement inférieures** à la valeur du nœud, et toutes les valeurs du sous-arbre **droit** lui sont **strictement supérieures**.

L'arbre de l'exemple en 4.1 est un ABR.

### Recherche d'une clé

```python
def rechercher(arbre, cle):
    if arbre is None:
        return False
    if cle == arbre.valeur:
        return True
    elif cle < arbre.valeur:
        return rechercher(arbre.gauche, cle)
    else:
        return rechercher(arbre.droit, cle)
```

À chaque étape, on élimine tout un sous-arbre : si l'arbre est **équilibré** (hauteur proche de `log₂(n)`), la recherche a un coût **logarithmique**, bien meilleur que le coût linéaire d'une recherche dans une liste.

### Insertion d'une clé

```python
def inserer(arbre, cle):
    if arbre is None:
        return NoeudArbre(cle)
    if cle < arbre.valeur:
        arbre.gauche = inserer(arbre.gauche, cle)
    elif cle > arbre.valeur:
        arbre.droit = inserer(arbre.droit, cle)
    # si cle == arbre.valeur, on ne fait rien (pas de doublon)
    return arbre
```

**Exemple d'utilisation :**

```python
racine = None
for valeur in [8, 3, 10, 1, 6, 14, 4, 7, 13]:
    racine = inserer(racine, valeur)

print(rechercher(racine, 6))    # True
print(rechercher(racine, 9))    # False
print(parcours_infixe(racine))  # [1, 3, 4, 6, 7, 8, 10, 13, 14] : triée !
```

---

## 4.5 Synthèse

| Notion | Définition |
|---|---|
| Nœud / racine / feuille | Élément d'un arbre / nœud sans parent / nœud sans enfant |
| Sous-arbre gauche / droit | Arbre binaire attaché à gauche (resp. à droite) d'un nœud |
| Taille | Nombre total de nœuds d'un arbre |
| Hauteur | Longueur du plus long chemin racine → feuille |
| Parcours préfixe / infixe / suffixe | Trois ordres de visite récursifs, selon la position de la racine par rapport à ses sous-arbres |
| Parcours en largeur | Visite niveau par niveau, à l'aide d'une file |
| ABR | Arbre binaire où, en chaque nœud, gauche < nœud < droit ; recherche/insertion en coût logarithmique si l'arbre est équilibré |

*Prochaine étape suggérée : chapitre 5, les graphes, qui généralisent encore la notion de structure hiérarchique à des structures relationnelles quelconques.*
