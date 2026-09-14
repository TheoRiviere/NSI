# Chapitre 11 — Bases de données relationnelles et SQL
## TP sur machine — Gérer une médiathèque avec SQLite

*Terminale NSI — Python 3 (module `sqlite3`) — Durée indicative : 1h30 à 2h*

---

## Objectifs

- Créer une base de données SQLite avec plusieurs tables liées.
- Écrire des requêtes d'interrogation et de mise à jour.
- Manipuler une base de données depuis un programme Python.

## Mise en situation

On gère la base de données d'une médiathèque, avec deux tables :

```
Livres(id, titre, auteur, disponible)
Emprunts(id, livre_id, emprunteur, date_emprunt)
```

---

## Partie A — Création de la base

**A.1.** Écrire un script Python qui crée une base SQLite `mediatheque.db` avec les deux tables ci-dessus (`disponible` de type entier, `1` pour vrai et `0` pour faux ; `livre_id` est une clé étrangère vers `Livres.id`).

**A.2.** Insérer au moins 6 livres et 3 emprunts de votre choix (les livres empruntés doivent avoir `disponible = 0`).

---

## Partie B — Interrogations

Écrire, tester et exécuter les requêtes SQL suivantes depuis Python (à l'aide de `curseur.execute(...)` puis `curseur.fetchall()`) :

**B.1.** Afficher les titres de tous les livres disponibles.

**B.2.** Afficher les auteurs distincts présents dans la base.

**B.3.** Afficher, pour chaque emprunt, le titre du livre et le nom de l'emprunteur (nécessite une jointure entre `Livres` et `Emprunts`).

**B.4.** Compter le nombre de livres actuellement empruntés (`disponible = 0`).

---

## Partie C — Fonctions Python autour de la base

**C.1.** Écrire une fonction `emprunter_livre(connexion, titre, emprunteur, date)` qui : vérifie que le livre est disponible, puis, si c'est le cas, ajoute une ligne dans `Emprunts` et met à jour `Livres.disponible` à `0`. Elle renverra `True` en cas de succès, `False` si le livre n'était pas disponible ou n'existe pas.

**C.2.** Écrire une fonction `rendre_livre(connexion, titre)` qui remet `disponible` à `1` pour ce livre (on ne supprime pas la ligne d'emprunt, pour garder un historique).

**C.3.** Tester ces deux fonctions sur plusieurs cas, y compris un emprunt refusé (livre déjà emprunté) et un livre inexistant.

---

## Corrigé indicatif

```python
import sqlite3

connexion = sqlite3.connect("mediatheque.db")
curseur = connexion.cursor()

curseur.execute("""
CREATE TABLE IF NOT EXISTS Livres (
    id INTEGER PRIMARY KEY,
    titre TEXT,
    auteur TEXT,
    disponible INTEGER
)
""")

curseur.execute("""
CREATE TABLE IF NOT EXISTS Emprunts (
    id INTEGER PRIMARY KEY,
    livre_id INTEGER,
    emprunteur TEXT,
    date_emprunt TEXT,
    FOREIGN KEY (livre_id) REFERENCES Livres(id)
)
""")

livres = [
    (1, "1984", "Orwell", 1),
    (2, "Dune", "Herbert", 1),
    (3, "Fondation", "Asimov", 1),
    (4, "La Peste", "Camus", 1),
    (5, "Les Misérables", "Hugo", 1),
    (6, "Fahrenheit 451", "Bradbury", 1),
]
curseur.executemany("INSERT OR IGNORE INTO Livres VALUES (?,?,?,?)", livres)
connexion.commit()


def emprunter_livre(connexion, titre, emprunteur, date):
    curseur = connexion.cursor()
    curseur.execute("SELECT id, disponible FROM Livres WHERE titre = ?", (titre,))
    resultat = curseur.fetchone()
    if resultat is None or resultat[1] == 0:
        return False
    livre_id = resultat[0]
    curseur.execute(
        "INSERT INTO Emprunts (livre_id, emprunteur, date_emprunt) VALUES (?, ?, ?)",
        (livre_id, emprunteur, date),
    )
    curseur.execute("UPDATE Livres SET disponible = 0 WHERE id = ?", (livre_id,))
    connexion.commit()
    return True


def rendre_livre(connexion, titre):
    curseur = connexion.cursor()
    curseur.execute("UPDATE Livres SET disponible = 1 WHERE titre = ?", (titre,))
    connexion.commit()
    return curseur.rowcount > 0


# --- Partie B ---
curseur.execute("SELECT titre FROM Livres WHERE disponible = 1")
print(curseur.fetchall())

curseur.execute("SELECT DISTINCT auteur FROM Livres")
print(curseur.fetchall())

curseur.execute("""
SELECT Livres.titre, Emprunts.emprunteur
FROM Livres JOIN Emprunts ON Livres.id = Emprunts.livre_id
""")
print(curseur.fetchall())

curseur.execute("SELECT COUNT(*) FROM Livres WHERE disponible = 0")
print(curseur.fetchall())

# --- Partie C : tests ---
assert emprunter_livre(connexion, "1984", "Ada", "2025-09-01") == True
assert emprunter_livre(connexion, "1984", "Alan", "2025-09-02") == False   # déjà emprunté
assert emprunter_livre(connexion, "Inconnu", "Grace", "2025-09-02") == False
rendre_livre(connexion, "1984")
assert emprunter_livre(connexion, "1984", "Alan", "2025-09-03") == True

connexion.close()
```
