# Chapitre 10 — Calculabilité, modularité, paradigmes et qualité de programmation
## Évaluation

*Terminale NSI — Durée : 55 min — Barème sur 20 points*

---

### Partie 1 — Questions de cours (10 points)

**Question 1 (2 pts).** En quel sens peut-on dire qu'un programme est aussi une donnée ? Donner un exemple.

**Question 2 (3 pts).** Énoncer le problème de l'arrêt, et donner sa réponse (décidable ou indécidable). Cette réponse dépend-elle du langage de programmation utilisé ?

**Question 3 (2 pts).** Qu'est-ce qu'une API ? Quel lien peut-on faire avec la notion d'interface vue dans un chapitre précédent ?

**Question 4 (3 pts).** Nommer les trois paradigmes de programmation vus en cours, et donner, pour chacun, un mot-clé ou une caractéristique typique en Python.

---

### Partie 2 — Identifier des bugs (6 points)

On donne le code suivant :
```python
def categorie_age(age):
    if age < 13:
        categorie = "enfant"
    elif age < 18:
        categorie = "adolescent"
    elif age < 65:
        categorie = "adulte"
    return categorie

def premiere_lettre_majuscule(mots):
    resultat = []
    for i in range(len(mots) + 1):
        resultat.append(mots[i][0].upper())
    return resultat
```

**Question 5 (3 pts).** La fonction `categorie_age` contient un bug. Lequel ? Sur quelle entrée se manifeste-t-il, et quelle erreur Python obtient-on ?

**Question 6 (3 pts).** La fonction `premiere_lettre_majuscule` contient un bug. Lequel ? Corriger la fonction.

---

### Partie 3 — Écrire du code (4 points)

**Question 7 (4 pts).** Réécrire la fonction impérative suivante dans le style **fonctionnel**, à l'aide de `filter` et/ou `map` (sans boucle `for` ni `while`) :
```python
def mots_longs(mots):
    resultat = []
    for mot in mots:
        if len(mot) > 5:
            resultat.append(mot.upper())
    return resultat
```

---

## Corrigé et barème détaillé

### Partie 1 (10 pts)

**Q1 (2 pts)** — Un programme est une suite de caractères (du texte), qui peut donc être manipulée comme une donnée par un autre programme (1 pt). Exemple : un interpréteur lit le code source comme une donnée pour l'exécuter ; un logiciel de transfert de fichiers déplace un exécutable sans l'exécuter (1 pt).

**Q2 (3 pts)** — Le problème de l'arrêt consiste à déterminer, pour un programme et une entrée quelconques, si l'exécution de ce programme sur cette entrée se termine ou non (1 pt). Il est **indécidable** : aucun algorithme ne peut le résoudre pour tous les cas possibles (1 pt). Cette réponse ne dépend pas du langage de programmation utilisé (1 pt).

**Q3 (2 pts)** — Une API est l'ensemble des fonctions, classes et constantes qu'un module ou une bibliothèque met à disposition de ses utilisateurs (1 pt). C'est un cas particulier de la notion d'interface : elle décrit ce qu'on peut utiliser, sans révéler comment c'est implémenté (1 pt).

**Q4 (3 pts, 1 pt/paradigme)** — Impératif : boucles (`for`, `while`) et variables modifiées pas à pas. Fonctionnel : `map`, `filter`, `reduce`, fonctions lambda, récursivité, absence de modification d'état. Objet : `class`, attributs, méthodes, `self`.

### Partie 2 (6 pts)

**Q5 (3 pts)** — Instruction conditionnelle non exhaustive : pour `age >= 65`, aucune des conditions n'est vérifiée, donc `categorie` n'est jamais définie (1 pt), et l'exécution de `categorie_age(70)` par exemple lève une `UnboundLocalError` (2 pts).

**Q6 (3 pts)** — Débordement de tableau : la boucle va jusqu'à `range(len(mots) + 1)`, ce qui provoque un accès à `mots[len(mots)]`, hors limites (1 pt pour l'identification). Correction :
```python
def premiere_lettre_majuscule(mots):
    resultat = []
    for i in range(len(mots)):
        resultat.append(mots[i][0].upper())
    return resultat
```
*(2 pts pour la correction fonctionnelle.)*

### Partie 3 (4 pts)

**Q7 (4 pts)**
```python
def mots_longs(mots):
    return list(map(lambda m: m.upper(), filter(lambda m: len(m) > 5, mots)))
```
*(2 pts filtrage correct des mots longs ; 2 pts transformation en majuscules et valeur de retour sous forme de liste.)*

---

**Barème global : 10 + 6 + 4 = 20 points.**
