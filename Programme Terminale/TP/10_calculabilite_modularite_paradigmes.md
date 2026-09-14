# Chapitre 10 — Calculabilité, modularité, paradigmes et qualité de programmation
## TP sur machine — Modules, styles de code et traque aux bugs

*Terminale NSI — Python 3 — Durée indicative : 1h30*

---

## Objectifs

- Créer et utiliser un module Python personnel.
- Réécrire un même traitement selon les trois paradigmes vus en cours.
- Détecter et corriger des bugs dans du code fourni, à l'aide de tests.

---

## Partie A — Créer un module

**A.1.** Créer un fichier `conversions.py` contenant des fonctions de conversion d'unités, chacune documentée par une docstring : `celsius_vers_fahrenheit(temp)`, `fahrenheit_vers_celsius(temp)`, `km_vers_miles(distance)`, `miles_vers_km(distance)`.

**A.2.** Dans un second fichier, importer ce module et tester chaque fonction avec au moins deux valeurs.

**A.3.** Ajouter, en tête du fichier `conversions.py`, une docstring de module décrivant son rôle général.

---

## Partie B — Un même problème, trois paradigmes

On veut, à partir d'une liste de notes sur 20, obtenir la liste des notes converties sur 100, en ne gardant que celles qui sont supérieures ou égales à 10/20.

**B.1.** Écrire une solution en style **impératif** (boucle `for`, variable accumulatrice).

**B.2.** Écrire une solution en style **fonctionnel** (`filter`, `map`, sans boucle explicite ni variable modifiée).

**B.3.** Écrire une solution en style **objet** : une classe `Bulletin` qui stocke une liste de notes et propose une méthode `notes_converties_admises()`.

**B.4.** Vérifier que les trois solutions donnent exactement le même résultat sur un même jeu de notes.

---

## Partie C — Traque aux bugs

On donne le code suivant, qui contient **quatre bugs** distincts (un de chaque type vu en cours, ou presque) :

```python
def analyser(notes):
    if len(notes) > 0:
        moyenne = sum(notes) / len(notes)
    mention = ""
    if moyenne >= 16:
        mention = "Très bien"
    elif moyenne >= 14:
        mention = "Bien"
    elif moyenne >= 12:
        mention = "Assez bien"
    return moyenne, mention

def note_maximale(notes):
    maximum = notes[0]
    for i in range(1, len(notes) + 1):
        if notes[i] > maximum:
            maximum = notes[i]
    return maximum

def a_la_moyenne(note):
    return note - 10 == 0.0
```

**C.1.** Exécuter `analyser([])` : quelle erreur obtient-on, et pourquoi ?

**C.2.** Exécuter `analyser([10, 11])` : quel est le problème (moins visible qu'une erreur, mais tout aussi réel) ?

**C.3.** Exécuter `note_maximale([12, 15, 9])` : quelle erreur obtient-on, et pourquoi ?

**C.4.** Une note est obtenue en additionnant cent fois le bonus `0.1` à une base : `note = sum([0.1] * 100)` (qui devrait mathématiquement valoir exactement `10.0`). Exécuter `a_la_moyenne(sum([0.1] * 100))` avec la version du cours (`return note - 10 == 0.0`) et expliquer le résultat obtenu.

**C.5.** Corriger le code pour éliminer ces quatre problèmes, puis écrire un petit jeu de tests (avec `assert`) qui les couvre.

---

## Corrigé indicatif

```python
# --- Partie B ---
def notes_converties_impératif(notes):
    resultat = []
    for note in notes:
        if note >= 10:
            resultat.append(note * 5)
    return resultat

def notes_converties_fonctionnel(notes):
    return list(map(lambda n: n * 5, filter(lambda n: n >= 10, notes)))

class Bulletin:
    def __init__(self, notes):
        self.notes = notes

    def notes_converties_admises(self):
        return [note * 5 for note in self.notes if note >= 10]


# --- Partie C : version corrigée ---
def analyser(notes):
    if len(notes) == 0:
        return None, "aucune note"
    moyenne = sum(notes) / len(notes)
    if moyenne >= 16:
        mention = "Très bien"
    elif moyenne >= 14:
        mention = "Bien"
    elif moyenne >= 12:
        mention = "Assez bien"
    else:
        mention = "sans mention particulière"
    return moyenne, mention

def note_maximale(notes):
    maximum = notes[0]
    for i in range(1, len(notes)):
        if notes[i] > maximum:
            maximum = notes[i]
    return maximum

def a_la_moyenne(note):
    return abs(note - 10) < 1e-9


# Jeu de tests
assert analyser([]) == (None, "aucune note")
assert analyser([10, 11])[1] == "sans mention particulière"
assert analyser([17, 18])[1] == "Très bien"
assert note_maximale([12, 15, 9]) == 15
assert a_la_moyenne(sum([0.1] * 100)) == True
assert a_la_moyenne(11) == False
print("Tous les tests passent.")
```

**C.1.** `UnboundLocalError` : pour une liste vide, la variable `moyenne` n'est jamais affectée (instruction conditionnelle non exhaustive), mais elle est utilisée juste après.

**C.2.** Pour `[10, 11]`, la moyenne vaut 10,5, ce qui ne correspond à aucune des trois conditions (`>= 16`, `>= 14`, `>= 12`) : `mention` reste une chaîne vide `""`, silencieusement, sans erreur — un bug d'autant plus dangereux qu'il ne se voit pas immédiatement.

**C.3.** `IndexError` : la boucle va jusqu'à `range(1, len(notes) + 1)`, ce qui fait que `notes[i]` est évalué pour `i = len(notes)`, un indice hors limites (débordement de tableau).

**C.4.** `sum([0.1] * 100)` ne vaut pas exactement `10.0` en représentation flottante binaire (chaque addition de `0.1` — un nombre qui n'a pas d'écriture binaire finie exacte — introduit une minuscule erreur d'arrondi, qui s'accumule sur cent additions), donc `note - 10 == 0.0` renvoie `False` avec la version non corrigée du cours, alors que mathématiquement le résultat attendu est bien 10. La version corrigée avec `abs(note - 10) < 1e-9` tolère cette imprécision et renvoie correctement `True`.
