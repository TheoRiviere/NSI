# Terminale NSI — Chapitre 10
# Calculabilité, modularité, paradigmes et qualité de programmation

*Support de cours — Python 3*

---

## Objectifs du chapitre

- Comprendre l'idée qu'un programme peut être considéré comme une donnée.
- Comprendre, sans formalisme, pourquoi le problème de l'arrêt est indécidable.
- Utiliser et créer des modules, exploiter une documentation.
- Distinguer les paradigmes impératif, fonctionnel et objet.
- Reconnaître et corriger les causes typiques de bugs.

---

## 10.1 Le programme en tant que donnée

Un programme, une fois écrit, est avant tout une suite de caractères — donc une **donnée**, comme n'importe quel texte. C'est ce qui permet à d'autres programmes de le manipuler :

- un **interpréteur** (comme celui de Python) lit le code source et l'exécute ;
- un **compilateur** traduit le code source vers un autre langage (souvent plus bas niveau) ;
- un logiciel de **téléchargement** ou d'**installation** manipule des programmes comme de simples fichiers, sans les exécuter ;
- un système d'exploitation charge un programme (une donnée stockée sur le disque) en mémoire pour l'exécuter.

```python
code_source = "print(2 + 3)"
exec(code_source)   # le système exécute une chaîne de caractères comme un programme
```

Cette idée — qu'un programme peut être manipulé comme une donnée par un autre programme — est au fondement de l'informatique moderne (et historiquement, de la notion de machine universelle introduite par Turing en 1936).

---

## 10.2 Calculabilité et décidabilité

Un problème est dit **calculable** (ou **décidable**, lorsqu'il s'agit d'une question à réponse oui/non) s'il existe un algorithme qui, pour toute entrée, se termine et fournit la réponse correcte.

Un résultat fondamental de l'informatique théorique est que **certains problèmes ne sont pas calculables**, quel que soit le langage de programmation utilisé (la calculabilité ne dépend pas du langage).

### Le problème de l'arrêt

**Énoncé.** Existe-t-il un programme `arret(P, entree)` qui, pour **tout** programme `P` et toute entrée `entree`, détermine si l'exécution de `P` sur `entree` se termine (renvoie `True`) ou boucle indéfiniment (renvoie `False`) — et ce, **sans jamais lui-même se lancer dans une boucle infinie** ?

**Réponse : non.** On peut le montrer par un raisonnement par l'absurde, sans formalisme théorique poussé.

**Argument informel.** Supposons qu'un tel programme `arret(P, entree)` existe. Construisons alors le programme suivant :

```python
def paradoxe(P):
    if arret(P, P):      # on teste si P s'arrête... quand on lui donne lui-même en entrée
        while True:       # si oui, on boucle exprès indéfiniment
            pass
    else:
        return "je m'arrête"   # si non, on s'arrête
```

Posons-nous alors la question : `paradoxe(paradoxe)` s'arrête-t-il ?

- Si `arret(paradoxe, paradoxe)` renvoie `True` (c'est-à-dire que `paradoxe(paradoxe)` devrait s'arrêter), alors, par définition de `paradoxe`, celui-ci **boucle indéfiniment** — contradiction.
- Si `arret(paradoxe, paradoxe)` renvoie `False` (c'est-à-dire que `paradoxe(paradoxe)` ne devrait pas s'arrêter), alors, par définition de `paradoxe`, celui-ci **s'arrête** immédiatement — contradiction.

Dans les deux cas, on obtient une contradiction : l'hypothèse de départ (l'existence de `arret`) est donc fausse. **Le problème de l'arrêt est indécidable.**

> **Portée de ce résultat.** Ce résultat signifie qu'aucun outil ne pourra jamais, de façon totalement automatique et infaillible, prédire si n'importe quel programme se termine sur n'importe quelle entrée. C'est une limite fondamentale, indépendante des progrès technologiques ou de la puissance de calcul disponible.

---

## 10.3 Modularité

La **modularité** consiste à découper un programme en unités indépendantes et réutilisables (des **modules**), chacune ayant un rôle précis, et à s'appuyer sur des modules déjà écrits plutôt que de tout redévelopper.

### Utiliser une API ou une bibliothèque

```python
import math

print(math.sqrt(16))     # utilise une fonction déjà écrite, sans connaître son implémentation
print(math.pi)
```

Une **API** (*Application Programming Interface*) est l'ensemble des fonctions, classes et constantes qu'un module met à disposition — on retrouve ici l'idée d'**interface** vue au chapitre 2 : on utilise `math.sqrt` sans savoir comment la racine carrée est calculée en interne.

> **Bonne pratique.** Avant d'utiliser une bibliothèque, on consulte sa **documentation**, qui décrit précisément l'interface de chaque fonction (paramètres attendus, valeur renvoyée, exceptions possibles) — c'est l'équivalent, pour un module, de la spécification vue au chapitre 2.

### Créer son propre module

Un fichier Python peut lui-même être importé comme un module. Par exemple, dans un fichier `geometrie.py` :

```python
# fichier geometrie.py
"""Module de fonctions géométriques simples."""

def aire_rectangle(largeur, hauteur):
    """Renvoie l'aire d'un rectangle de dimensions largeur x hauteur."""
    return largeur * hauteur

def aire_cercle(rayon):
    """Renvoie l'aire d'un cercle de rayon donné (approximation avec pi = 3.14)."""
    return 3.14 * rayon ** 2
```

Ce module peut ensuite être utilisé depuis un autre fichier :

```python
import geometrie

print(geometrie.aire_rectangle(3, 4))
print(geometrie.aire_cercle(2))
```

Documenter chaque fonction (avec une *docstring*, entre triples guillemets) permet à quiconque utilise le module de connaître son interface sans lire son code.

---

## 10.4 Paradigmes de programmation

Un **paradigme de programmation** est une façon d'organiser et de structurer un programme. On en distingue trois principaux au programme de terminale.

### Paradigme impératif

On décrit une **suite d'instructions** qui modifient l'état du programme (des variables) au fil de leur exécution.

```python
total = 0
for x in [1, 2, 3, 4, 5]:
    total = total + x
print(total)
```

### Paradigme fonctionnel

On décrit le résultat comme la **composition de fonctions**, en évitant autant que possible de modifier un état (pas de boucle avec variable modifiée, on préfère la récursivité et les fonctions comme `map`, `filter`).

```python
from functools import reduce

total = reduce(lambda a, b: a + b, [1, 2, 3, 4, 5])
print(total)

carres = list(map(lambda x: x ** 2, [1, 2, 3, 4, 5]))
print(carres)
```

### Paradigme objet

On organise le programme autour d'**objets** qui regroupent données et comportements (voir chapitre 1).

```python
class Somme:
    def __init__(self):
        self.total = 0

    def ajouter(self, x):
        self.total += x

s = Somme()
for x in [1, 2, 3, 4, 5]:
    s.ajouter(x)
print(s.total)
```

Ces trois extraits calculent la **même chose** (la somme de `[1, 2, 3, 4, 5]`), avec le **même langage** (Python, qui autorise les trois paradigmes), mais des styles très différents. Le choix d'un paradigme dépend du problème à résoudre, des habitudes de l'équipe, et des bibliothèques disponibles.

---

## 10.5 Mise au point des programmes : causes typiques de bugs

| Cause de bug | Exemple erroné | Correction |
|---|---|---|
| Problème de typage | `"3" + 5` (`TypeError`) | `int("3") + 5` |
| Effet de bord non désiré | une fonction modifie une liste passée en paramètre sans que l'appelant s'y attende | documenter clairement si une fonction modifie ses arguments, ou travailler sur une copie |
| Débordement dans un tableau | `tableau[len(tableau)]` (`IndexError`) | utiliser `tableau[len(tableau) - 1]` pour le dernier élément, ou `tableau[-1]` |
| Instruction conditionnelle non exhaustive | un `if`/`elif` qui oublie un cas possible, laissant une variable non définie | ajouter un `else` explicite, ou vérifier tous les cas possibles |
| Mauvais choix d'inégalité | `if x =< 10` (erreur de syntaxe) ou confusion `<` / `<=` aux bornes | relire attentivement les conditions aux limites (tests aux bornes) |
| Comparaison de flottants | `0.1 + 0.2 == 0.3` (renvoie `False` à cause des arrondis) | comparer `abs(a - b) < 1e-9` plutôt que `a == b` |
| Mauvais nommage de variables | `l = [1, 2, 3]` (confusion possible avec le chiffre 1), noms trop proches (`somme` et `somme2`) | choisir des noms clairs, explicites et bien distincts |

```python
# Illustration : comparaison de flottants
print(0.1 + 0.2 == 0.3)               # False, à cause des arrondis binaires !
print(abs((0.1 + 0.2) - 0.3) < 1e-9)  # True : comparaison correcte
```

> **Anticiper les bugs.** Au-delà de la correction ponctuelle, il s'agit de développer une vigilance systématique : tester les cas limites (tableau vide, valeur nulle, valeur négative), vérifier le typage des entrées, et documenter précisément le comportement attendu d'une fonction (ce qui rejoint la notion de spécification et de jeux de tests, vue en première).

---

## 10.6 Synthèse

| Notion | Définition |
|---|---|
| Programme comme donnée | Un programme est une suite de caractères manipulable par d'autres programmes (interpréteur, compilateur...) |
| Calculabilité / décidabilité | Existence d'un algorithme qui résout un problème, en s'arrêtant, pour toute entrée |
| Problème de l'arrêt | Problème indécidable : aucun algorithme ne peut toujours prédire si un programme donné termine |
| Modularité | Découpage d'un programme en unités réutilisables (modules), utilisées via leur API |
| Paradigme impératif / fonctionnel / objet | Trois façons différentes de structurer un même programme |

*Prochaine étape suggérée : chapitre 11, les bases de données relationnelles et le langage SQL.*
