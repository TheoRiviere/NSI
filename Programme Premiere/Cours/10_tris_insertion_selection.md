# Chapitre 10 — Tris par insertion et par sélection

## Objectifs

- Écrire et justifier (invariant de boucle) le tri par sélection.
- Écrire et justifier le tri par insertion.
- Comprendre pourquoi ces deux algorithmes ont un coût quadratique dans le pire des cas.

## Prérequis

- Parcours séquentiel, invariant de boucle — chapitre 9.
- Tableaux (listes).

---

## 1. Le tri par sélection

### 1.1 Principe

Le **tri par sélection** trie un tableau en répétant le principe suivant : à chaque étape, on recherche le **plus petit élément** parmi ceux qui ne sont pas encore à leur place définitive, et on l'échange avec l'élément situé en première position de cette zone non triée.

```python
def tri_selection(tableau):
    t = tableau[:]           # on travaille sur une copie
    n = len(t)
    for i in range(n - 1):
        indice_min = i
        for j in range(i + 1, n):
            if t[j] < t[indice_min]:
                indice_min = j
        t[i], t[indice_min] = t[indice_min], t[i]   # échange
    return t
```

### 1.2 Déroulement sur un exemple

Pour `[5, 2, 8, 1, 9]` :
- Étape `i=0` : le minimum de `[5, 2, 8, 1, 9]` est `1` (indice 3) → échange avec l'indice 0 → `[1, 2, 8, 5, 9]`
- Étape `i=1` : le minimum de `[2, 8, 5, 9]` (à partir de l'indice 1) est `2`, déjà en place → `[1, 2, 8, 5, 9]`
- Étape `i=2` : le minimum de `[8, 5, 9]` est `5` (indice 3) → échange avec l'indice 2 → `[1, 2, 5, 8, 9]`
- Étape `i=3` : le minimum de `[8, 9]` est `8`, déjà en place → `[1, 2, 5, 8, 9]`
- Le tableau est trié.

### 1.3 Invariant de boucle

**Invariant proposé (boucle externe, indice `i`) :** *à chaque début d'itération, les éléments `t[0]` à `t[i-1]` sont triés et contiennent les `i` plus petites valeurs du tableau d'origine.*

- **Initialisation :** avant la première itération (`i=0`), il n'y a aucun élément à considérer (`t[0..-1]` est vide) : l'invariant est trivialement vrai.
- **Conservation :** si l'invariant est vrai avant l'itération `i`, la boucle interne recherche le minimum parmi `t[i..n-1]` (donc parmi tout ce qui n'est pas encore trié), puis l'échange avec `t[i]`. Après cet échange, `t[0..i]` contient bien les `i+1` plus petites valeurs, triées.
- **Conclusion :** à la fin (`i = n-1`), `t[0..n-2]` contient les `n-1` plus petites valeurs triées, et `t[n-1]` est nécessairement la plus grande valeur restante : le tableau entier est trié.

---

## 2. Le tri par insertion

### 2.1 Principe

Le **tri par insertion** procède différemment : on considère que le début du tableau (`t[0..i-1]`) est déjà trié, et on **insère** l'élément suivant (`t[i]`) à sa bonne place parmi les éléments déjà triés, en décalant si nécessaire les éléments plus grands.

```python
def tri_insertion(tableau):
    t = tableau[:]
    n = len(t)
    for i in range(1, n):
        valeur = t[i]
        j = i - 1
        while j >= 0 and t[j] > valeur:
            t[j + 1] = t[j]     # on décale l'élément vers la droite
            j -= 1
        t[j + 1] = valeur       # on insère valeur à la bonne place
    return t
```

### 2.2 Déroulement sur un exemple

Pour `[5, 2, 8, 1, 9]` :
- `i=1` : `valeur=2`. `2 < 5`, donc on décale `5` : `[5, 5, 8, 1, 9]`, puis on insère `2` en position 0 : `[2, 5, 8, 1, 9]`.
- `i=2` : `valeur=8`. `8 > 5` (élément précédent), pas de décalage : `[2, 5, 8, 1, 9]`.
- `i=3` : `valeur=1`. `1 < 8`, décale `8` ; `1 < 5`, décale `5` ; `1 < 2`, décale `2` : `[2, 2, 5, 8, 9]` puis insertion de `1` en position 0 : `[1, 2, 5, 8, 9]`.
- `i=4` : `valeur=9`. `9 > 8`, pas de décalage : `[1, 2, 5, 8, 9]`.
- Le tableau est trié.

### 2.3 Invariant de boucle

**Invariant proposé (boucle externe, indice `i`) :** *à chaque début d'itération, `t[0..i-1]` est trié (mais ne contient pas nécessairement les `i` plus petites valeurs — contrairement au tri par sélection, ce sont simplement les `i` premiers éléments du tableau d'origine, remis dans l'ordre entre eux).*

Cette différence est essentielle entre les deux algorithmes : le tri par sélection construit progressivement la portion triée en y plaçant, à chaque étape, la bonne valeur définitive (le minimum global restant) ; le tri par insertion construit la portion triée en y intégrant les éléments **dans l'ordre où ils apparaissaient** initialement, sans savoir à l'avance s'ils seront ou non les plus petits.

---

## 3. Coût des deux algorithmes

### 3.1 Nombre d'opérations dans le pire des cas

Pour le **tri par sélection**, la boucle interne parcourt, à l'étape `i`, environ `n - i` éléments pour trouver le minimum, et ce **quel que soit** le tableau de départ (même déjà trié, on effectue toujours cette recherche). Le nombre total de comparaisons est donc :

```
(n-1) + (n-2) + ... + 1 + 0 = n(n-1)/2
```

Pour le **tri par insertion**, dans le **pire des cas** (tableau trié dans l'ordre **décroissant**), chaque nouvel élément doit être décalé au-delà de **tous** les éléments déjà triés, ce qui donne également, au total, environ `n(n-1)/2` comparaisons/décalages. En revanche, dans le **meilleur des cas** (tableau déjà trié), le tri par insertion n'effectue qu'une seule comparaison par élément (`n-1` comparaisons au total) : il s'adapte à un tableau déjà (presque) trié, contrairement au tri par sélection qui effectue toujours le même nombre d'opérations.

### 3.2 Un coût quadratique

Dans les deux cas, le nombre d'opérations dans le pire des cas est de l'ordre de `n²` (on dit que le coût est **quadratique**) : si l'on double la taille du tableau, le nombre d'opérations est environ **multiplié par quatre**. C'est nettement moins efficace, pour de grands tableaux, que les algorithmes de tri plus élaborés étudiés en terminale (comme le tri fusion, de coût `n log(n)`), mais le tri par insertion et le tri par sélection restent simples à comprendre, à implémenter, et suffisamment efficaces pour de petits tableaux.

| Algorithme | Meilleur cas | Pire cas | Remarque |
|---|---|---|---|
| Tri par sélection | `n(n-1)/2` | `n(n-1)/2` | Toujours le même nombre de comparaisons |
| Tri par insertion | `n-1` (tableau déjà trié) | `n(n-1)/2` | S'adapte à un tableau presque trié |

---

## Synthèse

| Notion | Point clé à retenir |
|---|---|
| Tri par sélection | Recherche le minimum restant, l'échange en tête de la zone non triée |
| Tri par insertion | Insère chaque élément à sa place dans la portion déjà triée |
| Invariant (sélection) | `t[0..i-1]` contient les `i` plus petites valeurs, triées |
| Invariant (insertion) | `t[0..i-1]` est trié (mais pas nécessairement les plus petites valeurs) |
| Coût dans le pire des cas | Quadratique, de l'ordre de `n²`, pour les deux algorithmes |
| Différence pratique | L'insertion s'adapte à un tableau presque trié ; la sélection non |

*Prochaine étape suggérée : Chapitre 11 — Algorithme des k plus proches voisins.*
