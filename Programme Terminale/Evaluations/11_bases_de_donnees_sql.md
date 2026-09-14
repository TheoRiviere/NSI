# Chapitre 11 — Bases de données relationnelles et SQL
## Évaluation

*Terminale NSI — Durée : 55 min — Barème sur 20 points*

---

On donne le schéma relationnel suivant, pour un club sportif :

```
Adherents(id, nom, prenom, section)
Cotisations(id, adherent_id, montant, annee)
```

| id | nom | prenom | section |
|---|---|---|---|
| 1 | Diallo | Fatou | Natation |
| 2 | Martin | Léo | Tennis |
| 3 | Nguyen | Minh | Natation |
| 4 | Petit | Sarah | Tennis |

| id | adherent_id | montant | annee |
|---|---|---|---|
| 1 | 1 | 120 | 2024 |
| 2 | 2 | 150 | 2024 |
| 3 | 1 | 130 | 2025 |
| 4 | 3 | 120 | 2025 |
| 5 | 4 | 150 | 2025 |

---

### Partie 1 — Questions de cours (6 points)

**Question 1 (2 pts).** Identifier la clé primaire et la clé étrangère de ce schéma.

**Question 2 (2 pts).** Pourquoi ne pas avoir stocké directement le nom et le prénom de l'adhérent dans la table `Cotisations` ? Quel principe cela illustre-t-il ?

**Question 3 (2 pts).** Citer deux services rendus par un SGBD.

---

### Partie 2 — Écrire des requêtes SQL (10 points)

**Question 4 (2 pts).** Écrire la requête qui affiche le nom et le prénom de tous les adhérents de la section `"Natation"`.

**Question 5 (2 pts).** Écrire la requête qui affiche toutes les cotisations de l'année `2025`, triées par montant décroissant.

**Question 6 (2 pts).** Écrire la requête qui calcule le montant total des cotisations perçues en `2025`.

**Question 7 (4 pts).** Écrire la requête, utilisant une jointure, qui affiche le nom, le prénom et le montant de chaque cotisation payée en `2025`.

---

### Partie 3 — Mise à jour (4 points)

**Question 8 (4 pts).** Écrire les trois requêtes SQL qui : ajoutent un nouvel adhérent `(5, "Roche", "Emma", "Tennis")` ; changent la section de l'adhérent `"Nguyen"` en `"Tennis"` ; suppriment toutes les cotisations de l'année `2024`.

---

## Corrigé et barème détaillé

### Partie 1 (6 pts)

**Q1 (2 pts)** — Clé primaire : `id` (dans chacune des deux tables). Clé étrangère : `adherent_id` dans `Cotisations`, qui référence `Adherents.id`.

**Q2 (2 pts)** — Pour éviter la **redondance** : le nom et le prénom d'un adhérent seraient répétés sur chacune de ses lignes de cotisation. Cela illustre le principe de séparation des données selon ce dont elles dépendent réellement (ici, le nom dépend de l'adhérent, pas de chaque cotisation), afin d'éviter les anomalies de mise à jour.

**Q3 (2 pts, 1 pt/service parmi)** — Persistance des données ; gestion des accès concurrents ; efficacité du traitement des requêtes ; sécurisation des accès.

### Partie 2 (10 pts)

**Q4 (2 pts)**
```sql
SELECT nom, prenom FROM Adherents WHERE section = 'Natation';
```

**Q5 (2 pts)**
```sql
SELECT * FROM Cotisations WHERE annee = 2025 ORDER BY montant DESC;
```

**Q6 (2 pts)**
```sql
SELECT SUM(montant) FROM Cotisations WHERE annee = 2025;
```

**Q7 (4 pts)**
```sql
SELECT Adherents.nom, Adherents.prenom, Cotisations.montant
FROM Adherents JOIN Cotisations ON Adherents.id = Cotisations.adherent_id
WHERE Cotisations.annee = 2025;
```
*(2 pts jointure correcte, 2 pts sélection et filtre corrects.)*

### Partie 3 (4 pts)

**Q8 (4 pts, environ 1,3 pt/requête)**
```sql
INSERT INTO Adherents VALUES (5, 'Roche', 'Emma', 'Tennis');

UPDATE Adherents SET section = 'Tennis' WHERE nom = 'Nguyen';

DELETE FROM Cotisations WHERE annee = 2024;
```

---

**Barème global : 6 + 10 + 4 = 20 points.**
