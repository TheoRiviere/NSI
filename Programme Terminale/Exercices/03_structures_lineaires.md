# Chapitre 3 — Structures linéaires
## Fiche d'exercices

*Terminale NSI — Python 3*

---

### Exercice 1 — Liste chaînée : compléments

En reprenant les classes `Maillon` et `ListeChainee` du cours :

1. Écrire une méthode `inserer_apres(self, valeur_ref, valeur)` qui insère `valeur` juste après le premier maillon contenant `valeur_ref` (ne rien faire si `valeur_ref` n'est pas trouvée).
2. Écrire une méthode `longueur_recursive(self)` qui calcule la taille de la liste **récursivement**, sans utiliser l'attribut `_taille`.
3. Écrire une méthode `inverser(self)` qui inverse l'ordre de la liste chaînée **en place**, en manipulant uniquement les références `suivant` (sans créer de nouveaux maillons, sans passer par une liste Python intermédiaire).

### Exercice 2 — Piles/files avec liste chaînée

1. Rappeler pourquoi une pile s'implémente naturellement et efficacement avec une liste chaînée simple, en n'insérant/supprimant qu'en tête.
2. Expliquer pourquoi une file, elle, nécessite de garder une référence supplémentaire vers la queue de la liste chaînée pour rester efficace.

### Exercice 3 — Dictionnaires

On dispose d'un texte sous forme de chaîne de caractères.

1. Écrire une fonction `compter_mots(texte)` qui renvoie un dictionnaire associant chaque mot du texte (en minuscules) à son nombre d'occurrences. On pourra utiliser `texte.lower().split()`.
2. Écrire une fonction `mot_le_plus_frequent(texte)` qui renvoie le mot le plus fréquent du texte, en s'appuyant sur `compter_mots`.
3. Comparer, en une phrase, le coût de cette approche avec une approche qui utiliserait une liste de `(mot, nombre)` et rechercherait le mot par parcours à chaque occurrence.

### Exercice 4 — Choisir la bonne structure

Pour chacune des situations suivantes, indiquer la structure la plus adaptée (pile, file, liste chaînée, tableau, ou dictionnaire) et justifier :

1. Gérer l'historique de navigation d'un navigateur web, avec un retour possible à la page précédente.
2. Gérer une file d'attente de tickets à traiter dans l'ordre d'arrivée.
3. Associer à chaque élève de la classe sa moyenne, avec des recherches fréquentes par nom.
4. Défaire (`Ctrl+Z`) les dernières actions effectuées dans un éditeur de texte.

### Exercice 5 — Fusionner deux dictionnaires

Écrire une fonction `fusionner(d1, d2)` qui renvoie un nouveau dictionnaire contenant toutes les clés de `d1` et `d2`. En cas de clé commune, on additionnera les deux valeurs (on suppose qu'elles sont numériques).

---

## Corrigés

### Exercice 1

```python
class Maillon:
    def __init__(self, valeur, suivant=None):
        self.valeur = valeur
        self.suivant = suivant

class ListeChainee:
    def __init__(self):
        self._tete = None
        self._taille = 0

    def inserer_tete(self, valeur):
        self._tete = Maillon(valeur, self._tete)
        self._taille += 1

    def inserer_apres(self, valeur_ref, valeur):
        courant = self._tete
        while courant is not None:
            if courant.valeur == valeur_ref:
                courant.suivant = Maillon(valeur, courant.suivant)
                self._taille += 1
                return
            courant = courant.suivant

    def longueur_recursive(self):
        def aux(maillon):
            if maillon is None:
                return 0
            return 1 + aux(maillon.suivant)
        return aux(self._tete)

    def inverser(self):
        precedent = None
        courant = self._tete
        while courant is not None:
            suivant = courant.suivant
            courant.suivant = precedent
            precedent = courant
            courant = suivant
        self._tete = precedent

    def vers_liste_python(self):
        resultat = []
        courant = self._tete
        while courant is not None:
            resultat.append(courant.valeur)
            courant = courant.suivant
        return resultat
```

### Exercice 2

1. Insérer ou supprimer en tête d'une liste chaînée ne nécessite que de modifier une référence (celle de la tête, et celle du nouveau maillon) : ce coût est constant, indépendant du nombre d'éléments, ce qui correspond exactement au besoin d'une pile (`empiler`/`depiler` en LIFO).
2. Pour une file, il faut insérer d'un côté et retirer de l'autre. Retirer en tête reste en temps constant, mais **insérer en queue** nécessiterait, sans référence sur la queue, de parcourir toute la liste jusqu'au dernier maillon (coût proportionnel à la taille). En gardant une référence supplémentaire vers le dernier maillon, on retrouve un coût constant pour l'insertion en queue également.

### Exercice 3

```python
def compter_mots(texte):
    compteur = {}
    for mot in texte.lower().split():
        if mot in compteur:
            compteur[mot] = compteur[mot] + 1
        else:
            compteur[mot] = 1
    return compteur

def mot_le_plus_frequent(texte):
    compteur = compter_mots(texte)
    meilleur_mot = None
    meilleur_nombre = 0
    for mot, nombre in compteur.items():
        if nombre > meilleur_nombre:
            meilleur_mot = mot
            meilleur_nombre = nombre
    return meilleur_mot
```

3. Avec un dictionnaire, retrouver et mettre à jour le compteur d'un mot se fait en coût quasi constant grâce à l'accès direct par clé, alors qu'avec une liste de couples il faudrait parcourir la liste à chaque mot pour savoir s'il y est déjà, ce qui rend l'approche globale bien plus coûteuse sur un texte long.

### Exercice 4

1. Pile : le retour à la page précédente suit un ordre LIFO (la dernière page visitée est la première à laquelle on revient).
2. File : les tickets doivent être traités dans leur ordre d'arrivée (FIFO).
3. Dictionnaire : recherche fréquente par une clé (le nom de l'élève).
4. Pile : défaire annule les actions dans l'ordre inverse de leur exécution (LIFO).

### Exercice 5

```python
def fusionner(d1, d2):
    resultat = dict(d1)
    for cle, valeur in d2.items():
        if cle in resultat:
            resultat[cle] = resultat[cle] + valeur
        else:
            resultat[cle] = valeur
    return resultat
```
