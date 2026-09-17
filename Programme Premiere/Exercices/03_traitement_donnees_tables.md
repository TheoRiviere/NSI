# Chapitre 3 — Traitement de données en tables
## Fiche d'exercices

*Première NSI — Python 3*

---

On travaille tout au long de cette fiche avec la table suivante :

```python
table = [
    {"nom": "Diallo", "ville": "Lyon", "age": 17},
    {"nom": "Martin", "ville": "Paris", "age": 16},
    {"nom": "Nguyen", "ville": "Lyon", "age": 18},
    {"nom": "Petit", "ville": "Marseille", "age": 17},
]
```

### Exercice 1 — Sélection et tri

1. En utilisant `selectionner` du cours, obtenir la liste des élèves âgés de 17 ans.
2. En utilisant `trier_par` du cours, trier la table par âge **décroissant**.
3. Écrire une expression (sans nouvelle fonction) qui sélectionne les élèves de Lyon âgés de 17 ans ou plus (indication : la condition passée à `selectionner` peut combiner deux tests avec `and`).

### Exercice 2 — Statistiques sur une colonne

1. Écrire une fonction `moyenne_colonne(table, colonne)` qui calcule la moyenne des valeurs d'une colonne numérique.
2. Vérifier que `moyenne_colonne(table, "age")` renvoie `17.0`.
3. Écrire une fonction `compter_par_colonne(table, colonne)` qui renvoie un dictionnaire associant à chaque valeur distincte de la colonne le nombre de lignes correspondantes (indication : on peut réutiliser `indexer_par` du cours, puis ne garder que la longueur de chaque liste).
4. Vérifier que `compter_par_colonne(table, "ville")` renvoie `{"Lyon": 2, "Paris": 1, "Marseille": 1}`.

### Exercice 3 — Recherche dichotomique dans une table triée

Lorsqu'une table est **triée** selon une colonne, on peut y rechercher une valeur bien plus efficacement qu'avec un parcours linéaire, grâce à une recherche dichotomique (déjà vue sur des tableaux simples — voir aussi le chapitre sur l'algorithmique).

1. Trier la table par `nom` à l'aide de `trier_par`.
2. Écrire une fonction `recherche_dichotomique_table(table_triee, colonne, valeur)` qui recherche, par dichotomie, la ligne dont la colonne donnée vaut `valeur`, et renvoie cette ligne (ou `None` si elle n'existe pas). On s'inspirera de la recherche dichotomique classique sur un tableau trié.
3. Vérifier que la recherche de `"Nguyen"` renvoie bien la ligne correspondante, et que la recherche de `"Zorro"` renvoie `None`.

### Exercice 4 — Fusion de tables

On donne une seconde table :
```python
inscriptions_club = [
    {"nom": "Diallo", "club": "Échecs"},
    {"nom": "Nguyen", "club": "Théâtre"},
]
```

1. En utilisant `fusionner_tables` du cours, fusionner `table` et `inscriptions_club` sur la colonne `"nom"`.
2. Combien de lignes contient le résultat ? Pourquoi Martin et Petit n'y apparaissent-ils pas, alors qu'ils sont présents dans `table` ?
3. Modifier `fusionner_tables` en une nouvelle fonction `fusionner_tables_toutes(table1, table2, cle)` qui conserve **toutes** les lignes de `table1`, même celles qui n'ont pas de correspondance dans `table2` (dans ce cas, on pourra ajouter une colonne `"club"` avec la valeur `None`).

---

## Corrigés

### Exercice 1

1.
```python
dixsept = selectionner(table, lambda ligne: ligne["age"] == 17)
# Diallo et Petit
```
2.
```python
trier_par(table, "age", decroissant=True)
# Nguyen (18), Diallo (17), Petit (17), Martin (16)
```
3.
```python
selectionner(table, lambda ligne: ligne["ville"] == "Lyon" and ligne["age"] >= 17)
# Diallo, Nguyen
```

### Exercice 2

1-2.
```python
def moyenne_colonne(table, colonne):
    return sum(ligne[colonne] for ligne in table) / len(table)

moyenne_colonne(table, "age")   # (17+16+18+17)/4 = 17.0
```
3-4.
```python
def compter_par_colonne(table, colonne):
    index = indexer_par(table, colonne)
    return {valeur: len(lignes) for valeur, lignes in index.items()}

compter_par_colonne(table, "ville")
# {'Lyon': 2, 'Paris': 1, 'Marseille': 1}
```

### Exercice 3

1.
```python
table_triee = trier_par(table, "nom")
# Diallo, Martin, Nguyen, Petit (ordre alphabétique)
```
2.
```python
def recherche_dichotomique_table(table_triee, colonne, valeur):
    gauche, droite = 0, len(table_triee) - 1
    while gauche <= droite:
        milieu = (gauche + droite) // 2
        if table_triee[milieu][colonne] == valeur:
            return table_triee[milieu]
        elif table_triee[milieu][colonne] < valeur:
            gauche = milieu + 1
        else:
            droite = milieu - 1
    return None
```
3. `recherche_dichotomique_table(table_triee, "nom", "Nguyen")` renvoie bien la ligne de Nguyen ; `recherche_dichotomique_table(table_triee, "nom", "Zorro")` renvoie `None` car "Zorro" n'est présent dans aucune ligne.

### Exercice 4

1.
```python
fusionner_tables(table, inscriptions_club, "nom")
# [{'nom': 'Diallo', ..., 'club': 'Échecs'}, {'nom': 'Nguyen', ..., 'club': 'Théâtre'}]
```
2. Le résultat contient **2 lignes**. Martin et Petit n'y apparaissent pas car la fonction `fusionner_tables` du cours ne conserve que les lignes de `table1` dont la clé possède une correspondance dans `table2` (c'est ce qu'on appelle une jointure « interne », qui exclut les lignes sans correspondance).
3.
```python
def fusionner_tables_toutes(table1, table2, cle):
    index2 = indexer_par(table2, cle)
    resultat = []
    for ligne1 in table1:
        valeur_cle = ligne1[cle]
        if valeur_cle in index2:
            for ligne2 in index2[valeur_cle]:
                resultat.append({**ligne1, **ligne2})
        else:
            resultat.append({**ligne1, "club": None})
    return resultat
```
