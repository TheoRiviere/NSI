# Chapitre 3 — Traitement de données en tables

## Objectifs

- Représenter une table de données en Python (liste de dictionnaires).
- Effectuer une indexation, une recherche (sélection), un tri et une projection sur une table.
- Fusionner deux tables à partir d'une clé commune.
- Lire un fichier au format CSV.

## Prérequis

- Tableaux (listes) et dictionnaires — chapitre 2.
- Fonction `sorted` et paramètre `key`.

---

## 1. Qu'est-ce qu'une table de données ?

Une **table** est une manière d'organiser des données structurées en lignes et en colonnes, comme un tableur ou une base de données. Chaque **ligne** représente un enregistrement (par exemple, un élève), et chaque **colonne** représente un attribut (le nom, la ville, l'âge...).

En Python, une façon naturelle de représenter une table est une **liste de dictionnaires**, où chaque dictionnaire représente une ligne, et où les clés du dictionnaire correspondent aux noms des colonnes.

```python
table = [
    {"nom": "Diallo", "ville": "Lyon", "age": 17},
    {"nom": "Martin", "ville": "Paris", "age": 16},
    {"nom": "Nguyen", "ville": "Lyon", "age": 18},
]
```

---

## 2. Le format CSV

Le format **CSV** (*Comma-Separated Values*) est un format de fichier texte très répandu pour stocker des tables : la première ligne contient les noms des colonnes, et chaque ligne suivante contient les valeurs correspondantes, séparées par des virgules (ou parfois des points-virgules).

```
nom,ville,age
Diallo,Lyon,17
Martin,Paris,16
```

Le module `csv` de Python permet de lire facilement un tel fichier et de le transformer directement en liste de dictionnaires grâce à `csv.DictReader` :

```python
import csv

with open("eleves.csv", encoding="utf-8") as fichier:
    lecteur = csv.DictReader(fichier)
    table = list(lecteur)
```

**Point de vigilance :** toutes les valeurs lues depuis un fichier CSV sont des **chaînes de caractères**, même celles qui représentent des nombres. Il faut donc penser à les convertir explicitement si l'on veut effectuer des calculs (par exemple avec `int(ligne["age"])`).

---

## 3. Sélection (recherche par condition)

Sélectionner des lignes vérifiant une condition, c'est en réalité un simple **filtrage** de liste, comme on l'a déjà pratiqué avec les compréhensions de liste.

```python
def selectionner(table, condition):
    """Renvoie les lignes de la table qui vérifient la condition (une fonction)."""
    return [ligne for ligne in table if condition(ligne)]

lyonnais = selectionner(table, lambda ligne: ligne["ville"] == "Lyon")
```

---

## 4. Projection (sélection de colonnes)

Projeter une table sur certaines colonnes consiste à ne conserver, pour chaque ligne, que certaines clés du dictionnaire.

```python
def projeter(table, colonnes):
    """Renvoie la table restreinte aux colonnes données."""
    return [{c: ligne[c] for c in colonnes} for ligne in table]

projeter(table, ["nom", "age"])
# [{'nom': 'Diallo', 'age': 17}, {'nom': 'Martin', 'age': 16}, {'nom': 'Nguyen', 'age': 18}]
```

---

## 5. Tri d'une table

On utilise la fonction native `sorted`, avec le paramètre `key` pour indiquer selon quelle colonne trier.

```python
def trier_par(table, colonne, decroissant=False):
    return sorted(table, key=lambda ligne: ligne[colonne], reverse=decroissant)

trier_par(table, "age")
# trié par age croissant : Martin (16), Diallo (17), Nguyen (18)
```

---

## 6. Indexation

Lorsqu'une table est volumineuse et que l'on doit rechercher fréquemment des lignes à partir de la valeur d'une même colonne, il est intéressant de construire un **index** : un dictionnaire qui associe directement à chaque valeur de cette colonne la (ou les) ligne(s) correspondante(s), pour éviter de reparcourir toute la table à chaque recherche.

```python
def indexer_par(table, colonne):
    """Construit un dictionnaire {valeur_de_colonne: [lignes correspondantes]}."""
    index = {}
    for ligne in table:
        valeur = ligne[colonne]
        index.setdefault(valeur, []).append(ligne)
    return index

index_ville = indexer_par(table, "ville")
index_ville["Lyon"]   # [{'nom': 'Diallo', ...}, {'nom': 'Nguyen', ...}]
```

`dict.setdefault(cle, valeur_par_defaut)` renvoie la valeur associée à `cle` si elle existe déjà, sinon elle l'initialise avec `valeur_par_defaut` (ici une liste vide) avant de la renvoyer — cela permet de construire progressivement des listes de valeurs associées à chaque clé, sans avoir à tester explicitement si la clé existe déjà.

Une fois l'index construit, rechercher toutes les lignes correspondant à une valeur donnée se fait en temps constant (`index_ville["Lyon"]`), au lieu de reparcourir toute la table (ce qui serait nécessaire avec `selectionner`).

---

## 7. Fusion de deux tables (jointure)

Fusionner deux tables consiste à **combiner** les lignes de deux tables qui partagent une valeur commune sur une colonne servant de clé (par exemple, fusionner une table d'élèves avec une table de leurs notes, en utilisant le nom comme clé commune).

```python
notes = [
    {"nom": "Diallo", "matiere": "NSI", "note": 15},
    {"nom": "Martin", "matiere": "NSI", "note": 12},
    {"nom": "Nguyen", "matiere": "NSI", "note": 18},
]

def fusionner_tables(table1, table2, cle):
    """Fusionne deux tables sur la colonne cle (jointure)."""
    index2 = indexer_par(table2, cle)
    resultat = []
    for ligne1 in table1:
        valeur_cle = ligne1[cle]
        if valeur_cle in index2:
            for ligne2 in index2[valeur_cle]:
                resultat.append({**ligne1, **ligne2})   # fusionne les deux dictionnaires
    return resultat

fusionner_tables(table, notes, "nom")
# [{'nom': 'Diallo', 'ville': 'Lyon', 'age': 17, 'matiere': 'NSI', 'note': 15}, ...]
```

**Remarque sur l'efficacité :** on aurait pu écrire une version naïve de cette fusion avec deux boucles imbriquées (pour chaque ligne de `table1`, parcourir toutes les lignes de `table2` à la recherche d'une valeur de clé correspondante), mais cette approche serait beaucoup plus coûteuse pour de grandes tables. En construisant d'abord un **index** de `table2`, on ramène la recherche d'une correspondance à un simple accès par clé dans un dictionnaire, ce qui est bien plus efficace.

---

## Synthèse

| Opération | Principe | Fonction Python type |
|---|---|---|
| Lecture CSV | fichier texte → liste de dictionnaires | `csv.DictReader` |
| Sélection | filtrer les lignes selon une condition | compréhension de liste avec `if` |
| Projection | ne garder que certaines colonnes | compréhension de dictionnaire |
| Tri | ordonner les lignes selon une colonne | `sorted(table, key=...)` |
| Indexation | dictionnaire valeur → lignes, pour accès rapide | `dict.setdefault` |
| Fusion (jointure) | combiner deux tables sur une clé commune | indexation + parcours |

*Prochaine étape suggérée : Chapitre 4 — Interactions Homme-Machine sur le Web.*
