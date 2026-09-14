# Chapitre 3 — Structures linéaires
## TP sur machine — Un éditeur de texte simplifié

*Terminale NSI — Python 3 — Durée indicative : 1h30 à 2h*

---

## Objectifs

- Implémenter et utiliser une liste chaînée pour une application concrète.
- Utiliser une pile pour gérer un historique d'actions (fonctionnalité « annuler »).
- Utiliser un dictionnaire pour indexer des informations et effectuer des recherches rapides.

## Mise en situation

On développe le cœur d'un mini-éditeur de texte qui gère une liste de lignes, un historique d'actions annulables, et un index des mots utilisés (pour une recherche rapide).

---

## Partie A — Les lignes du document (liste chaînée)

**A.1.** Reprendre les classes `Maillon` et `ListeChainee` du cours (avec au minimum `inserer_tete`, `inserer_queue`, `vers_liste_python`, `taille`).

**A.2.** Créer un document en insérant, dans l'ordre, les lignes suivantes en queue : `"Bonjour"`, `"Ceci est un test"`, `"Fin du document"`.

**A.3.** Écrire une fonction `afficher_document(document)` qui affiche chaque ligne précédée de son numéro (à partir de 1).

---

## Partie B — Historique des actions (pile)

On veut pouvoir annuler la dernière action effectuée sur le document.

**B.1.** Écrire une classe `Editeur` qui contient :
- un attribut `lignes` (une simple liste Python, pour simplifier cette partie) ;
- un attribut `historique`, une pile (utiliser `PileListe` du chapitre 2, ou une simple liste Python utilisée en pile avec `append`/`pop`) ;
- une méthode `ajouter_ligne(self, texte)` qui ajoute `texte` à la fin de `lignes` **et** empile l'action `("ajout", texte)` dans l'historique ;
- une méthode `annuler(self)` qui dépile la dernière action et l'annule (si c'était un ajout, on retire la dernière ligne).

**B.2.** Tester : ajouter trois lignes, puis annuler deux fois, et vérifier l'état final de `lignes`.

---

## Partie C — Index des mots (dictionnaire)

**C.1.** Écrire une méthode `indexer(self)` sur la classe `Editeur` qui construit et renvoie un dictionnaire associant chaque mot apparaissant dans le document à la **liste des numéros de lignes** où il apparaît (on ignorera la casse).

**C.2.** Écrire une méthode `rechercher_mot(self, mot)` qui utilise cet index pour renvoyer rapidement la liste des lignes contenant un mot donné.

**C.3. (bonus)** Comparer, en une phrase, le coût de `rechercher_mot` si l'on utilise l'index construit par `indexer`, par rapport à une recherche qui parcourrait toutes les lignes à chaque appel.

---

## Corrigé indicatif

```python
class Maillon:
    def __init__(self, valeur, suivant=None):
        self.valeur = valeur
        self.suivant = suivant

class ListeChainee:
    def __init__(self):
        self._tete = None
        self._taille = 0

    def inserer_queue(self, valeur):
        nouveau = Maillon(valeur)
        if self._tete is None:
            self._tete = nouveau
        else:
            courant = self._tete
            while courant.suivant is not None:
                courant = courant.suivant
            courant.suivant = nouveau
        self._taille += 1

    def taille(self):
        return self._taille

    def vers_liste_python(self):
        resultat = []
        courant = self._tete
        while courant is not None:
            resultat.append(courant.valeur)
            courant = courant.suivant
        return resultat


def afficher_document(document):
    for i, ligne in enumerate(document.vers_liste_python(), start=1):
        print(f"{i}: {ligne}")


class Editeur:
    def __init__(self):
        self.lignes = []
        self.historique = []   # pile : liste Python utilisée avec append/pop

    def ajouter_ligne(self, texte):
        self.lignes.append(texte)
        self.historique.append(("ajout", texte))

    def annuler(self):
        if not self.historique:
            return
        action, texte = self.historique.pop()
        if action == "ajout":
            self.lignes.pop()

    def indexer(self):
        index = {}
        for numero, ligne in enumerate(self.lignes, start=1):
            for mot in ligne.lower().split():
                if mot not in index:
                    index[mot] = []
                if numero not in index[mot]:
                    index[mot].append(numero)
        return index

    def rechercher_mot(self, mot):
        index = self.indexer()
        return index.get(mot.lower(), [])
```

**C.3.** Une fois l'index construit, `rechercher_mot` accède directement à la liste des lignes via la clé (coût quasi constant), alors qu'une recherche « à la volée » sans index devrait reparcourir toutes les lignes du document à chaque appel (coût proportionnel à la taille du document). L'intérêt de l'index est d'autant plus grand que l'on effectue de nombreuses recherches sur un même document.
