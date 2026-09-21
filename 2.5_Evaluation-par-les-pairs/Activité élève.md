Parcours séquentiel et recherche dichotomique
## Fiche d'exercices

*Première NSI*

*A réaliser sur Visual Studio Code*

*Un fichier par exercice.* 

*Les fichiers seront zipé dans une archive et envoyé au professeur*

---

### Exercice 1 — Parcours séquentiel

1. Écrire une fonction `minimum(tableau)` qui renvoie la plus petite valeur d'un tableau non vide (sur le modèle de `maximum` du cours).
2. Écrire une fonction `compter_occurrences(tableau, valeur)` qui renvoie le nombre de fois où `valeur` apparaît dans `tableau`.
3. Vérifier que `compter_occurrences([1, 2, 2, 3, 2], 2)` renvoie `3`.

### Exercice 2 — Invariant de boucle

On donne la fonction suivante, censée calculer la somme des éléments d'un tableau :
```python
def somme(tableau):
    s = 0
    for x in tableau:
        s = s + x
    return s
```

1. Proposer un invariant de boucle pour cette fonction (à quoi correspond `s`, à un instant donné de la boucle, par rapport aux éléments déjà parcourus ?).
2. Vérifier que cet invariant est vrai avant la première itération (initialisation).
3. Vérifier qu'il reste vrai après chaque itération (conservation).
4. En déduire, à la fin de la boucle, que `s` contient bien la somme de **tous** les éléments du tableau.

### Exercice 3 — Recherche dichotomique : tracer à la main

On donne le tableau trié `t = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]` (indices de 0 à 9).

1. Dérouler à la main l'algorithme `recherche_dichotomique` du cours pour rechercher la valeur `18`. Donner, à chaque itération, les valeurs de `gauche`, `droite`, `milieu`, et la comparaison effectuée.
2. Combien d'itérations (donc de comparaisons) ont été nécessaires ?
3. Dérouler de même la recherche de la valeur `5` (absente du tableau). Que se passe-t-il, et quel est le résultat renvoyé ?

### Exercice 4 — Comparer les coûts

1. Modifier `recherche_dichotomique` du cours pour qu'elle renvoie, en plus de l'indice trouvé (ou -1), le **nombre de comparaisons** effectuées (fonction `recherche_dichotomique_compte`).
2. Pour un tableau trié de taille `10`, rechercher la valeur `14` (troisième position en partant de la fin) et noter le nombre de comparaisons obtenu.
3. Pour ce même tableau, rechercher une valeur absente (`5`) et noter le nombre de comparaisons. Ce nombre est-il très différent du cas précédent ? Est-ce cohérent avec ce que vous savez du coût de la recherche dichotomique (de l'ordre de `log₂(n)`, quel que soit le résultat) ?

---

## Corrigés

### Exercice 1

1-2-3.
```python
def minimum(tableau):
    m = tableau[0]
    for x in tableau[1:]:
        if x < m:
            m = x
    return m

def compter_occurrences(tableau, valeur):
    compte = 0
    for x in tableau:
        if x == valeur:
            compte += 1
    return compte

compter_occurrences([1, 2, 2, 3, 2], 2)   # 3
```

### Exercice 2

1. **Invariant proposé :** à chaque étape de la boucle, `s` contient la somme de tous les éléments du tableau **déjà parcourus**.
2. **Initialisation :** avant la boucle, `s = 0`, et aucun élément n'a encore été parcouru ; la somme des éléments déjà parcourus (un ensemble vide) est bien `0`. L'invariant est vrai.
3. **Conservation :** supposons l'invariant vrai avant de traiter un nouvel élément `x`. Après l'instruction `s = s + x`, `s` contient l'ancienne somme (celle des éléments déjà parcourus avant `x`) plus `x` lui-même, ce qui est bien la somme de tous les éléments parcourus jusqu'ici, `x` inclus. L'invariant reste donc vrai.
4. À la fin de la boucle, tous les éléments du tableau ont été parcourus. D'après l'invariant, `s` contient donc la somme de **tous** les éléments du tableau, ce qui est bien le résultat attendu de la fonction `somme`.

### Exercice 3

1. Recherche de `18` dans `t = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]` :
   - `gauche=0, droite=9, milieu=4` → `t[4]=10 < 18` → `gauche=5`
   - `gauche=5, droite=9, milieu=7` → `t[7]=16 < 18` → `gauche=8`
   - `gauche=8, droite=9, milieu=8` → `t[8]=18` → trouvé, on renvoie `8`.
2. **3 itérations** (donc 3 comparaisons) ont été nécessaires.
3. Recherche de `5` :
   - `gauche=0, droite=9, milieu=4` → `t[4]=10 > 5` → `droite=3`
   - `gauche=0, droite=3, milieu=1` → `t[1]=4 < 5` → `gauche=2`
   - `gauche=2, droite=3, milieu=2` → `t[2]=6 > 5` → `droite=1`
   - `gauche=2, droite=1` → `gauche > droite`, la boucle s'arrête : on renvoie `-1` (valeur absente), après **3 comparaisons**.

### Exercice 4

1.
```python
def recherche_dichotomique_compte(tableau_trie, valeur):
    gauche, droite = 0, len(tableau_trie) - 1
    nb_comparaisons = 0
    while gauche <= droite:
        milieu = (gauche + droite) // 2
        nb_comparaisons += 1
        if tableau_trie[milieu] == valeur:
            return milieu, nb_comparaisons
        elif tableau_trie[milieu] < valeur:
            gauche = milieu + 1
        else:
            droite = milieu - 1
    return -1, nb_comparaisons
```
2. `recherche_dichotomique_compte(t, 14)` renvoie `(6, 4)` : l'indice `6`, en `4` comparaisons.
3. `recherche_dichotomique_compte(t, 5)` renvoie `(-1, 3)` : la valeur est absente, détectée en `3` comparaisons. Ce nombre est effectivement très **proche** du cas précédent (3 contre 4, sur un tableau de taille 10) : c'est cohérent avec le coût théorique en `log₂(n)`, qui borne le nombre de comparaisons **dans le pire des cas**, que la valeur recherchée soit présente ou non — la dichotomie élimine toujours environ la moitié des éléments restants à chaque étape, indépendamment du résultat final.