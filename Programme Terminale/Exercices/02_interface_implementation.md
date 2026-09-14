# Chapitre 2 — Interface et implémentation
## Fiche d'exercices

*Terminale NSI — Python 3*

---

### Exercice 1 — Vocabulaire

1. Définir en une phrase ce qu'est l'interface d'une structure de données.
2. Définir en une phrase ce qu'est une implémentation.
3. Une pile et une file ont-elles la même interface ? Justifier.

### Exercice 2 — Spécifier avant d'implémenter

On souhaite créer une structure `EnsembleBorne` qui gère un ensemble d'entiers, avec une capacité maximale fixée à la construction.

Écrire la spécification (l'interface) de cette structure : lister les opérations nécessaires (au minimum : ajouter un élément, tester la présence d'un élément, connaître le nombre d'éléments) avec, pour chacune, son nom, ses paramètres et une description en une phrase de son effet. **Ne pas écrire de code** pour cet exercice : il s'agit uniquement de rédiger la spécification.

### Exercice 3 — Une deuxième implémentation de la pile

En vous inspirant de `PileListe` vue en cours, écrire une classe `PileChainee` qui implémente l'interface d'une pile (`empiler`, `depiler`, `sommet`, `est_vide`) à l'aide d'une **liste chaînée** : chaque élément est stocké dans un petit objet `Maillon` possédant une valeur et une référence vers le maillon suivant, et la pile ne garde qu'une référence vers le sommet.

*Indication :*
```python
class Maillon:
    def __init__(self, valeur, suivant=None):
        self.valeur = valeur
        self.suivant = suivant
```

### Exercice 4 — Comparer deux implémentations d'une file

1. Recopier `FileListe` et `FileDeuxPiles` du cours.
2. Écrire un petit programme qui enfile les entiers de 1 à 5 puis les défile tous, avec chacune des deux implémentations, et vérifier que le résultat est identique.
3. Expliquer pourquoi, malgré ce résultat identique, ces deux implémentations n'ont pas le même coût en pratique.

### Exercice 5 — Une pile bornée avec vérification

Écrire une classe `PileBornee` qui implémente l'interface d'une pile, mais lève une exception `OverflowError` si l'on tente d'empiler alors que la pile a atteint une capacité maximale donnée au constructeur.

### Exercice 6 — Utiliser une pile sans connaître son implémentation

On donne la fonction suivante, qui ne dépend que de l'**interface** d'une pile :

```python
def parenthesage_correct(expression, pile):
    for caractere in expression:
        if caractere == "(":
            pile.empiler(caractere)
        elif caractere == ")":
            if pile.est_vide():
                return False
            pile.depiler()
    return pile.est_vide()
```

1. Tester cette fonction avec `PileListe()` sur les expressions `"(()())"` et `"(()"`.
2. Tester cette même fonction avec `PileTableauFixe(10)`. Le résultat change-t-il ? Pourquoi ?
3. Que se passe-t-il si l'on teste avec `PileTableauFixe(2)` sur une expression contenant plus de deux parenthèses ouvrantes imbriquées ? Expliquer.

---

## Corrigés

### Exercice 1

1. L'interface d'une structure de données est l'ensemble des opérations qu'elle propose, avec leur nom et leur effet attendu, sans préciser comment elles sont réalisées.
2. Une implémentation est une réalisation concrète (un code) de ces opérations, qui précise comment les données sont effectivement stockées et manipulées.
3. Non : une pile propose `empiler`/`depiler` selon le principe LIFO, une file propose `enfiler`/`defiler` selon le principe FIFO. Les noms et le comportement des opérations diffèrent, même si les deux structures se ressemblent par ailleurs (ajout/retrait d'éléments un par un).

### Exercice 2

```
EnsembleBorne(capacite) : construit un ensemble vide pouvant contenir au plus `capacite` éléments.
ajouter(e) : ajoute l'entier e à l'ensemble s'il n'y est pas déjà et si la capacité n'est pas atteinte ;
             ne fait rien si e est déjà présent ; lève une erreur si la capacité est atteinte.
contient(e) : renvoie True si e appartient à l'ensemble, False sinon.
taille() : renvoie le nombre d'éléments actuellement dans l'ensemble.
```

### Exercice 3

```python
class Maillon:
    def __init__(self, valeur, suivant=None):
        self.valeur = valeur
        self.suivant = suivant

class PileChainee:
    def __init__(self):
        self._sommet = None

    def empiler(self, e):
        self._sommet = Maillon(e, self._sommet)

    def depiler(self):
        if self.est_vide():
            raise IndexError("dépiler sur une pile vide")
        valeur = self._sommet.valeur
        self._sommet = self._sommet.suivant
        return valeur

    def sommet(self):
        if self.est_vide():
            raise IndexError("sommet sur une pile vide")
        return self._sommet.valeur

    def est_vide(self):
        return self._sommet is None
```

### Exercice 4

3. Bien que le résultat produit soit identique, `FileListe.defiler()` décale tous les éléments restants à chaque appel (coût proportionnel à la taille de la file), alors que `FileDeuxPiles` ne déplace chaque élément qu'une seule fois de `_entree` vers `_sortie` sur toute sa durée de vie (coût *amorti* constant par opération). Sur une file de grande taille, `FileDeuxPiles` est donc bien plus efficace.

### Exercice 5

```python
class PileBornee:
    def __init__(self, capacite):
        self._capacite = capacite
        self._elements = []

    def empiler(self, e):
        if len(self._elements) == self._capacite:
            raise OverflowError("pile pleine")
        self._elements.append(e)

    def depiler(self):
        if self.est_vide():
            raise IndexError("dépiler sur une pile vide")
        return self._elements.pop()

    def sommet(self):
        if self.est_vide():
            raise IndexError("sommet sur une pile vide")
        return self._elements[-1]

    def est_vide(self):
        return len(self._elements) == 0
```

### Exercice 6

1. `parenthesage_correct("(()())", PileListe())` renvoie `True` ; `parenthesage_correct("(()", PileListe())` renvoie `False`.
2. Le résultat ne change pas avec `PileTableauFixe(10)` : la fonction n'utilise que l'interface commune (`empiler`, `depiler`, `est_vide`), donc son comportement est identique quelle que soit l'implémentation utilisée, tant que la capacité n'est pas dépassée.
3. Avec `PileTableauFixe(2)` et plus de deux parenthèses ouvrantes imbriquées, l'appel à `empiler` lève une `OverflowError` : cette implémentation a une capacité fixe, contrairement à `PileListe`. Ceci illustre une limite concrète : deux implémentations d'une même interface peuvent avoir des comportements limites différents (ici, la gestion de la saturation), même si leur comportement « normal » est identique.
