# Chapitre 11 — Bases de données relationnelles et SQL
## Fiche d'exercices

*Terminale NSI — SQL*

---

On travaille sur la base de données du cours :

```
Eleves(id, nom, prenom, classe)
Notes(id, eleve_id, matiere, note)
```

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

### Exercice 1 — Vocabulaire

1. Quelle est la clé primaire de `Eleves` ? de `Notes` ?
2. Quelle est la clé étrangère de `Notes`, et vers quelle table pointe-t-elle ?
3. Combien d'attributs possède la table `Notes` ?

### Exercice 2 — Requêtes simples

Écrire les requêtes SQL permettant d'obtenir :
1. Le nom et le prénom de tous les élèves de la classe `TNSI2`.
2. Toutes les notes de la matière `"Maths"`, triées par ordre décroissant.
3. Le nombre total d'élèves enregistrés dans la base.

### Exercice 3 — Agrégation

Écrire les requêtes SQL permettant d'obtenir :
1. La moyenne de toutes les notes de la table `Notes`, toutes matières confondues.
2. La meilleure note obtenue en `"NSI"`.
3. Le nombre de notes strictement inférieures à 10.

### Exercice 4 — Jointures

Écrire la requête SQL qui affiche le nom, le prénom et la note de tous les élèves ayant obtenu une note strictement inférieure à `10`, quelle que soit la matière.

### Exercice 5 — Mise à jour

1. Écrire la requête SQL qui ajoute un nouvel élève `(5, "Babbage", "Charles", "TNSI2")`.
2. Écrire la requête SQL qui change la classe de l'élève `"Hopper"` en `"TNSI1"`.
3. Écrire la requête SQL qui supprime toutes les notes de la matière `"Maths"`.

### Exercice 6 — Anomalies

On propose la table unique suivante, censée remplacer `Eleves` et `Notes` :

```
NotesUniques(nom_eleve, prenom_eleve, classe_eleve, matiere, note)
```

1. Quelle anomalie ce schéma introduit-il par rapport au schéma en deux tables du cours ?
2. Donner un exemple concret de problème que cela peut causer si un élève change de classe en cours d'année.

---

## Corrigés

### Exercice 1

1. La clé primaire de `Eleves` est `id`. Celle de `Notes` est `id` (celui de la table `Notes`, un identifiant propre à chaque note).
2. `eleve_id` est la clé étrangère de `Notes`, elle référence `Eleves.id`.
3. 4 attributs (`id`, `eleve_id`, `matiere`, `note`).

### Exercice 2

```sql
SELECT nom, prenom FROM Eleves WHERE classe = 'TNSI2';

SELECT * FROM Notes WHERE matiere = 'Maths' ORDER BY note DESC;

SELECT COUNT(*) FROM Eleves;
```

### Exercice 3

```sql
SELECT AVG(note) FROM Notes;

SELECT MAX(note) FROM Notes WHERE matiere = 'NSI';

SELECT COUNT(*) FROM Notes WHERE note < 10;
```

### Exercice 4

```sql
SELECT Eleves.nom, Eleves.prenom, Notes.note
FROM Eleves JOIN Notes ON Eleves.id = Notes.eleve_id
WHERE Notes.note < 10;
```

### Exercice 5

```sql
INSERT INTO Eleves VALUES (5, 'Babbage', 'Charles', 'TNSI2');

UPDATE Eleves SET classe = 'TNSI1' WHERE nom = 'Hopper';

DELETE FROM Notes WHERE matiere = 'Maths';
```

### Exercice 6

1. Ce schéma réintroduit une **redondance** : le nom, le prénom et la classe d'un élève sont répétés sur chacune de ses lignes de notes (autant de fois qu'il a de notes), alors qu'ils ne dépendent que de l'élève, pas de chaque note.
2. Si un élève change de classe, il faut modifier **toutes ses lignes** dans `NotesUniques` (une par note) ; si l'on en oublie ne serait-ce qu'une seule, la base devient incohérente : un même élève apparaîtrait avec deux classes différentes selon les lignes consultées — c'est exactement l'anomalie de mise à jour évoquée en cours.
