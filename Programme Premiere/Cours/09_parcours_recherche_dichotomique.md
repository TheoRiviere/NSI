# Chapitre 9 — Parcours séquentiel et recherche dichotomique

## Objectifs

- Écrire et justifier des algorithmes de parcours séquentiel (recherche, extremum, moyenne).
- Comprendre et démontrer la correction d'un algorithme à l'aide d'un invariant de boucle.
- Écrire l'algorithme de recherche dichotomique et justifier sa terminaison à l'aide d'un variant de boucle.
- Comparer le coût de la recherche séquentielle et de la recherche dichotomique.

## Prérequis

- Tableaux (listes) — chapitre 2.
- Boucles `for` et `while`.

---

## 1. Le parcours séquentiel

Un **parcours séquentiel** consiste à examiner, un par un et dans l'ordre, tous les éléments d'un tableau, pour y effectuer un traitement (rechercher une valeur, calculer une statistique...).

### 1.1 Recherche d'une valeur (recherche linéaire)

```python
def recherche_lineaire(tableau, valeur):
    """Renvoie l'indice de la première occurrence de valeur dans tableau,
    ou -1 si elle n'y figure pas."""
    for i in range(len(tableau)):
        if tableau[i] == valeur:
            return i
    return -1
```

Cet algorithme fonctionne sur un tableau **quelconque**, trié ou non : il n'existe aucune hypothèse permettant de faire mieux qu'examiner, dans le pire des cas, tous les éléments (si la valeur ne figure pas dans le tableau, ou figure à la toute fin, on est bien obligé de tous les regarder).

### 1.2 Recherche de l'extremum

```python
def maximum(tableau):
    """Renvoie la plus grande valeur du tableau (non vide)."""
    m = tableau[0]
    for x in tableau[1:]:
        if x > m:
            m = x
    return m
```

### 1.3 Calcul d'une moyenne

```python
def moyenne(tableau):
    """Renvoie la moyenne arithmétique des valeurs du tableau (non vide)."""
    return sum(tableau) / len(tableau)
```

---

## 2. Prouver la correction avec un invariant de boucle

### 2.1 La notion d'invariant de boucle

Comment être certain qu'un algorithme itératif comme `maximum` calcule bien ce qu'il prétend calculer, pour **toutes** les entrées possibles, et pas seulement pour les quelques exemples que l'on a testés ? Une méthode rigoureuse consiste à identifier un **invariant de boucle** : une propriété qui est vraie **avant** la boucle, qui reste vraie **après chaque itération**, et qui, combinée à la condition d'arrêt de la boucle, permet de conclure que le résultat final est correct.

### 2.2 Exemple : preuve de `maximum`

**Invariant proposé :** *à chaque étape de la boucle, `m` contient la plus grande valeur parmi les éléments du tableau déjà examinés.*

- **Initialisation :** avant la boucle, `m = tableau[0]`. Le seul élément « déjà examiné » est `tableau[0]` lui-même, et `m` en contient bien la plus grande valeur (trivialement, puisqu'il n'y en a qu'un). L'invariant est donc vrai au départ.
- **Conservation :** supposons l'invariant vrai avant d'examiner un nouvel élément `x`. Si `x > m`, alors `m` est mis à jour à `x`, qui est bien la plus grande valeur parmi les éléments examinés jusqu'ici (les précédents, dont le maximum était l'ancien `m`, plus `x` qui le dépasse). Si `x <= m`, `m` reste inchangé et demeure bien le maximum des éléments examinés (puisque `x` ne le dépasse pas). Dans les deux cas, l'invariant reste vrai après cette itération.
- **Terminaison et conclusion :** la boucle s'arrête lorsque tous les éléments du tableau ont été examinés. À ce moment, d'après l'invariant, `m` contient la plus grande valeur parmi **tous** les éléments du tableau — ce qui est exactement le résultat attendu.

Cette démarche (initialisation, conservation, conclusion à la fin de la boucle) est une méthode générale pour prouver rigoureusement la **correction** d'un algorithme itératif, indépendamment des tests que l'on pourrait effectuer.

---

## 3. La recherche dichotomique

### 3.1 Principe

Lorsque le tableau est **trié**, on peut faire beaucoup mieux que la recherche linéaire : la **recherche dichotomique** (ou recherche par dichotomie) consiste à comparer la valeur recherchée à l'élément **central** du tableau, ce qui permet d'éliminer, à chaque étape, la **moitié** des éléments restants (ceux qui ne peuvent pas contenir la valeur, puisque le tableau est trié).

```python
def recherche_dichotomique(tableau_trie, valeur):
    """Renvoie l'indice de valeur dans tableau_trie (trié), ou -1 si absente."""
    gauche, droite = 0, len(tableau_trie) - 1
    while gauche <= droite:
        milieu = (gauche + droite) // 2
        if tableau_trie[milieu] == valeur:
            return milieu
        elif tableau_trie[milieu] < valeur:
            gauche = milieu + 1
        else:
            droite = milieu - 1
    return -1
```

À chaque tour de boucle, on compare `valeur` à l'élément central de la portion de tableau encore « en jeu » (délimitée par `gauche` et `droite`). Si l'élément central est trop petit, la valeur recherchée ne peut se trouver qu'à sa droite ; s'il est trop grand, elle ne peut se trouver qu'à sa gauche. On restreint ainsi progressivement la zone de recherche, jusqu'à trouver la valeur ou jusqu'à ce que la zone de recherche devienne vide (`gauche > droite`).

### 3.2 Prouver la terminaison avec un variant de boucle

Pour une boucle `while`, il faut aussi s'assurer qu'elle **se termine** bien (et ne tourne pas indéfiniment). On utilise pour cela un **variant de boucle** : une quantité entière positive ou nulle qui **diminue strictement** à chaque itération, ce qui garantit que la boucle finira par s'arrêter (une quantité entière positive ne peut pas décroître indéfiniment).

**Variant proposé pour la recherche dichotomique :** la quantité `droite - gauche` (la taille de la zone de recherche restante).

- À chaque itération qui ne trouve pas la valeur, soit `gauche` **augmente** strictement (passe à `milieu + 1`), soit `droite` **diminue** strictement (passe à `milieu - 1`) — dans les deux cas, `droite - gauche` **diminue strictement**.
- Cette quantité est toujours un entier, et la boucle s'arrête dès que `gauche > droite`, c'est-à-dire dès que cette quantité devient négative.

Comme une suite d'entiers strictement décroissante ne peut pas décroître indéfiniment sans finir par sortir de son domaine de validité, la boucle se termine nécessairement, en un nombre fini d'étapes.

### 3.3 Coût de la recherche dichotomique

Puisque chaque itération élimine environ la **moitié** des éléments restants, le nombre d'itérations nécessaires pour un tableau de `n` éléments est de l'ordre de `log₂(n)` — un nombre qui croît beaucoup plus lentement que `n` lui-même.

| Taille du tableau | Recherche linéaire (pire cas) | Recherche dichotomique (pire cas, approx.) |
|---|---|---|
| 10 | 10 comparaisons | ~4 comparaisons |
| 1 000 | 1 000 comparaisons | ~10 comparaisons |
| 1 000 000 | 1 000 000 comparaisons | ~20 comparaisons |

Cette différence devient considérable pour de grands tableaux : c'est pour cette raison qu'il est souvent avantageux de **trier** un tableau une fois pour toutes (voir le chapitre suivant sur les algorithmes de tri) si l'on doit ensuite y effectuer de nombreuses recherches.

**Condition indispensable :** la recherche dichotomique ne fonctionne **que** sur un tableau trié. L'appliquer à un tableau non trié produirait un résultat incorrect (ou une non-détection erronée), car le raisonnement « éliminer une moitié » repose entièrement sur l'ordre des éléments.

---

## Synthèse

| Algorithme | Principe | Coût (pire cas) | Prérequis |
|---|---|---|---|
| Recherche linéaire | Examine les éléments un par un | de l'ordre de `n` | aucun |
| Maximum / moyenne | Parcours séquentiel avec accumulation | de l'ordre de `n` | tableau non vide |
| Recherche dichotomique | Élimine la moitié des éléments à chaque étape | de l'ordre de `log₂(n)` | tableau **trié** |
| Invariant de boucle | Propriété vraie avant, après chaque itération | outil de preuve de **correction** | — |
| Variant de boucle | Quantité entière strictement décroissante | outil de preuve de **terminaison** | — |

*Prochaine étape suggérée : Chapitre 10 — Tris par insertion et par sélection.*
