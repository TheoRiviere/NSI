# Chapitre 10 — Calculabilité, modularité, paradigmes et qualité de programmation
## Fiche d'exercices

*Terminale NSI — Python 3*

---

### Exercice 1 — Programme comme donnée

1. Donner deux exemples de logiciels qui manipulent des programmes comme de simples données, sans les exécuter.
2. En quoi un interpréteur Python traite-t-il différemment un programme, par rapport à ces logiciels ?

### Exercice 2 — Le problème de l'arrêt

1. Énoncer, avec ses propres mots, le problème de l'arrêt.
2. Dans l'argument vu en cours, pourquoi construit-on spécifiquement un programme `paradoxe` qui s'appelle **lui-même** en entrée (`paradoxe(paradoxe)`) plutôt que sur un autre programme quelconque ?
3. Le fait que le problème de l'arrêt soit indécidable signifie-t-il qu'on ne peut *jamais* savoir si un programme particulier termine ? Justifier votre réponse.

### Exercice 3 — Modularité

On donne le module suivant, `statistiques.py` :
```python
"""Fonctions statistiques simples."""

def moyenne(valeurs):
    """Renvoie la moyenne d'une liste de nombres non vide."""
    return sum(valeurs) / len(valeurs)

def variance(valeurs):
    """Renvoie la variance d'une liste de nombres non vide."""
    m = moyenne(valeurs)
    return sum((x - m) ** 2 for x in valeurs) / len(valeurs)
```

1. Écrire le code qui importe ce module et affiche la moyenne et la variance de `[10, 12, 8, 14, 6]`.
2. Ajouter au module une fonction `ecart_type(valeurs)` qui renvoie la racine carrée de la variance (on utilisera le module `math`).
3. Pourquoi est-il utile que chaque fonction du module comporte une docstring ?

### Exercice 4 — Paradigmes

Pour chacun des extraits suivants, indiquer le paradigme dominant (impératif, fonctionnel ou objet) :

```python
# Extrait A
resultat = [x * 2 for x in range(10) if x % 2 == 0]

# Extrait B
class Compteur:
    def __init__(self):
        self.valeur = 0
    def incrementer(self):
        self.valeur += 1

# Extrait C
n = 0
while n < 10:
    print(n)
    n = n + 1
```

### Exercice 5 — Trouver et corriger le bug

Pour chacune des fonctions suivantes, identifier la cause du bug (parmi celles vues en cours) et proposer une correction.

```python
# Fonction 1
def moyenne_ou_zero(valeurs):
    if len(valeurs) > 0:
        m = sum(valeurs) / len(valeurs)
    return m

# Fonction 2
def dernier_element(tableau):
    return tableau[len(tableau)]

# Fonction 3
def est_environ_egal_a_un(x):
    return x == 1.0
```

---

## Corrigés

### Exercice 1

1. Un logiciel de transfert de fichiers, un antivirus (qui analyse un fichier exécutable sans l'exécuter), un système de gestion de versions, un service de stockage en ligne.
2. Un interpréteur ne se contente pas de stocker ou de transmettre le programme : il le **lit et l'exécute**, instruction par instruction, en produisant les effets que ce programme décrit.

### Exercice 2

1. Il n'existe aucun programme capable de déterminer, pour tout programme et toute entrée donnés, si ce programme s'arrête ou non sur cette entrée.
2. Cette auto-référence est ce qui permet de construire la contradiction : en demandant à `paradoxe` de se comporter à l'opposé de ce que prédit `arret` **sur lui-même**, on obtient une situation où la prédiction de `arret` est nécessairement fausse, quel que soit son résultat.
3. Non : on peut très bien démontrer que certains programmes particuliers terminent (par exemple avec un variant décroissant, chapitre 6) ou ne terminent pas. L'indécidabilité du problème de l'arrêt signifie qu'il n'existe **pas de méthode générale et automatique** qui fonctionnerait pour **tous** les programmes possibles — pas qu'on ne peut rien démontrer au cas par cas.

### Exercice 3

```python
import statistiques

valeurs = [10, 12, 8, 14, 6]
print(statistiques.moyenne(valeurs))
print(statistiques.variance(valeurs))
```

2.
```python
import math

def ecart_type(valeurs):
    """Renvoie l'écart-type d'une liste de nombres non vide."""
    return math.sqrt(variance(valeurs))
```

3. La docstring décrit l'**interface** de chaque fonction (ce qu'elle fait, ce qu'elle attend en entrée, ce qu'elle renvoie) sans qu'il soit nécessaire de lire son implémentation : c'est indispensable pour qu'une autre personne (ou soi-même, plus tard) puisse utiliser le module correctement et rapidement.

### Exercice 4

- Extrait A : paradigme **fonctionnel** (compréhension de liste, sans variable modifiée pas à pas).
- Extrait B : paradigme **objet** (classe, attribut, méthode).
- Extrait C : paradigme **impératif** (boucle avec modification explicite d'une variable d'état).

### Exercice 5

**Fonction 1.** Instruction conditionnelle non exhaustive : si `valeurs` est vide, `m` n'est jamais défini, ce qui provoque une erreur `UnboundLocalError` à la ligne `return m`.
```python
def moyenne_ou_zero(valeurs):
    if len(valeurs) > 0:
        return sum(valeurs) / len(valeurs)
    else:
        return 0
```

**Fonction 2.** Débordement de tableau : `tableau[len(tableau)]` est hors des indices valides (le dernier indice valide est `len(tableau) - 1`).
```python
def dernier_element(tableau):
    return tableau[len(tableau) - 1]   # ou plus simplement tableau[-1]
```

**Fonction 3.** Comparaison de flottants par égalité stricte, qui peut échouer à cause des arrondis (par exemple si `x` vaut `0.999999999999` suite à un calcul).
```python
def est_environ_egal_a_un(x):
    return abs(x - 1.0) < 1e-9
```
