# Chapitre 8 — Langages, spécification et mise au point de programmes
## Évaluation

*Première NSI — Durée : 50 min — Barème sur 20 points*

---

### Partie 1 — Questions de cours (7 points)

**Question 1 (2 pts).** Citer trois constructions élémentaires communes à la plupart des langages de programmation.

**Question 2 (2 pts).** Qu'est-ce qu'une précondition ? Qu'est-ce qu'une postcondition ? À qui incombe la responsabilité de chacune ?

**Question 3 (3 pts).** Citer trois techniques permettant de déboguer un programme qui ne fonctionne pas comme attendu.

---

### Partie 2 — Spécification et tests (7 points)

**Question 4 (3 pts).** Écrire la spécification (précondition et postcondition, sous forme de docstring) d'une fonction `indice_maximum(liste)` qui renvoie l'indice de l'élément maximum d'une liste.

**Question 5 (4 pts).** Écrire un jeu de tests (fonction `tester_indice_maximum`) pour cette fonction, couvrant au moins 3 cas différents, dont un cas limite (par exemple une liste à un seul élément).

---

### Partie 3 — Déboguer du code (6 points)

On donne la fonction suivante, censée renvoyer le premier élément négatif d'une liste (ou `None` s'il n'y en a aucun) :
```python
def premier_negatif_buggue(liste):
    for i in range(1, len(liste)):
        if liste[i] < 0:
            return liste[i]
    return None
```

**Question 6 (2 pts).** Que renvoie `premier_negatif_buggue([-3, 5, 2])` ? Ce résultat est-il correct ? Justifier.

**Question 7 (2 pts).** Identifier précisément l'origine du bug.

**Question 8 (2 pts).** Corriger la fonction (en `premier_negatif_correct`).

---

## Corrigé et barème détaillé

### Partie 1 (7 pts)

**Q1 (2 pts, parmi)** — Affectation, séquence, test conditionnel, répétition (boucle), définition/appel de fonction. *(2/3 éléments corrects suffisent pour les 2 points.)*

**Q2 (2 pts)** — La précondition décrit ce qui doit être vrai sur les paramètres pour que la fonction fonctionne correctement ; c'est la responsabilité de celui qui **appelle** la fonction (1 pt). La postcondition décrit ce que la fonction garantit sur son résultat (si la précondition est respectée) ; c'est la responsabilité de celui qui **écrit** la fonction (1 pt).

**Q3 (3 pts, 1 pt par technique parmi)** — Lire attentivement le message d'erreur ; ajouter des affichages (`print`) temporaires pour observer l'état des variables ; isoler le problème en testant séparément une petite partie du code ; utiliser un débogueur pas à pas.

### Partie 2 (7 pts)

**Q4 (3 pts)**
```python
def indice_maximum(liste):
    """
    Précondition : liste est une liste non vide.
    Postcondition : renvoie l'indice d'un élément de valeur maximale dans liste.
    """
    ...
```
*(1,5 pt pour une précondition correcte (liste non vide), 1,5 pt pour une postcondition correcte.)*

**Q5 (4 pts)**
```python
def indice_maximum(liste):
    indice_meilleur = 0
    for i in range(1, len(liste)):
        if liste[i] > liste[indice_meilleur]:
            indice_meilleur = i
    return indice_meilleur

def tester_indice_maximum():
    assert indice_maximum([3, 7, 2]) == 1
    assert indice_maximum([5]) == 0
    assert indice_maximum([-1, -5, -2]) == 0
    print("Tests réussis !")
```
*(2 pts pour au moins 3 cas de test cohérents avec la fonction, 2 pts pour la présence d'un cas limite pertinent comme une liste à un seul élément.)*

### Partie 3 (6 pts)

**Q6 (2 pts)** — La fonction renvoie `None`, ce qui est **incorrect** : le premier élément négatif de `[-3, 5, 2]` est `-3` (à l'indice 0), mais la fonction ne le trouve pas.

**Q7 (2 pts)** — La boucle commence à `range(1, len(liste))`, donc à l'indice `1`, et **ignore complètement l'indice 0** de la liste : si le premier élément négatif se trouve précisément à cet indice, il n'est jamais examiné.

**Q8 (2 pts)**
```python
def premier_negatif_correct(liste):
    for i in range(len(liste)):
        if liste[i] < 0:
            return liste[i]
    return None
```
*(Toute solution correcte est acceptée, y compris un parcours direct `for element in liste:`.)*

---

**Barème global : 7 + 7 + 6 = 20 points.**
