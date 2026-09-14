# Chapitre 4 — Arbres binaires
## TP sur machine — Un annuaire sous forme d'arbre binaire de recherche

*Terminale NSI — Python 3 — Durée indicative : 1h30 à 2h*

---

## Objectifs

- Construire et manipuler un arbre binaire de recherche.
- Mettre en œuvre les quatre parcours d'un arbre.
- Mesurer expérimentalement l'intérêt d'un ABR par rapport à une recherche linéaire.

## Mise en situation

On souhaite stocker un annuaire de contacts, indexés par un identifiant numérique, dans un arbre binaire de recherche.

---

## Partie A — Construction et parcours

**A.1.** Reprendre la classe `NoeudArbre` et les fonctions `inserer`, `rechercher`, `parcours_infixe`, `parcours_prefixe`, `parcours_largeur` du cours.

**A.2.** Construire un ABR en insérant, dans cet ordre, les identifiants suivants : `50, 30, 70, 20, 40, 60, 80, 10, 25`.

**A.3.** Afficher les quatre parcours de cet arbre (préfixe, infixe, suffixe, largeur) et vérifier que le parcours infixe donne bien la liste triée des identifiants.

---

## Partie B — Un annuaire complet

**B.1.** Modifier `NoeudArbre` pour qu'il stocke, en plus de la clé (l'identifiant), une valeur associée (par exemple le nom du contact) :

```python
class NoeudAnnuaire:
    def __init__(self, cle, valeur, gauche=None, droit=None):
        self.cle = cle
        self.valeur = valeur
        self.gauche = gauche
        self.droit = droit
```

**B.2.** Adapter `inserer` et écrire une fonction `rechercher_valeur(arbre, cle)` qui renvoie la valeur associée à une clé, ou `None` si la clé est absente.

**B.3.** Construire un annuaire avec au moins 8 contacts `(identifiant, nom)` de votre choix, puis tester plusieurs recherches.

---

## Partie C — ABR contre recherche linéaire

**C.1.** Générer une liste de 2000 entiers aléatoires distincts (module `random`), les insérer un par un dans un ABR, puis chronométrer 1000 recherches d'identifiants tirés au hasard dans cet ABR.

**C.2.** Chronométrer les mêmes 1000 recherches, mais effectuées par un simple parcours linéaire (`in`) sur la liste Python d'origine.

**C.3.** Comparer les deux durées obtenues et conclure sur l'intérêt d'un ABR pour la recherche, en la reliant à la notion de coût logarithmique vue en cours.

---

## Corrigé indicatif

```python
class NoeudAnnuaire:
    def __init__(self, cle, valeur, gauche=None, droit=None):
        self.cle = cle
        self.valeur = valeur
        self.gauche = gauche
        self.droit = droit


def inserer_annuaire(arbre, cle, valeur):
    if arbre is None:
        return NoeudAnnuaire(cle, valeur)
    if cle < arbre.cle:
        arbre.gauche = inserer_annuaire(arbre.gauche, cle, valeur)
    elif cle > arbre.cle:
        arbre.droit = inserer_annuaire(arbre.droit, cle, valeur)
    return arbre


def rechercher_valeur(arbre, cle):
    if arbre is None:
        return None
    if cle == arbre.cle:
        return arbre.valeur
    elif cle < arbre.cle:
        return rechercher_valeur(arbre.gauche, cle)
    else:
        return rechercher_valeur(arbre.droit, cle)


# --- Partie C ---
import random
import time

identifiants = random.sample(range(1_000_000), 2000)

annuaire = None
for i in identifiants:
    annuaire = inserer_annuaire(annuaire, i, f"contact_{i}")

recherches = random.sample(identifiants, 1000)

debut = time.perf_counter()
for cle in recherches:
    rechercher_valeur(annuaire, cle)
duree_abr = time.perf_counter() - debut

debut = time.perf_counter()
for cle in recherches:
    cle in identifiants
duree_liste = time.perf_counter() - debut

print("Durée ABR   :", duree_abr)
print("Durée liste :", duree_liste)
```

On observe que la recherche dans l'ABR est nettement plus rapide que la recherche linéaire dans la liste, ce qui illustre concrètement la différence entre un coût logarithmique (ABR, si l'arbre reste raisonnablement équilibré) et un coût linéaire (liste).
