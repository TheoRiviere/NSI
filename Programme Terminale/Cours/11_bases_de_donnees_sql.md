# Terminale NSI — Chapitre 11
# Bases de données relationnelles et langage SQL

*Support de cours — SQL (SQLite) et Python 3*

---

## Objectifs du chapitre

- Connaître le vocabulaire du modèle relationnel.
- Distinguer la structure d'une base de données de son contenu, repérer des anomalies.
- Comprendre le rôle d'un système de gestion de bases de données (SGBD).
- Écrire des requêtes SQL d'interrogation et de mise à jour.

---

## 11.1 Le modèle relationnel

Une base de données relationnelle organise l'information en **relations** (que l'on appelle aussi **tables**). Chaque relation est composée :

- d'**attributs** (les colonnes), chacun associé à un **domaine** (l'ensemble des valeurs qu'il peut prendre : entiers, texte, dates...) ;
- de **n-uplets** (les lignes), chacun représentant une occurrence concrète de la relation.

On identifie chaque n-uplet de façon unique grâce à une **clé primaire** (un ou plusieurs attributs dont la valeur ne se répète jamais dans la table). Une **clé étrangère** est un attribut d'une table qui référence la clé primaire d'une autre table, ce qui permet de relier les tables entre elles.

### Exemple de schéma relationnel

```
Eleves(id, nom, prenom, classe)
Notes(id, eleve_id, matiere, note)
```

Ici, `id` est la clé primaire de `Eleves` ; `eleve_id`, dans `Notes`, est une **clé étrangère** qui référence `Eleves.id` : chaque note est ainsi rattachée à un élève précis.

| id | nom | prenom | classe |
|---|---|---|---|
| 1 | Lovelace | Ada | TNSI1 |
| 2 | Turing | Alan | TNSI1 |
| 3 | Hopper | Grace | TNSI2 |
| 4 | Curie | Marie | TNSI2 |

| id | eleve_id | matiere | note |
|---|---|---|---|
| 1 | 1 | NSI | 16 |
| 2 | 1 | Maths | 14 |
| 3 | 2 | NSI | 18 |
| 4 | 2 | Maths | 12 |
| 5 | 3 | NSI | 9 |
| 6 | 3 | Maths | 15 |
| 7 | 4 | NSI | 17 |

---

## 11.2 Structure et contenu, anomalies

La **structure** d'une base de données (son schéma relationnel) est indépendante de son **contenu** (les données qu'elle stocke à un instant donné) : on peut modifier le contenu (ajouter, supprimer des lignes) sans changer la structure.

Une base de données **mal conçue** peut présenter des **anomalies** :

- **redondance** : une même information répétée inutilement dans plusieurs lignes (par exemple, si l'on stockait le nom du professeur de chaque matière directement dans la table `Notes`, répété à chaque ligne) ;
- **anomalie de mise à jour** : en cas de redondance, une modification doit être répercutée partout, au risque d'incohérences si on l'oublie quelque part ;
- **anomalie d'insertion / de suppression** : impossibilité d'enregistrer une information isolée, ou perte d'information non désirée lors d'une suppression.

> **Pourquoi séparer `Eleves` et `Notes` ?** Si l'on stockait le nom et le prénom de chaque élève directement dans la table `Notes` (une ligne par note), ces informations seraient répétées à chaque note d'un même élève : une redondance, source d'anomalies si le nom d'un élève doit être corrigé (il faudrait le faire sur toutes ses lignes de notes). Séparer les deux tables, reliées par une clé étrangère, élimine cette redondance.

---

## 11.3 Le système de gestion de bases de données (SGBD)

Un **SGBD** (comme SQLite, PostgreSQL, MySQL...) est le logiciel qui gère une base de données relationnelle. Il rend notamment les services suivants :

- **persistance des données** : les données restent disponibles après l'arrêt des programmes qui les utilisent (stockage sur disque) ;
- **gestion des accès concurrents** : plusieurs utilisateurs ou programmes peuvent lire et modifier la base simultanément, sans se corrompre mutuellement les données ;
- **efficacité du traitement des requêtes** : le SGBD optimise l'exécution des requêtes (notamment via des index), même sur des bases volumineuses ;
- **sécurisation des accès** : gestion des droits (qui peut lire, modifier, quelles tables).

---

## 11.4 Le langage SQL — requêtes d'interrogation

On utilise ici SQLite, un SGBD léger utilisable directement depuis Python via le module `sqlite3`.

### SELECT ... FROM ... WHERE

```sql
SELECT nom, prenom FROM Eleves WHERE classe = 'TNSI1';
```
Résultat : `Lovelace, Ada` et `Turing, Alan`.

### DISTINCT

```sql
SELECT DISTINCT classe FROM Eleves;
```
Résultat : `TNSI1`, `TNSI2` (chaque valeur n'apparaît qu'une fois, même si plusieurs élèves partagent la même classe).

### ORDER BY

```sql
SELECT Eleves.nom, Notes.note
FROM Eleves JOIN Notes ON Eleves.id = Notes.eleve_id
WHERE matiere = 'NSI'
ORDER BY note DESC;
```
Résultat, trié par note décroissante : `Turing (18)`, `Curie (17)`, `Lovelace (16)`, `Hopper (9)`.

### Les fonctions d'agrégation

```sql
SELECT AVG(note) FROM Notes WHERE matiere = 'NSI';   -- moyenne : 15.0
SELECT MAX(note), MIN(note) FROM Notes WHERE matiere = 'Maths';  -- 15.0, 12.0
SELECT COUNT(*) FROM Eleves WHERE classe = 'TNSI2';   -- 2
```

### La jointure (JOIN)

La clause `JOIN ... ON ...` permet de combiner des lignes de deux tables lorsqu'une condition (typiquement, l'égalité entre une clé étrangère et la clé primaire référencée) est vérifiée.

```sql
SELECT Eleves.nom, Eleves.prenom, Notes.matiere, Notes.note
FROM Eleves JOIN Notes ON Eleves.id = Notes.eleve_id
WHERE Eleves.classe = 'TNSI1';
```
Résultat :
```
Lovelace, Ada, NSI, 16
Lovelace, Ada, Maths, 14
Turing, Alan, NSI, 18
Turing, Alan, Maths, 12
```

Sans jointure, il serait impossible d'obtenir directement le nom d'un élève associé à chacune de ses notes : cette information est répartie entre les deux tables, précisément pour éviter la redondance vue en 11.2.

---

## 11.5 Le langage SQL — requêtes de mise à jour

### INSERT

```sql
INSERT INTO Eleves VALUES (5, 'Babbage', 'Charles', 'TNSI1');
```
Ajoute une nouvelle ligne à la table `Eleves`.

### UPDATE

```sql
UPDATE Notes SET note = note + 1 WHERE matiere = 'NSI';
```
Augmente d'un point toutes les notes de NSI.

### DELETE

```sql
DELETE FROM Notes WHERE note < 10;
```
Supprime toutes les lignes dont la note est strictement inférieure à 10.

---

## 11.6 Utiliser SQL depuis Python

```python
import sqlite3

connexion = sqlite3.connect("ecole.db")
curseur = connexion.cursor()

curseur.execute("SELECT nom, prenom FROM Eleves WHERE classe = ?", ("TNSI1",))
for ligne in curseur.fetchall():
    print(ligne)

connexion.commit()   # valide les modifications (INSERT / UPDATE / DELETE)
connexion.close()
```

> **Sécurité.** On utilise un `?` comme paramètre substitué (plutôt que de construire la requête par concaténation de chaînes) pour éviter les **injections SQL**, une faille où un utilisateur malveillant insérerait du code SQL non désiré via une saisie de texte.

---

## 11.7 Synthèse

| Notion | Définition |
|---|---|
| Relation (table) | Ensemble structuré de n-uplets (lignes), organisés en attributs (colonnes) |
| Clé primaire | Attribut(s) identifiant chaque n-uplet de façon unique |
| Clé étrangère | Attribut référençant la clé primaire d'une autre table, pour relier les données |
| SGBD | Logiciel assurant persistance, accès concurrents, efficacité et sécurité |
| `SELECT` / `WHERE` / `ORDER BY` | Sélectionner, filtrer, trier des données |
| `JOIN` | Combiner des lignes de plusieurs tables selon une condition |
| `INSERT` / `UPDATE` / `DELETE` | Ajouter, modifier, supprimer des données |

*Prochaine étape suggérée : chapitre 12, les architectures matérielles, systèmes d'exploitation et réseaux, dernier chapitre du programme.*
