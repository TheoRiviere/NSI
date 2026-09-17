# Chapitre 8 — Langages, spécification et mise au point de programmes
## TP sur machine — Chasse aux bugs

*Première NSI — Python 3 — Durée indicative : 1h30 à 2h*

---

## Objectifs

- Mettre en pratique une démarche méthodique de débogage (test, isolement, correction, revérification).
- Rencontrer trois catégories classiques de bugs en Python.
- Écrire des jeux de tests permettant de détecter ces bugs.

---

## Partie A — Un bug d'inversion de condition

```python
def est_pair_buggue(n):
    if n % 2 == 1:
        return True
    return False
```

**A.1.** Écrire une fonction `tester_est_pair(fonction_a_tester)` qui prend en paramètre une fonction (par exemple `est_pair_buggue`) et vérifie, à l'aide d'une série d'`assert`, qu'elle se comporte correctement sur plusieurs cas : `4` (pair), `7` (impair), `0` (pair), `-4` (pair), `-3` (impair).

**A.2.** Exécuter ce test sur `est_pair_buggue`. Sur quel(s) cas échoue-t-il ? Identifier précisément l'erreur dans le code.

**A.3.** Corriger la fonction (en `est_pair_correct`), et vérifier que `tester_est_pair(est_pair_correct)` réussit intégralement.

---

## Partie B — Un bug d'indexation (off-by-one)

```python
def compter_voyelles_buggue(mot):
    voyelles = "aeiouAEIOU"
    compte = 0
    for i in range(len(mot) - 1):
        if mot[i] in voyelles:
            compte += 1
    return compte
```

**B.1.** Tester `compter_voyelles_buggue("banana")`. Le résultat attendu est `3` (les trois `a`). Que renvoie réellement la fonction ?

**B.2.** Pourquoi ce bug ne se manifeste-t-il **pas** avec un mot comme `"xyz"` (aucune voyelle) ? Et pourquoi se manifeste-t-il avec `"banana"` mais serait resté invisible avec un mot ne se terminant pas par une voyelle, comme `"ananas"` ? (Réfléchir précisément à quelle lettre n'est jamais testée par la boucle.)

**B.3.** Corriger la fonction (en `compter_voyelles_correct`), en utilisant de préférence un parcours direct des caractères (`for lettre in mot:`) plutôt qu'un parcours par indice, pour éviter ce type d'erreur.

**B.4.** Écrire un jeu de tests couvrant au moins 4 cas (dont un mot sans voyelle, et un mot se terminant par une voyelle) pour `compter_voyelles_correct`.

---

## Partie C — Un piège classique de Python : l'argument par défaut mutable

```python
def ajouter_note_buggue(note, notes=[]):
    notes.append(note)
    return notes
```

Cette fonction est censée ajouter une note à une liste (créée vide par défaut si aucune n'est fournie), et renvoyer cette liste.

**C.1.** Exécuter le code suivant et observer attentivement le résultat :
```python
r1 = ajouter_note_buggue(10)
r2 = ajouter_note_buggue(12)
print(r1)
print(r2)
```
Le résultat vous surprend-il ? `r2` devrait-il, intuitivement, contenir uniquement `[12]` ?

**C.2.** Ce comportement est un piège très classique et bien documenté de Python : une valeur par défaut d'un paramètre (ici, la liste `[]`) n'est créée **qu'une seule fois**, au moment où la fonction est définie, et non à chaque appel. Toutes les invocations de `ajouter_note_buggue` qui n'indiquent pas explicitement `notes` **partagent donc la même liste**, qui continue d'accumuler des éléments d'un appel à l'autre.

Corriger la fonction en utilisant la technique standard pour éviter ce piège : le paramètre par défaut doit être `None`, et une nouvelle liste vide doit être créée **à l'intérieur** de la fonction si aucune liste n'a été fournie.

**C.3.** Vérifier que, avec la version corrigée, deux appels successifs sans argument `notes` donnent bien des listes indépendantes (`[10]` puis `[12]`, et non `[10]` puis `[10, 12]`).

---

## Corrigé indicatif

```python
# --- Partie A ---
def est_pair_buggue(n):
    if n % 2 == 1:
        return True
    return False

def tester_est_pair(fonction_a_tester):
    cas_de_test = [(4, True), (7, False), (0, True), (-4, True), (-3, False)]
    for entree, attendu in cas_de_test:
        resultat = fonction_a_tester(entree)
        statut = "OK" if resultat == attendu else "ÉCHEC"
        print(f"{statut} : {fonction_a_tester.__name__}({entree}) = {resultat} (attendu {attendu})")

tester_est_pair(est_pair_buggue)
# On observe que TOUS les cas échouent : la condition est inversée
# (n % 2 == 1 signifie "n est impair", pas "n est pair")

def est_pair_correct(n):
    return n % 2 == 0

tester_est_pair(est_pair_correct)   # tous les tests réussissent


# --- Partie B ---
def compter_voyelles_buggue(mot):
    voyelles = "aeiouAEIOU"
    compte = 0
    for i in range(len(mot) - 1):
        if mot[i] in voyelles:
            compte += 1
    return compte

print(compter_voyelles_buggue("banana"))   # 2 au lieu de 3 !
# La boucle range(len(mot) - 1) s'arrête un indice trop tôt :
# elle ne teste jamais le DERNIER caractère du mot.
# Avec "xyz", le dernier caractère ('z') n'est pas une voyelle,
# donc l'oubli ne change rien au résultat : le bug reste invisible.
# Avec "banana", le dernier caractère est justement un 'a' (une voyelle) :
# il est ignoré à tort, d'où un résultat trop petit de 1.

def compter_voyelles_correct(mot):
    voyelles = "aeiouAEIOU"
    compte = 0
    for lettre in mot:
        if lettre in voyelles:
            compte += 1
    return compte

def tester_compter_voyelles():
    cas_de_test = [("banana", 3), ("xyz", 0), ("aeiou", 5), ("Python", 1)]
    for entree, attendu in cas_de_test:
        resultat = compter_voyelles_correct(entree)
        assert resultat == attendu, f"échec pour {entree} : attendu {attendu}, obtenu {resultat}"
    print("compter_voyelles_correct : tous les tests réussis")

tester_compter_voyelles()


# --- Partie C ---
def ajouter_note_buggue(note, notes=[]):
    notes.append(note)
    return notes

r1 = ajouter_note_buggue(10)
r2 = ajouter_note_buggue(12)
print(r1)   # [10, 12]  <- surprenant !
print(r2)   # [10, 12]  <- les deux appels partagent la MÊME liste

def ajouter_note_correcte(note, notes=None):
    if notes is None:
        notes = []
    notes.append(note)
    return notes

r3 = ajouter_note_correcte(10)
r4 = ajouter_note_correcte(12)
assert r3 == [10]
assert r4 == [12]
print(r3, r4)   # [10] [12]  <- comportement attendu
```

**Leçon générale de ce TP :** ces trois bugs illustrent des catégories très différentes d'erreurs — une erreur de **logique** (condition inversée), une erreur d'**indexation** (bornes de boucle), et un piège spécifique au **fonctionnement du langage** lui-même (évaluation des valeurs par défaut). Un jeu de tests bien construit, couvrant des cas variés (y compris des cas limites), est souvent le meilleur moyen de détecter ce type d'erreurs avant qu'elles ne causent des problèmes plus difficiles à diagnostiquer dans un programme plus grand.
