# Chapitre 3 — Traitement de données en tables
## TP sur machine — Analyse d'un fichier CSV de classe

*Première NSI — Python 3 — Durée indicative : 1h30 à 2h*

---

## Objectifs

- Lire un vrai fichier CSV avec le module `csv`.
- Convertir les types de données (les valeurs lues d'un CSV sont toujours des chaînes).
- Effectuer des statistiques (sélection, tri, regroupement) sur une table.
- Écrire une nouvelle table dans un fichier CSV.

---

## Préparation

**Étape 0.** Créer, dans le même dossier que votre script, un fichier `classe.csv` contenant exactement ceci (attention à respecter les en-têtes de colonnes) :

```
nom,ville,age,moyenne
Diallo,Lyon,17,15.2
Martin,Paris,16,11.8
Nguyen,Lyon,18,17.5
Petit,Marseille,17,13.0
Roche,Paris,16,9.4
Girard,Lyon,17,14.1
```

---

## Partie A — Lecture et conversion des types

**A.1.** Écrire un script qui ouvre `classe.csv` et charge son contenu dans une liste de dictionnaires `table_brute`, à l'aide de `csv.DictReader`.

**A.2.** Afficher `table_brute[0]` et observer, en affichant `type(table_brute[0]["age"])`, que la colonne `age` est bien de type `str` et non `int`.

**A.3.** Écrire une fonction `convertir_types(table)` qui renvoie une nouvelle table où la colonne `age` est convertie en `int` et la colonne `moyenne` en `float` (les autres colonnes restant inchangées).

---

## Partie B — Statistiques sur la classe

**B.1.** Recopier `selectionner` et `trier_par` du cours.

**B.2.** À l'aide de `selectionner`, obtenir la liste des élèves « en difficulté », c'est-à-dire ayant une moyenne strictement inférieure à `10`.

**B.3.** À l'aide de `trier_par`, obtenir le classement de la classe par moyenne décroissante.

**B.4.** Calculer la moyenne générale de la classe (moyenne de la colonne `moyenne` sur toute la table).

**B.5.** Recopier `indexer_par` du cours, puis écrire une fonction `moyenne_par_groupe(table, colonne_groupe, colonne_valeur)` qui renvoie un dictionnaire associant à chaque valeur distincte de `colonne_groupe` la moyenne de `colonne_valeur` pour les lignes correspondantes (indication : réutiliser `indexer_par`).

**B.6.** Calculer la moyenne des notes par ville avec `moyenne_par_groupe(table, "ville", "moyenne")`. Quelle ville a la meilleure moyenne ?

---

## Partie C — Écriture d'un nouveau fichier CSV

**C.1.** Écrire une fonction `ecrire_csv(table, chemin, colonnes)` qui écrit la table dans un fichier CSV au chemin donné, en ne conservant que les colonnes indiquées, à l'aide de `csv.DictWriter` (penser à `writer.writeheader()` puis à `writer.writerow(...)` pour chaque ligne).

**C.2.** Utiliser cette fonction pour écrire un fichier `classement.csv` contenant uniquement les colonnes `nom` et `moyenne`, pour les élèves triés par moyenne décroissante (réutiliser le résultat de B.3).

**C.3.** Ouvrir le fichier `classement.csv` produit avec un tableur (ou l'afficher avec `print(open("classement.csv").read())`) pour vérifier son contenu.

---

## Corrigé indicatif

```python
import csv

# --- Partie A ---
with open("classe.csv", encoding="utf-8") as fichier:
    lecteur = csv.DictReader(fichier)
    table_brute = list(lecteur)

print(table_brute[0])
print(type(table_brute[0]["age"]))   # <class 'str'>

def convertir_types(table):
    resultat = []
    for ligne in table:
        nouvelle_ligne = dict(ligne)
        nouvelle_ligne["age"] = int(ligne["age"])
        nouvelle_ligne["moyenne"] = float(ligne["moyenne"])
        resultat.append(nouvelle_ligne)
    return resultat

table = convertir_types(table_brute)


# --- Partie B ---
def selectionner(table, condition):
    return [ligne for ligne in table if condition(ligne)]

def trier_par(table, colonne, decroissant=False):
    return sorted(table, key=lambda ligne: ligne[colonne], reverse=decroissant)

en_difficulte = selectionner(table, lambda ligne: ligne["moyenne"] < 10)
print("En difficulté :", [ligne["nom"] for ligne in en_difficulte])

classement = trier_par(table, "moyenne", decroissant=True)
print("Classement :", [ligne["nom"] for ligne in classement])

moyenne_generale = sum(ligne["moyenne"] for ligne in table) / len(table)
print("Moyenne générale :", moyenne_generale)

def indexer_par(table, colonne):
    index = {}
    for ligne in table:
        index.setdefault(ligne[colonne], []).append(ligne)
    return index

def moyenne_par_groupe(table, colonne_groupe, colonne_valeur):
    index = indexer_par(table, colonne_groupe)
    return {
        groupe: sum(ligne[colonne_valeur] for ligne in lignes) / len(lignes)
        for groupe, lignes in index.items()
    }

moyennes_villes = moyenne_par_groupe(table, "ville", "moyenne")
print("Moyennes par ville :", moyennes_villes)
meilleure_ville = max(moyennes_villes, key=lambda v: moyennes_villes[v])
print("Meilleure ville :", meilleure_ville)


# --- Partie C ---
def ecrire_csv(table, chemin, colonnes):
    with open(chemin, "w", newline="", encoding="utf-8") as fichier:
        writer = csv.DictWriter(fichier, fieldnames=colonnes)
        writer.writeheader()
        for ligne in table:
            writer.writerow({c: ligne[c] for c in colonnes})

ecrire_csv(classement, "classement.csv", ["nom", "moyenne"])
print(open("classement.csv", encoding="utf-8").read())
```

**Résultat attendu pour B.6 :** Lyon obtient la meilleure moyenne (environ `15.6`, contre environ `10.6` pour Paris et `13.0` pour Marseille), car ses trois élèves (Diallo, Nguyen, Girard) ont des moyennes globalement plus élevées.
