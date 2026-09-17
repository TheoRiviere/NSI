# Chapitre 8 — Langages, spécification et mise au point de programmes
## Fiche d'exercices

*Première NSI — Python 3*

---

### Exercice 1 — Écrire une spécification

1. Écrire la docstring (précondition + postcondition) d'une fonction `valeur_absolue(x)` qui renvoie la valeur absolue de `x`.
2. Implémenter cette fonction.
3. Écrire une fonction de test `tester_valeur_absolue()` couvrant au moins : un nombre positif, un nombre négatif, zéro, et un nombre flottant.

### Exercice 2 — Trouver et corriger un bug

On donne la fonction suivante, censée renvoyer le plus grand élément d'une liste non vide :
```python
def maximum_buggue(liste):
    maximum = 0
    for x in liste:
        if x > maximum:
            maximum = x
    return maximum
```

1. Tester cette fonction avec `maximum_buggue([-5, -2, -8])`. Le résultat obtenu est-il correct ? Pourquoi ce cas de test révèle-t-il le bug alors qu'un test avec `maximum_buggue([3, 7, 2])` ne le révélerait pas ?
2. Identifier précisément l'origine du bug.
3. Corriger la fonction (renommée `maximum_correct`), puis vérifier avec un jeu de tests couvrant à la fois des listes de nombres positifs et des listes de nombres négatifs.

### Exercice 3 — Constructions élémentaires dans différents langages

On donne le code Python suivant :
```python
total = 0
for i in range(5):
    total = total + i
print(total)
```

1. Quelles sont les constructions élémentaires utilisées dans ce programme (parmi : affectation, séquence, test, répétition, fonction) ?
2. Réécrire ce même programme en pseudo-code générique, sans utiliser de syntaxe Python spécifique (par exemple `POUR i DE 0 A 4 FAIRE ... FIN POUR`), pour montrer que la logique est indépendante du langage utilisé.

### Exercice 4 — Utiliser une bibliothèque

1. Rechercher (ou se rappeler) le nom du module Python standard permettant de calculer facilement la moyenne et la médiane d'une liste de nombres.
2. Utiliser ce module pour calculer la moyenne et la médiane de `[12, 15, 8, 17, 10]`.
3. Pourquoi est-il préférable d'utiliser une fonction de bibliothèque déjà existante (comme `statistics.mean`) plutôt que de réécrire soi-même une fonction de calcul de moyenne à chaque fois qu'on en a besoin ?

---

## Corrigés

### Exercice 1

```python
def valeur_absolue(x):
    """
    Précondition : x est un nombre (int ou float).
    Postcondition : renvoie |x|, un nombre positif ou nul.
    """
    if x < 0:
        return -x
    return x

def tester_valeur_absolue():
    cas_de_test = [(5, 5), (-5, 5), (0, 0), (-3.5, 3.5), (3.5, 3.5)]
    for entree, attendu in cas_de_test:
        resultat = valeur_absolue(entree)
        assert resultat == attendu, f"échec pour {entree}"
    print("Tous les tests ont réussi !")
```

### Exercice 2

1. `maximum_buggue([-5, -2, -8])` renvoie `0`, ce qui est **incorrect** : le plus grand élément de cette liste est `-2`. Ce test révèle le bug car tous les éléments de la liste sont négatifs, donc strictement inférieurs à la valeur initiale `0` : aucune mise à jour de `maximum` n'a jamais lieu, et la fonction renvoie sa valeur initiale erronée. Avec `[3, 7, 2]`, tous les éléments sont positifs et au moins un dépasse `0`, donc `maximum` finit par être correctement mis à jour, et le bug reste invisible malgré son existence.
2. Le bug vient du choix de la valeur initiale de `maximum` : `0` n'est pas nécessairement une valeur présente ou inférieure à tous les éléments de la liste (ce n'est vrai que si la liste contient au moins un nombre positif ou nul).
3.
```python
def maximum_correct(liste):
    maximum = liste[0]
    for x in liste[1:]:
        if x > maximum:
            maximum = x
    return maximum

def tester_maximum():
    assert maximum_correct([-5, -2, -8]) == -2
    assert maximum_correct([3, 7, 2]) == 7
    assert maximum_correct([5]) == 5
    print("Tests réussis !")

tester_maximum()
```

### Exercice 3

1. Ce programme utilise : l'**affectation** (`total = 0`, `total = total + i`), la **séquence** (les instructions s'exécutent les unes après les autres), et la **répétition** (la boucle `for`).
2.
```
total <- 0
POUR i DE 0 A 4 FAIRE
    total <- total + i
FIN POUR
AFFICHER total
```
Cela montre que la logique de l'algorithme (accumuler une somme par répétition) est indépendante de la syntaxe précise d'un langage donné : on pourrait tout aussi bien l'écrire en C, en JavaScript ou dans tout autre langage disposant d'une boucle et d'affectations.

### Exercice 4

1. Le module `statistics` de la bibliothèque standard de Python.
2.
```python
import statistics

notes = [12, 15, 8, 17, 10]
statistics.mean(notes)     # 12.4
statistics.median(notes)   # 12
```
3. Utiliser une fonction de bibliothèque déjà existante évite de dupliquer un travail déjà fait (gain de temps), bénéficie d'une implémentation généralement déjà testée et optimisée (moins de risque de bug ou de lenteur inutile), et rend le code plus lisible pour quiconque connaît déjà cette bibliothèque standard.
