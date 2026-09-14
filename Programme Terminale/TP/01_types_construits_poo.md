# Chapitre 1 — Types construits & POO
## TP sur machine — Gestion d'une petite bibliothèque

*Terminale NSI — Python 3 — Durée indicative : 1h30 à 2h*

---

## Objectifs

- Manipuler des tableaux, des enregistrements et des classes dans un même projet.
- Concevoir une classe avec attributs, constructeur et méthodes.
- Combiner un tableau d'objets pour modéliser une petite base de données en mémoire.

## Mise en situation

On souhaite développer un petit programme de gestion des emprunts d'une bibliothèque de classe. On modélisera successivement le problème avec des enregistrements (dictionnaires), puis avec des objets.

---

## Partie A — Avec des enregistrements

Un livre est représenté par un dictionnaire `{"titre": ..., "auteur": ..., "annee": ..., "disponible": ...}`.

**A.1.** Créer une liste `bibliotheque` contenant au moins 5 livres de votre choix (tous disponibles au départ).

**A.2.** Écrire une fonction `chercher_par_titre(bibliotheque, titre)` qui renvoie le dictionnaire du livre correspondant, ou `None` s'il n'existe pas.

**A.3.** Écrire une fonction `emprunter(bibliotheque, titre)` qui :
- si le livre existe et est disponible, passe `"disponible"` à `False` et renvoie `True` ;
- sinon, renvoie `False`.

**A.4.** Écrire une fonction `livres_par_auteur(bibliotheque, auteur)` qui renvoie la liste des titres d'un auteur donné.

**A.5.** Écrire une fonction `livres_apres(bibliotheque, annee)` qui renvoie la liste des titres publiés strictement après une année donnée.

---

## Partie B — Avec une classe `Livre`

On reprend le même problème, mais en programmation orientée objet.

**B.1.** Écrire une classe `Livre` avec :
- un constructeur `__init__(self, titre, auteur, annee)` ;
- un attribut `disponible` initialisé à `True` ;
- une méthode `emprunter(self)` qui rend le livre indisponible s'il est disponible (et affiche un message sinon) ;
- une méthode `rendre(self)` qui rend le livre disponible ;
- une méthode `__str__(self)` qui renvoie une chaîne du type `"1984 (Orwell, 1949) - disponible"`.

**B.2.** Créer une liste `bibliotheque_objets` d'au moins 5 objets `Livre`.

**B.3.** Réécrire les fonctions `chercher_par_titre`, `livres_par_auteur` et `livres_apres` de la partie A pour qu'elles fonctionnent avec des objets `Livre` au lieu de dictionnaires.

---

## Partie C — La classe `Bibliotheque`

On veut maintenant encapsuler toute la logique dans une classe `Bibliotheque`, qui gère elle-même sa collection de livres.

**C.1.** Écrire une classe `Bibliotheque` avec :
- un constructeur qui initialise une liste vide `self.livres` ;
- une méthode `ajouter_livre(self, livre)` qui ajoute un objet `Livre` à la collection ;
- une méthode `chercher_par_titre(self, titre)` ;
- une méthode `emprunter(self, titre)` qui renvoie `True`/`False` selon le succès de l'emprunt ;
- une méthode `livres_disponibles(self)` qui renvoie la liste des titres disponibles ;
- une méthode `nombre_emprunts(self)` qui renvoie le nombre de livres actuellement empruntés.

**C.2.** Créer une instance de `Bibliotheque`, y ajouter vos 5 livres, effectuer quelques emprunts et vérifier que les compteurs sont cohérents.

**C.3. (bonus)** Ajouter à `Bibliotheque` une méthode `emprunts_par_eleve` qui utilise un dictionnaire associant le nom d'un élève à la liste des titres qu'il a empruntés, afin de suivre qui a emprunté quoi.

---

## Grille d'auto-évaluation

| Critère | Acquis |
|---|---|
| Le programme s'exécute sans erreur | ☐ |
| Les fonctions de la partie A fonctionnent avec des dictionnaires | ☐ |
| La classe `Livre` est correctement définie (attributs + méthodes) | ☐ |
| La classe `Bibliotheque` encapsule correctement la liste des livres | ☐ |
| Le code est testé avec plusieurs cas (livre disponible, indisponible, inexistant) | ☐ |

---

## Corrigé indicatif

```python
# --- Partie A ---
bibliotheque = [
    {"titre": "1984", "auteur": "Orwell", "annee": 1949, "disponible": True},
    {"titre": "Dune", "auteur": "Herbert", "annee": 1965, "disponible": True},
    {"titre": "Fondation", "auteur": "Asimov", "annee": 1951, "disponible": True},
    {"titre": "Les Misérables", "auteur": "Hugo", "annee": 1862, "disponible": True},
    {"titre": "La Peste", "auteur": "Camus", "annee": 1947, "disponible": True},
]

def chercher_par_titre(bib, titre):
    for livre in bib:
        if livre["titre"] == titre:
            return livre
    return None

def emprunter(bib, titre):
    livre = chercher_par_titre(bib, titre)
    if livre is not None and livre["disponible"]:
        livre["disponible"] = False
        return True
    return False

def livres_par_auteur(bib, auteur):
    return [l["titre"] for l in bib if l["auteur"] == auteur]

def livres_apres(bib, annee):
    return [l["titre"] for l in bib if l["annee"] > annee]


# --- Partie B ---
class Livre:
    def __init__(self, titre, auteur, annee):
        self.titre = titre
        self.auteur = auteur
        self.annee = annee
        self.disponible = True

    def emprunter(self):
        if self.disponible:
            self.disponible = False
        else:
            print(f"« {self.titre} » n'est pas disponible.")

    def rendre(self):
        self.disponible = True

    def __str__(self):
        etat = "disponible" if self.disponible else "emprunté"
        return f"{self.titre} ({self.auteur}, {self.annee}) - {etat}"


bibliotheque_objets = [
    Livre("1984", "Orwell", 1949),
    Livre("Dune", "Herbert", 1965),
    Livre("Fondation", "Asimov", 1951),
    Livre("Les Misérables", "Hugo", 1862),
    Livre("La Peste", "Camus", 1947),
]

def chercher_par_titre_obj(bib, titre):
    for livre in bib:
        if livre.titre == titre:
            return livre
    return None

def livres_par_auteur_obj(bib, auteur):
    return [l.titre for l in bib if l.auteur == auteur]

def livres_apres_obj(bib, annee):
    return [l.titre for l in bib if l.annee > annee]


# --- Partie C ---
class Bibliotheque:
    def __init__(self):
        self.livres = []

    def ajouter_livre(self, livre):
        self.livres.append(livre)

    def chercher_par_titre(self, titre):
        for livre in self.livres:
            if livre.titre == titre:
                return livre
        return None

    def emprunter(self, titre):
        livre = self.chercher_par_titre(titre)
        if livre is not None and livre.disponible:
            livre.disponible = False
            return True
        return False

    def livres_disponibles(self):
        return [l.titre for l in self.livres if l.disponible]

    def nombre_emprunts(self):
        return len([l for l in self.livres if not l.disponible])
```
