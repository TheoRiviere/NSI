# Chapitre 3 — Traitement de données en tables
## Évaluation

*Première NSI — Durée : 55 min — Barème sur 20 points*

---

On donne la table suivante, représentant le stock d'un magasin de fournitures :

```python
table = [
    {"produit": "Cahier", "categorie": "Papeterie", "prix": 2.5, "stock": 120},
    {"produit": "Stylo", "categorie": "Papeterie", "prix": 1.0, "stock": 300},
    {"produit": "Calculatrice", "categorie": "Electronique", "prix": 15.0, "stock": 40},
    {"produit": "Clé USB", "categorie": "Electronique", "prix": 8.0, "stock": 60},
]
```

---

### Partie 1 — Questions de cours (6 points)

**Question 1 (2 pts).** Pourquoi représente-t-on souvent une table de données par une **liste de dictionnaires** en Python plutôt que, par exemple, par une liste de listes ?

**Question 2 (2 pts).** Lorsqu'on lit un fichier CSV avec `csv.DictReader`, quel est le type Python de toutes les valeurs obtenues ? Pourquoi faut-il souvent les convertir avant de faire des calculs ?

**Question 3 (2 pts).** Expliquer l'intérêt de construire un **index** (dictionnaire valeur → lignes) avant d'effectuer une fusion (jointure) entre deux tables, plutôt que d'utiliser directement deux boucles imbriquées.

---

### Partie 2 — Manipulations (8 points)

**Question 4 (2 pts).** Écrire l'expression qui sélectionne les produits de la catégorie `"Electronique"` (à l'aide d'une compréhension de liste ou de la fonction `selectionner` du cours).

**Question 5 (3 pts).** Écrire une fonction `valeur_totale_stock(table)` qui calcule la valeur totale de tout le stock (somme, pour chaque produit, de `prix × stock`).

**Question 6 (3 pts).** Vérifier (en détaillant le calcul) que `valeur_totale_stock(table)` renvoie `1680.0`.

---

### Partie 3 — Écrire du code (6 points)

**Question 7 (3 pts).** Écrire une fonction `trier_par_prix(table, decroissant=False)` qui renvoie la table triée par prix (croissant par défaut).

**Question 8 (3 pts).** Écrire une fonction `valeur_stock_par_categorie(table)` qui renvoie un dictionnaire associant à chaque catégorie la valeur totale du stock de cette catégorie (indication : on pourra indexer la table par catégorie, puis calculer la somme pour chaque groupe).

---

## Corrigé et barème détaillé

### Partie 1 (6 pts)

**Q1 (2 pts)** — Une liste de dictionnaires permet d'accéder à chaque valeur par un **nom de colonne explicite** (`ligne["prix"]`) plutôt que par un indice numérique (`ligne[2]`), ce qui rend le code beaucoup plus lisible et moins sujet aux erreurs si l'ordre des colonnes change.

**Q2 (2 pts)** — Toutes les valeurs obtenues via `csv.DictReader` sont des **chaînes de caractères** (`str`), y compris celles qui représentent des nombres (1 pt). Il faut les convertir explicitement (avec `int(...)` ou `float(...)`) avant tout calcul, sinon des opérations comme l'addition seraient interprétées comme des concaténations de chaînes, ou provoqueraient une erreur (1 pt).

**Q3 (2 pts)** — Sans index, fusionner deux tables avec deux boucles imbriquées nécessite, pour chaque ligne de la première table, de reparcourir **toute** la seconde table à la recherche d'une correspondance (1 pt). En construisant d'abord un index (dictionnaire valeur de clé → lignes), on peut retrouver directement les lignes correspondantes par un simple accès au dictionnaire, ce qui est beaucoup plus efficace, surtout pour de grandes tables (1 pt).

### Partie 2 (8 pts)

**Q4 (2 pts)**
```python
[ligne for ligne in table if ligne["categorie"] == "Electronique"]
# Calculatrice, Clé USB
```

**Q5 (3 pts)**
```python
def valeur_totale_stock(table):
    return sum(ligne["prix"] * ligne["stock"] for ligne in table)
```

**Q6 (3 pts)** — `2.5×120 + 1.0×300 + 15.0×40 + 8.0×60 = 300 + 300 + 600 + 480 = 1680.0`. *(1 pt par terme correctement calculé jusqu'à 3 pts, avec le total exact.)*

### Partie 3 (6 pts)

**Q7 (3 pts)**
```python
def trier_par_prix(table, decroissant=False):
    return sorted(table, key=lambda ligne: ligne["prix"], reverse=decroissant)
```

**Q8 (3 pts)**
```python
def valeur_stock_par_categorie(table):
    index = {}
    for ligne in table:
        index.setdefault(ligne["categorie"], []).append(ligne)
    return {
        categorie: sum(ligne["prix"] * ligne["stock"] for ligne in lignes)
        for categorie, lignes in index.items()
    }
# {'Papeterie': 600.0, 'Electronique': 1080.0}
```
*(2 pts pour le regroupement correct par catégorie, 1 pt pour le calcul de la valeur par groupe.)*

---

**Barème global : 6 + 8 + 6 = 20 points.**
