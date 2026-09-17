# Chapitre 2 — Types construits : p-uplets, tableaux, dictionnaires
## Évaluation

*Première NSI — Durée : 55 min — Barème sur 20 points*

---

### Partie 1 — Questions de cours (6 points)

**Question 1 (2 pts).** Quelle est la différence essentielle entre un p-uplet (`tuple`) et un tableau (`list`) ?

**Question 2 (2 pts).** Dans quel cas préfère-t-on utiliser un p-uplet nommé (`namedtuple`) plutôt qu'un dictionnaire pour représenter une même structure de données ?

**Question 3 (2 pts).** Pour créer une matrice `n × n` de zéros, pourquoi écrit-on `[[0]*n for _ in range(n)]` plutôt que `[[0]*n]*n` ? Expliquer précisément le problème posé par la seconde écriture.

---

### Partie 2 — Manipulations (8 points)

**Question 4 (3 pts).** Écrire une fonction `moyenne_ponderee(notes_coeffs)` qui prend en paramètre une liste de tuples `(note, coefficient)` et renvoie la moyenne pondérée correspondante.

**Question 5 (2 pts).** Vérifier que `moyenne_ponderee([(15, 2), (12, 1), (18, 3)])` renvoie `16.0`. Détailler le calcul.

**Question 6 (3 pts).** Écrire une fonction `inverser_dict(d)` qui prend un dictionnaire `d` dont les valeurs sont toutes distinctes, et renvoie un nouveau dictionnaire où les clés et les valeurs sont échangées (indication : on peut utiliser une compréhension de dictionnaire `{v: k for k, v in d.items()}`).

---

### Partie 3 — Écrire du code (6 points)

On représente un ensemble d'élèves et leurs notes par le dictionnaire suivant :
```python
classe = {
    "Alice": [15, 12, 18],
    "Bob": [10, 8, 14],
    "Chloé": [17, 19, 16],
}
```

**Question 7 (3 pts).** Écrire une fonction `moyenne_par_eleve(classe)` qui renvoie un dictionnaire associant à chaque nom d'élève sa moyenne simple (arithmétique, sans coefficient).

**Question 8 (3 pts).** Écrire une fonction `meilleur_eleve(classe)` qui renvoie le nom de l'élève ayant la meilleure moyenne (indication : on pourra réutiliser `moyenne_par_eleve`, puis chercher la clé associée à la plus grande valeur).

---

## Corrigé et barème détaillé

### Partie 1 (6 pts)

**Q1 (2 pts)** — Un p-uplet est **immuable** (on ne peut pas le modifier après sa création) alors qu'un tableau (liste) est **modifiable** (on peut ajouter, retirer ou changer des éléments) (2 pts pour la notion d'immuabilité correctement expliquée).

**Q2 (2 pts)** — On préfère un p-uplet nommé lorsque la structure des champs est **fixe et connue à l'avance**, identique pour toutes les instances (par exemple, tous les points ont exactement `x` et `y`) : cela garantit qu'aucun champ ne manque, et l'accès par attribut (`p.x`) est plus lisible qu'un accès par clé de dictionnaire (2 pts).

**Q3 (2 pts)** — `[[0]*n]*n` crée une liste contenant `n` fois la **même référence** vers une seule et même liste interne `[0]*n` (1 pt) : modifier un élément d'une « ligne » modifierait alors, par effet de bord, la ligne correspondante dans toutes les autres lignes, car elles pointent toutes vers le même objet en mémoire (1 pt). La compréhension `[[0]*n for _ in range(n)]` crée, elle, une nouvelle liste indépendante à chaque itération.

### Partie 2 (8 pts)

**Q4 (3 pts)**
```python
def moyenne_ponderee(notes_coeffs):
    total_points = sum(note * coeff for note, coeff in notes_coeffs)
    total_coeffs = sum(coeff for note, coeff in notes_coeffs)
    return total_points / total_coeffs
```
*(1,5 pt pour le calcul correct du numérateur, 1,5 pt pour le dénominateur et la division.)*

**Q5 (2 pts)** — `(15×2 + 12×1 + 18×3) / (2+1+3) = (30+12+54) / 6 = 96 / 6 = 16.0`.

**Q6 (3 pts)**
```python
def inverser_dict(d):
    return {valeur: cle for cle, valeur in d.items()}
```

### Partie 3 (6 pts)

**Q7 (3 pts)**
```python
def moyenne_par_eleve(classe):
    return {nom: sum(notes) / len(notes) for nom, notes in classe.items()}
```
*(2 pts pour le parcours correct avec `.items()`, 1 pt pour le calcul de moyenne.)*

**Q8 (3 pts)**
```python
def meilleur_eleve(classe):
    moyennes = moyenne_par_eleve(classe)
    return max(moyennes, key=lambda nom: moyennes[nom])
```
*(Toute solution correcte est acceptée, par exemple un parcours manuel avec une variable "meilleure moyenne trouvée jusqu'ici" ; 2 pts pour la logique de comparaison correcte, 1 pt pour le renvoi du bon résultat.)*

---

**Barème global : 6 + 8 + 6 = 20 points.**
