# Terminale NSI — Chapitre 3
# Structures linéaires : listes chaînées, piles, files, dictionnaires

*Support de cours — Python 3*

---

## Objectifs du chapitre

- Manipuler une liste chaînée : insertion, suppression, parcours, recherche.
- Consolider les notions de pile (LIFO) et de file (FIFO) vues au chapitre 2.
- Comprendre la structure de dictionnaire par la notion d'index et de clé.
- Choisir la structure linéaire adaptée à une situation donnée.

**Prérequis :** chapitre 2 (interface/implémentation, pile, file).

---

## 3.1 La liste chaînée

Une **liste chaînée** est une structure où chaque élément (appelé **maillon** ou **nœud**) contient une valeur et une référence vers l'élément suivant. Contrairement à un tableau Python (`list`), les éléments ne sont pas nécessairement contigus en mémoire.

```python
class Maillon:
    def __init__(self, valeur, suivant=None):
        self.valeur = valeur
        self.suivant = suivant
```

Une liste chaînée se manipule à partir d'une référence vers son premier maillon (la **tête**) :

```python
class ListeChainee:
    def __init__(self):
        self._tete = None
        self._taille = 0

    def est_vide(self):
        return self._tete is None

    def taille(self):
        return self._taille

    def inserer_tete(self, valeur):
        self._tete = Maillon(valeur, self._tete)
        self._taille += 1

    def inserer_queue(self, valeur):
        nouveau = Maillon(valeur)
        if self.est_vide():
            self._tete = nouveau
        else:
            courant = self._tete
            while courant.suivant is not None:
                courant = courant.suivant
            courant.suivant = nouveau
        self._taille += 1

    def contient(self, valeur):
        courant = self._tete
        while courant is not None:
            if courant.valeur == valeur:
                return True
            courant = courant.suivant
        return False

    def supprimer(self, valeur):
        precedent = None
        courant = self._tete
        while courant is not None:
            if courant.valeur == valeur:
                if precedent is None:
                    self._tete = courant.suivant
                else:
                    precedent.suivant = courant.suivant
                self._taille -= 1
                return True
            precedent = courant
            courant = courant.suivant
        return False

    def vers_liste_python(self):
        resultat = []
        courant = self._tete
        while courant is not None:
            resultat.append(courant.valeur)
            courant = courant.suivant
        return resultat
```

**Exemple d'utilisation :**

```python
l = ListeChainee()
l.inserer_tete(2)
l.inserer_tete(1)
l.inserer_queue(3)
print(l.vers_liste_python())   # [1, 2, 3]
print(l.contient(2))           # True
l.supprimer(2)
print(l.vers_liste_python())   # [1, 3]
```

### Coût des opérations

| Opération | Liste chaînée | Liste Python (`list`) |
|---|---|---|
| Insertion en tête | rapide (temps constant) | lente (décalage de tous les éléments) |
| Insertion en queue (sans référence sur la queue) | lente (il faut parcourir toute la liste) | rapide (`append`) |
| Accès au `i`-ième élément | lent (il faut parcourir depuis la tête) | rapide (accès direct par indice) |
| Recherche d'une valeur | lente (parcours) | lente (parcours) |

> **À retenir.** Une liste chaînée est efficace pour des insertions/suppressions fréquentes en tête, mais perd l'accès direct par indice qu'offre un tableau. Le choix de structure dépend donc des opérations les plus fréquentes dans le programme.

---

## 3.2 Rappel — Piles et files

Vues au chapitre 2, ces deux structures peuvent être implémentées à partir d'une liste chaînée :

- une **pile** (LIFO) correspond exactement à une liste chaînée où l'on n'insère et ne supprime qu'en **tête** (`inserer_tete` / suppression de la tête) : ces deux opérations sont en temps constant, ce qui en fait une implémentation naturelle et efficace ;
- une **file** (FIFO) nécessite d'insérer d'un côté et de retirer de l'autre : avec une liste simplement chaînée comme ci-dessus, il faut garder en plus une référence vers la **queue** pour que l'insertion en queue soit, elle aussi, en temps constant.

---

## 3.3 Dictionnaires : index et clé

Un **dictionnaire** (`dict` en Python) associe à chaque **clé** une **valeur**. Contrairement à un tableau où l'on accède à un élément par sa **position** (un indice entier), un dictionnaire permet d'accéder à une valeur directement par sa **clé**, quelle que soit sa nature (chaîne de caractères, nombre, etc.).

```python
ages = {"Ada": 17, "Alan": 18, "Grace": 17}

print(ages["Ada"])       # accès direct par clé : 17
ages["Katherine"] = 18   # ajout d'une nouvelle clé
del ages["Alan"]         # suppression d'une clé

for cle, valeur in ages.items():
    print(cle, "->", valeur)
```

### Pourquoi l'accès par clé est rapide

En interne, un dictionnaire Python utilise une **table de hachage** : une fonction associe à chaque clé un **index** dans un tableau, ce qui permet de retrouver la valeur associée sans avoir à parcourir tous les éléments. C'est ce qui rend, **en moyenne**, la recherche dans un dictionnaire beaucoup plus rapide que la recherche dans une liste.

| Recherche d'une valeur | Coût moyen |
|---|---|
| Dans une liste (`valeur in liste`) | parcours de la liste : coût proportionnel au nombre d'éléments |
| Dans un dictionnaire (`cle in dictionnaire`) | accès direct via l'index calculé à partir de la clé : coût quasi constant |

> **Illustration.** Rechercher si un mot appartient à un dictionnaire de 100 000 mots est quasi instantané, alors que la même recherche dans une liste de 100 000 mots nécessite, dans le pire des cas, de comparer le mot à chercher avec chacun des 100 000 mots.

```python
mots_valides = {"chat", "chien", "oiseau"}   # un ensemble, cousin du dictionnaire (uniquement des clés)

def est_valide(mot):
    return mot in mots_valides   # recherche rapide
```

---

## 3.4 Choisir sa structure linéaire

| Besoin dominant | Structure recommandée |
|---|---|
| Ajouter/retirer uniquement en une seule extrémité, dans l'ordre LIFO | Pile |
| Ajouter à une extrémité, retirer à l'autre, dans l'ordre FIFO | File |
| Accès fréquent par position (indice) | Tableau (liste Python) |
| Insertions/suppressions fréquentes en tête, sans besoin d'accès par indice | Liste chaînée |
| Recherche fréquente par une clé identifiante (nom, identifiant...) | Dictionnaire |

---

## 3.5 Synthèse

| Notion | Définition |
|---|---|
| Maillon / nœud | Élément d'une liste chaînée contenant une valeur et une référence vers le suivant |
| Liste chaînée | Structure linéaire où chaque élément référence le suivant, sans nécessité de contiguïté en mémoire |
| Clé, valeur | Dans un dictionnaire, la clé identifie une valeur et permet d'y accéder directement |
| Index (table de hachage) | Mécanisme interne qui associe une clé à un emplacement, pour un accès rapide |

*Prochaine étape suggérée : chapitre 4, les arbres binaires, qui généralisent l'idée de structure chaînée à une organisation hiérarchique.*
