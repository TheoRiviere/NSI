# Chapitre 1 — Types construits & POO
## Fiche d'exercices

*Terminale NSI — Python 3*

---

### Exercice 1 — N-uplets

1. Écrire une fonction `milieu(a, b)` qui reçoit deux points `a` et `b` sous forme de 2-uplets `(x, y)` et renvoie le 2-uplet représentant leur point milieu.
2. Écrire une fonction `stats(valeurs)` qui reçoit une liste de nombres et renvoie un 3-uplet `(minimum, maximum, moyenne)`.
3. Que se passe-t-il si on exécute `p = (1, 2); p[0] = 5` ? Expliquer pourquoi.

### Exercice 2 — N-uplets nommés

On souhaite représenter des élèves par leur nom, leur âge et leur moyenne générale.

1. Définir un n-uplet nommé `Eleve` avec les champs `nom`, `age`, `moyenne`.
2. Créer trois élèves de votre choix.
3. Écrire une fonction `meilleur_eleve(eleves)` qui reçoit une liste d'objets `Eleve` et renvoie celui qui a la meilleure moyenne.

### Exercice 3 — Tableaux

1. Écrire une fonction `inverser(tableau)` qui inverse **en place** (sans créer de nouveau tableau) l'ordre des éléments d'une liste.
2. Écrire une fonction `sans_doublons(tableau)` qui renvoie un nouveau tableau contenant les éléments de `tableau`, sans doublons, en conservant l'ordre d'apparition.
3. Expliquer pourquoi le code suivant ne fait pas ce que l'on pourrait attendre, et proposer une correction :
   ```python
   def ajoute_zero(tableau):
       tableau = tableau + [0]

   t = [1, 2, 3]
   ajoute_zero(t)
   print(t)  # que va afficher cette ligne ?
   ```

### Exercice 4 — Tableaux de tableaux

On représente une grille de sudoku 4×4 par un tableau de tableaux d'entiers (0 = case vide).

1. Écrire une fonction `case_vide(grille)` qui renvoie le couple `(ligne, colonne)` de la première case vide rencontrée (parcours ligne par ligne), ou `None` s'il n'y en a pas.
2. Écrire une fonction `ligne_valide(grille, i)` qui vérifie que la ligne `i` ne contient pas deux fois la même valeur non nulle.
3. Expliquer pourquoi `grille = [[0] * 4] * 4` est dangereux pour représenter une grille modifiable, avec un exemple précis illustrant le problème.

### Exercice 5 — Enregistrements

On modélise un carnet d'adresses par une liste de dictionnaires, chacun avec les clés `"nom"`, `"telephone"`, `"email"`.

1. Écrire une fonction `rechercher(carnet, nom)` qui renvoie la fiche correspondant à un nom donné, ou `None` si absent.
2. Écrire une fonction `ajouter_contact(carnet, nom, telephone, email)` qui ajoute une nouvelle fiche au carnet.
3. Écrire une fonction `sans_email(carnet)` qui renvoie la liste des noms des contacts n'ayant pas d'adresse email renseignée (clé absente ou vide).

### Exercice 6 — Choisir le bon type

Pour chacune des situations suivantes, indiquer le type construit le plus adapté (n-uplet, n-uplet nommé, tableau, tableau de tableaux ou enregistrement) et justifier en une phrase :

1. Les coordonnées GPS (latitude, longitude) d'un lieu, qui ne changeront jamais une fois calculées.
2. La liste des notes d'un élève sur l'année, appelée à être complétée au fil du temps.
3. Le plateau d'un jeu de morpion (3×3 cases).
4. La fiche d'identité d'un utilisateur (nom, prénom, date de naissance, adresse).

---

### Exercice 7 — Une classe `Rectangle`

1. Écrire une classe `Rectangle` avec un constructeur prenant la largeur et la hauteur.
2. Ajouter une méthode `aire()` qui renvoie l'aire du rectangle.
3. Ajouter une méthode `perimetre()` qui renvoie le périmètre.
4. Ajouter une méthode `est_carre()` qui renvoie `True` si le rectangle est un carré.
5. Tester la classe avec plusieurs instances.

### Exercice 8 — La classe `CompteBancaire` (prolongement du cours)

En reprenant la classe `CompteBancaire` vue en cours :

1. Ajouter un attribut `historique` (une liste) qui enregistre chaque opération sous la forme d'une chaîne de caractères (par exemple `"dépôt de 50"`).
2. Ajouter une méthode `afficher_historique()` qui affiche toutes les opérations effectuées.
3. Modifier le constructeur pour refuser un `solde_initial` négatif (lever une `ValueError`).

### Exercice 9 — Encapsulation, vrai ou faux ?

Pour chacune des affirmations suivantes, dire si elle est vraie ou fausse et justifier :

1. En Python, un attribut précédé d'un simple underscore (`_solde`) est totalement inaccessible depuis l'extérieur de la classe.
2. L'encapsulation empêche toute modification des attributs d'un objet.
3. L'interface d'une classe correspond à l'ensemble de ses méthodes publiques, utilisables sans connaître le code de la classe.
4. Deux classes différentes peuvent avoir la même interface tout en ayant des implémentations différentes.

### Exercice 10 — Classe `Livre` et tableau d'objets

1. Écrire une classe `Livre` avec les attributs `titre`, `auteur`, `disponible` (booléen, `True` par défaut).
2. Ajouter les méthodes `emprunter()` (passe `disponible` à `False`, ou affiche un message si déjà emprunté) et `rendre()`.
3. Créer une liste de plusieurs objets `Livre`.
4. Écrire une fonction `livres_disponibles(liste_livres)` qui renvoie la liste des titres des livres actuellement disponibles.

---

## Corrigés

### Exercice 1

```python
def milieu(a, b):
    return ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)

def stats(valeurs):
    return (min(valeurs), max(valeurs), sum(valeurs) / len(valeurs))
```

3. `p[0] = 5` lève une `TypeError` car un n-uplet est **immuable** : une fois créé, on ne peut plus modifier ses éléments.

### Exercice 2

```python
from collections import namedtuple

Eleve = namedtuple("Eleve", ["nom", "age", "moyenne"])

e1 = Eleve("Ada", 17, 15.2)
e2 = Eleve("Alan", 18, 16.8)
e3 = Eleve("Grace", 17, 14.5)

def meilleur_eleve(eleves):
    meilleur = eleves[0]
    for e in eleves[1:]:
        if e.moyenne > meilleur.moyenne:
            meilleur = e
    return meilleur
```

### Exercice 3

```python
def inverser(tableau):
    gauche, droite = 0, len(tableau) - 1
    while gauche < droite:
        tableau[gauche], tableau[droite] = tableau[droite], tableau[gauche]
        gauche += 1
        droite -= 1

def sans_doublons(tableau):
    resultat = []
    for x in tableau:
        if x not in resultat:
            resultat.append(x)
    return resultat
```

3. La ligne `tableau = tableau + [0]` crée un **nouveau** tableau et le lie au nom local `tableau` à l'intérieur de la fonction : elle ne modifie pas l'objet passé en argument. Le `print(t)` affiche donc `[1, 2, 3]`, sans le `0`. Pour modifier réellement la liste d'origine, il faut utiliser une méthode qui agit en place, par exemple `tableau.append(0)`.

### Exercice 4

```python
def case_vide(grille):
    for i in range(len(grille)):
        for j in range(len(grille[i])):
            if grille[i][j] == 0:
                return (i, j)
    return None

def ligne_valide(grille, i):
    vues = []
    for valeur in grille[i]:
        if valeur != 0:
            if valeur in vues:
                return False
            vues.append(valeur)
    return True
```

3. `[[0] * 4] * 4` construit une liste contenant **quatre fois la même référence** vers la même sous-liste `[0, 0, 0, 0]`. Modifier `grille[0][0] = 1` modifie alors aussi `grille[1][0]`, `grille[2][0]` et `grille[3][0]`, ce qui n'est pas le comportement attendu d'une grille indépendante ligne par ligne.

### Exercice 5

```python
def rechercher(carnet, nom):
    for fiche in carnet:
        if fiche["nom"] == nom:
            return fiche
    return None

def ajouter_contact(carnet, nom, telephone, email):
    carnet.append({"nom": nom, "telephone": telephone, "email": email})

def sans_email(carnet):
    return [fiche["nom"] for fiche in carnet if not fiche.get("email")]
```

### Exercice 6

1. N-uplet (coordonnées immuables, deux valeurs liées).
2. Tableau (collection homogène, mutable, taille variable).
3. Tableau de tableaux (grille à deux dimensions).
4. Enregistrement / n-uplet nommé (champs nommés hétérogènes).

### Exercice 7

```python
class Rectangle:
    def __init__(self, largeur, hauteur):
        self.largeur = largeur
        self.hauteur = hauteur

    def aire(self):
        return self.largeur * self.hauteur

    def perimetre(self):
        return 2 * (self.largeur + self.hauteur)

    def est_carre(self):
        return self.largeur == self.hauteur
```

### Exercice 8

```python
class CompteBancaire:
    def __init__(self, titulaire, solde_initial=0):
        if solde_initial < 0:
            raise ValueError("Le solde initial ne peut pas être négatif")
        self.titulaire = titulaire
        self._solde = solde_initial
        self.historique = []

    def deposer(self, montant):
        if montant <= 0:
            raise ValueError("Le montant doit être positif")
        self._solde = self._solde + montant
        self.historique.append(f"dépôt de {montant}")

    def retirer(self, montant):
        if montant > self._solde:
            raise ValueError("Solde insuffisant")
        self._solde = self._solde - montant
        self.historique.append(f"retrait de {montant}")

    def consulter_solde(self):
        return self._solde

    def afficher_historique(self):
        for operation in self.historique:
            print(operation)
```

### Exercice 9

1. **Faux** : `_solde` reste accessible directement (`compte._solde`), il s'agit d'une simple convention indiquant qu'on ne *devrait* pas y accéder directement.
2. **Faux** : l'encapsulation encadre et contrôle les modifications (via des méthodes), elle ne les empêche pas.
3. **Vrai**.
4. **Vrai** : c'est même l'intérêt principal de la notion d'interface — pouvoir changer l'implémentation sans changer la façon dont on utilise la classe.

### Exercice 10

```python
class Livre:
    def __init__(self, titre, auteur):
        self.titre = titre
        self.auteur = auteur
        self.disponible = True

    def emprunter(self):
        if self.disponible:
            self.disponible = False
        else:
            print(f"« {self.titre} » n'est pas disponible.")

    def rendre(self):
        self.disponible = True


def livres_disponibles(liste_livres):
    return [livre.titre for livre in liste_livres if livre.disponible]
```
