# Chapitre 3 — Structures linéaires
## Évaluation

*Terminale NSI — Durée : 55 min — Barème sur 20 points*

---

### Partie 1 — Questions de cours (6 points)

**Question 1 (2 pts).** Qu'est-ce qu'un maillon dans une liste chaînée ? De quoi est-il composé ?

**Question 2 (2 pts).** Expliquer pourquoi l'insertion en tête d'une liste chaînée est plus rapide que l'insertion en tête d'une liste Python (`list`).

**Question 3 (2 pts).** Expliquer, sans entrer dans les détails d'implémentation, pourquoi la recherche par clé dans un dictionnaire est en moyenne plus rapide que la recherche d'une valeur dans une liste.

---

### Partie 2 — Liste chaînée (7 points)

On donne :
```python
class Maillon:
    def __init__(self, valeur, suivant=None):
        self.valeur = valeur
        self.suivant = suivant
```

**Question 4 (3 pts).** Écrire une fonction `somme_liste(tete)` qui reçoit la tête d'une liste chaînée d'entiers et renvoie la somme de ses valeurs (on suppose qu'il n'y a pas de méthode disponible, uniquement la classe `Maillon` ci-dessus).

**Question 5 (4 pts).** Écrire une fonction `maximum_liste(tete)` qui renvoie la valeur maximale contenue dans une liste chaînée non vide (même remarque que ci-dessus).

---

### Partie 3 — Dictionnaires (7 points)

On donne un dictionnaire représentant le stock d'un magasin : `stock = {"pommes": 34, "poires": 12, "bananes": 0, "kiwis": 8}`.

**Question 6 (3 pts).** Écrire une fonction `produits_en_rupture(stock)` qui renvoie la liste des noms de produits dont la quantité en stock est nulle.

**Question 7 (4 pts).** Écrire une fonction `vendre(stock, produit, quantite)` qui diminue de `quantite` le stock du `produit` donné. Si le produit n'existe pas dans `stock`, ou si la quantité demandée est supérieure au stock disponible, la fonction ne modifie rien et renvoie `False` ; sinon elle effectue la vente et renvoie `True`.

---

## Corrigé et barème détaillé

### Partie 1 (6 pts)

**Q1 (2 pts)** — Un maillon est un élément d'une liste chaînée ; il contient une valeur (1 pt) et une référence vers le maillon suivant (1 pt), ou `None` s'il s'agit du dernier maillon.

**Q2 (2 pts)** — Insérer en tête d'une liste chaînée ne demande de modifier que quelques références (temps constant, 1 pt), alors qu'insérer en tête d'une liste Python (`list.insert(0, x)`) impose de décaler tous les éléments existants d'une case, ce qui prend un temps proportionnel au nombre d'éléments (1 pt).

**Q3 (2 pts)** — Un dictionnaire utilise une table de hachage qui calcule, à partir de la clé, l'emplacement où se trouve la valeur associée, ce qui permet d'y accéder directement (1 pt), alors qu'une liste doit être parcourue élément par élément jusqu'à trouver (ou ne pas trouver) la valeur cherchée (1 pt).

### Partie 2 (7 pts)

**Q4 (3 pts)**
```python
def somme_liste(tete):
    total = 0
    courant = tete
    while courant is not None:
        total = total + courant.valeur
        courant = courant.suivant
    return total
```
*(1 pt initialisation ; 1 pt boucle de parcours correcte ; 1 pt accumulation et valeur de retour.)*

**Q5 (4 pts)**
```python
def maximum_liste(tete):
    maximum = tete.valeur
    courant = tete.suivant
    while courant is not None:
        if courant.valeur > maximum:
            maximum = courant.valeur
        courant = courant.suivant
    return maximum
```
*(1 pt initialisation correcte avec le premier élément ; 2 pts boucle et comparaison ; 1 pt valeur de retour.)*

### Partie 3 (7 pts)

**Q6 (3 pts)**
```python
def produits_en_rupture(stock):
    return [produit for produit, quantite in stock.items() if quantite == 0]
```
*(1 pt parcours des couples clé/valeur ; 1 pt condition correcte ; 1 pt construction de la liste.)*

**Q7 (4 pts)**
```python
def vendre(stock, produit, quantite):
    if produit not in stock or quantite > stock[produit]:
        return False
    stock[produit] = stock[produit] - quantite
    return True
```
*(1 pt vérification de l'existence du produit ; 1 pt vérification de la quantité disponible ; 1 pt mise à jour correcte du stock ; 1 pt valeurs de retour correctes dans les deux cas.)*

---

**Barème global : 6 + 7 + 7 = 20 points.**
