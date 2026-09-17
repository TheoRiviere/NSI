# Chapitre 2 — Types construits : p-uplets, tableaux, dictionnaires
## TP sur machine — Carnet d'adresses, traitement d'image et inventaire

*Première NSI — Python 3 — Durée indicative : 1h30 à 2h*

---

## Objectifs

- Combiner p-uplets nommés et dictionnaires pour gérer un carnet d'adresses.
- Manipuler une image en niveaux de gris représentée par une matrice.
- Utiliser un dictionnaire de dictionnaires pour gérer un inventaire.

---

## Partie A — Carnet d'adresses

On représente un carnet d'adresses par un dictionnaire dont les clés sont les noms des contacts, et les valeurs des p-uplets nommés `Contact`.

**A.1.** Définir le type `Contact` avec les champs `nom`, `telephone`, `email`, à l'aide de `namedtuple`.

**A.2.** Écrire une fonction `ajouter_contact(carnet, nom, telephone, email)` qui ajoute (ou remplace) un contact dans le dictionnaire `carnet` (la fonction modifie `carnet` directement, elle ne renvoie rien).

**A.3.** Écrire une fonction `rechercher_contact(carnet, nom)` qui renvoie le `Contact` correspondant au nom donné, ou `None` si ce nom n'existe pas dans le carnet (indication : utiliser `.get`).

**A.4.** Écrire une fonction `supprimer_contact(carnet, nom)` qui supprime le contact s'il existe (et ne fait rien sinon, sans provoquer d'erreur).

**A.5.** Tester l'ensemble : ajouter deux contacts, rechercher l'un d'eux et afficher son numéro de téléphone, rechercher un contact inexistant, supprimer un contact et vérifier qu'il n'est plus présent.

---

## Partie B — Traitement d'une image en niveaux de gris

Une image en niveaux de gris peut être représentée par une matrice d'entiers entre 0 (noir) et 255 (blanc), chaque entier représentant l'intensité lumineuse d'un pixel.

```python
image = [
    [10, 20, 30],
    [40, 50, 60],
    [70, 80, 90],
]
```

**B.1.** Écrire une fonction `negatif(image, valeur_max=255)` qui renvoie une nouvelle image où chaque pixel `p` est remplacé par `valeur_max - p` (indication : on utilisera une compréhension de liste imbriquée, comme pour `transposer` dans le cours).

**B.2.** Vérifier que `negatif(image)[0][0] == 245` et `negatif(image)[2][2] == 165`.

**B.3.** Recopier la fonction `rotation_90` (rotation d'un quart de tour) — vous pouvez vous inspirer de `transposer` du cours, en adaptant les indices pour obtenir une vraie rotation plutôt qu'une simple transposition (indication : le pixel `image[i][j]` doit se retrouver, après une rotation de 90° dans le sens horaire, en position `resultat[j][lignes-1-i]`).

**B.4.** Écrire une fonction `luminosite_moyenne(image)` qui calcule la moyenne de tous les pixels de l'image (parcours des deux dimensions).

**B.5.** Vérifier que `luminosite_moyenne(image)` renvoie `50.0` pour l'image donnée en exemple.

---

## Partie C — Gestion d'un inventaire de magasin

On représente l'inventaire d'un magasin par un dictionnaire associant à chaque nom de produit un dictionnaire `{"prix": ..., "quantite": ...}`.

**C.1.** Écrire une fonction `ajouter_produit(inventaire, nom, prix, quantite)` qui ajoute un produit à l'inventaire.

**C.2.** Écrire une fonction `valeur_totale_stock(inventaire)` qui calcule la valeur totale du stock (somme, pour chaque produit, de `prix × quantite`), en utilisant `.values()` et la fonction native `sum`.

**C.3.** Écrire une fonction `produits_en_rupture(inventaire, seuil=10)` qui renvoie la liste des noms de produits dont la quantité est strictement inférieure au `seuil` donné (indication : utiliser `.items()` et une compréhension de liste).

**C.4.** Créer un inventaire avec au moins 3 produits, dont un avec une quantité faible (inférieure à 10), et vérifier que `produits_en_rupture` le détecte correctement.

---

## Corrigé indicatif

```python
from collections import namedtuple

# --- Partie A ---
Contact = namedtuple('Contact', ['nom', 'telephone', 'email'])

def ajouter_contact(carnet, nom, telephone, email):
    carnet[nom] = Contact(nom, telephone, email)

def rechercher_contact(carnet, nom):
    return carnet.get(nom)

def supprimer_contact(carnet, nom):
    if nom in carnet:
        del carnet[nom]

carnet = {}
ajouter_contact(carnet, "Alice", "0611223344", "alice@mail.fr")
ajouter_contact(carnet, "Bob", "0622334455", "bob@mail.fr")
print(rechercher_contact(carnet, "Alice").telephone)   # 0611223344
print(rechercher_contact(carnet, "Zoé"))                # None
supprimer_contact(carnet, "Bob")
assert "Bob" not in carnet


# --- Partie B ---
image = [
    [10, 20, 30],
    [40, 50, 60],
    [70, 80, 90],
]

def negatif(image, valeur_max=255):
    return [[valeur_max - pixel for pixel in ligne] for ligne in image]

def rotation_90(image):
    lignes = len(image)
    colonnes = len(image[0])
    resultat = [[0] * lignes for _ in range(colonnes)]
    for i in range(lignes):
        for j in range(colonnes):
            resultat[j][lignes - 1 - i] = image[i][j]
    return resultat

def luminosite_moyenne(image):
    total = 0
    n = 0
    for ligne in image:
        for pixel in ligne:
            total += pixel
            n += 1
    return total / n

print(negatif(image))
print(rotation_90(image))
print(luminosite_moyenne(image))   # 50.0


# --- Partie C ---
def ajouter_produit(inventaire, nom, prix, quantite):
    inventaire[nom] = {"prix": prix, "quantite": quantite}

def valeur_totale_stock(inventaire):
    return sum(p["prix"] * p["quantite"] for p in inventaire.values())

def produits_en_rupture(inventaire, seuil=10):
    return [nom for nom, p in inventaire.items() if p["quantite"] < seuil]

inventaire = {}
ajouter_produit(inventaire, "Cahier", 2.5, 100)
ajouter_produit(inventaire, "Stylo", 1.0, 200)
ajouter_produit(inventaire, "Gomme", 0.5, 5)

print(valeur_totale_stock(inventaire))     # 450.0
print(produits_en_rupture(inventaire))     # ['Gomme']
```
