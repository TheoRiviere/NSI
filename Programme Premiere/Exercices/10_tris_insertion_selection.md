# Chapitre 10 — Tris par insertion et par sélection
## Fiche d'exercices

*Première NSI — Python 3*

---

### Exercice 1 — Tracer les deux tris à la main

1. Dérouler à la main le tri par sélection sur le tableau `[4, 1, 7, 3]` : donner l'état du tableau après chaque étape de la boucle externe.
2. Dérouler à la main le tri par insertion sur le tableau `[9, 3, 6, 1, 2]` : donner l'état du tableau après chaque insertion.
3. Vérifier vos résultats avec `tri_selection` et `tri_insertion` du cours.

### Exercice 2 — Adapter le tri par sélection pour trier en ordre décroissant

1. Écrire une fonction `tri_selection_decroissant(tableau)` qui trie un tableau par ordre **décroissant**, en adaptant `tri_selection` du cours (indication : il suffit de rechercher, à chaque étape, le **maximum** restant plutôt que le minimum).
2. Vérifier que `tri_selection_decroissant([4, 1, 7, 3])` renvoie `[7, 4, 3, 1]`.

### Exercice 3 — Compter les échanges du tri par sélection

1. Modifier `tri_selection` pour qu'elle compte le nombre d'**échanges** réellement effectués (un échange n'a lieu que si `indice_min != i`, sinon l'élément était déjà à sa place et échanger reviendrait à ne rien faire).
2. Appliquer cette version sur un tableau déjà trié, `[1, 2, 3, 4, 5]`. Combien d'échanges sont effectués ? Est-ce cohérent avec l'affirmation du cours selon laquelle le tri par sélection effectue **toujours** le même nombre de *comparaisons*, quel que soit le tableau de départ ? (Bien distinguer *nombre de comparaisons* et *nombre d'échanges*.)
3. Appliquer cette version sur le tableau trié à l'envers `[5, 4, 3, 2, 1]`. Combien d'échanges sont effectués cette fois ?

### Exercice 4 — Meilleur cas du tri par insertion

1. Modifier `tri_insertion` du cours pour qu'elle compte le nombre de **décalages** effectués (chaque passage dans le corps de la boucle `while`).
2. Appliquer cette version sur un tableau déjà trié, `[1, 2, 3, 4, 5]`. Combien de décalages sont effectués ? Pourquoi ce nombre est-il si petit ?
3. Appliquer cette version sur le tableau trié à l'envers `[5, 4, 3, 2, 1]`. Combien de décalages sont effectués ? Comparer avec `n(n-1)/2` pour `n=5`.

---

## Corrigés

### Exercice 1

1. `[4, 1, 7, 3]` → étape 0 : minimum = 1 (indice 1), échange avec indice 0 → `[1, 4, 7, 3]` → étape 1 : minimum parmi `[4,7,3]` = 3 (indice 3), échange avec indice 1 → `[1, 3, 7, 4]` → étape 2 : minimum parmi `[7,4]` = 4 (indice 3), échange avec indice 2 → `[1, 3, 4, 7]`. Résultat : `[1, 3, 4, 7]`.
2. `[9, 3, 6, 1, 2]` → insertion de `3` : `[3, 9, 6, 1, 2]` → insertion de `6` : `[3, 6, 9, 1, 2]` → insertion de `1` : `[1, 3, 6, 9, 2]` → insertion de `2` : `[1, 2, 3, 6, 9]`. Résultat : `[1, 2, 3, 6, 9]`.

### Exercice 2

```python
def tri_selection_decroissant(tableau):
    t = tableau[:]
    n = len(t)
    for i in range(n - 1):
        indice_max = i
        for j in range(i + 1, n):
            if t[j] > t[indice_max]:
                indice_max = j
        t[i], t[indice_max] = t[indice_max], t[i]
    return t

tri_selection_decroissant([4, 1, 7, 3])   # [7, 4, 3, 1]
```

### Exercice 3

1.
```python
def tri_selection_compte_echanges(tableau):
    t = tableau[:]
    n = len(t)
    nb_echanges = 0
    for i in range(n - 1):
        indice_min = i
        for j in range(i + 1, n):
            if t[j] < t[indice_min]:
                indice_min = j
        if indice_min != i:
            t[i], t[indice_min] = t[indice_min], t[i]
            nb_echanges += 1
    return t, nb_echanges
```
2. Sur `[1, 2, 3, 4, 5]` (déjà trié) : **0 échange** (à chaque étape, l'élément minimum trouvé est déjà en position `i`). Cela reste cohérent avec le cours : le nombre de **comparaisons** de la boucle interne (qui parcourt toujours toute la zone restante pour trouver le minimum) ne dépend pas du tableau de départ, mais le nombre d'**échanges** effectivement réalisés, lui, en dépend bien : un tableau déjà trié ne nécessite jamais d'échange, même si l'algorithme continue de faire toutes ses comparaisons.
3. Sur `[5, 4, 3, 2, 1]` : **2 échanges** (le tableau se retrouve trié après l'échange des positions 0↔4 et 1↔3 ; la position 2, contenant déjà `3`, l'élément médian, ne bouge pas).

### Exercice 4

1.
```python
def tri_insertion_compte_decalages(tableau):
    t = tableau[:]
    n = len(t)
    nb_decalages = 0
    for i in range(1, n):
        valeur = t[i]
        j = i - 1
        while j >= 0 and t[j] > valeur:
            t[j + 1] = t[j]
            j -= 1
            nb_decalages += 1
        t[j + 1] = valeur
    return t, nb_decalages
```
2. Sur `[1, 2, 3, 4, 5]` : **0 décalage**. C'est parce qu'à chaque étape, l'élément à insérer est déjà plus grand que tous les éléments qui le précèdent (le tableau est déjà trié), donc la condition `t[j] > valeur` est fausse dès la première comparaison, et la boucle `while` ne s'exécute jamais.
3. Sur `[5, 4, 3, 2, 1]` : **10 décalages**, soit exactement `n(n-1)/2 = 5×4/2 = 10` pour `n=5` — ce tableau constitue bien le pire cas du tri par insertion, où chaque nouvel élément doit être décalé au-delà de tous les éléments déjà en place.
