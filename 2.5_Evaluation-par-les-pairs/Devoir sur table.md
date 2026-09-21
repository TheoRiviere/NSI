# Devoir sur table — Tableaux, recherche séquentielle et dichotomique

**Niveau :** Première NSI · **Durée :** 45 minutes · **Barème sur 20 points**

## Sujet

### Exercice 1 — Parcours de tableau (6 points)
On donne un tableau `temperatures` contenant des relevés de température sur une semaine.
1. Écrire une fonction `moyenne(tableau)` qui renvoie la moyenne des valeurs du tableau. *(3 points)*
2. Écrire une fonction `indice_max(tableau)` qui renvoie l'indice de la plus grande valeur du tableau. *(3 points)*

### Exercice 2 — Invariant de boucle (6 points)
On donne la fonction suivante, censée calculer le produit des éléments d'un tableau :
```python
def produit(tableau):
    p = 1
    for x in tableau:
        p = p * x
    return p
```
1. Proposer un invariant de boucle pour cette fonction. *(2 points)*
2. Vérifier que cet invariant est vrai avant la première itération (initialisation). *(2 points)*
3. Vérifier qu'il reste vrai après chaque itération (conservation). *(2 points)*

### Exercice 3 — Recherche dichotomique (8 points)
On donne le tableau trié `t = [1, 3, 5, 7, 9, 11, 13, 15]` (indices de 0 à 7).
1. Dérouler à la main l'algorithme de recherche dichotomique du cours pour rechercher la valeur `7`. Donner, à chaque itération, les valeurs de `gauche`, `droite`, `milieu`, et la comparaison effectuée. *(3 points)*
2. Faire de même pour la valeur `4` (absente du tableau). Que renvoie l'algorithme ? *(3 points)*
3. Combien de comparaisons ont été nécessaires dans chacun des deux cas ? Ce résultat est-il cohérent avec la complexité théorique en O(log n) de la recherche dichotomique ? *(2 points)*

## Corrigé et barème détaillé

### Exercice 1
```python
def moyenne(tableau):
    return sum(tableau) / len(tableau)

def indice_max(tableau):
    i_max = 0
    for i in range(1, len(tableau)):
        if tableau[i] > tableau[i_max]:
            i_max = i
    return i_max
```
Barème : 1 point par fonction si la logique est correcte mais la syntaxe imparfaite ; 3 points si la fonction est correcte et fonctionnelle.

### Exercice 2
- **Invariant :** à chaque étape de la boucle, `p` contient le produit de tous les éléments du tableau déjà parcourus.
- **Initialisation :** avant la boucle, `p = 1`, ce qui correspond bien au produit d'un ensemble vide d'éléments. *(2 points si formulé correctement)*
- **Conservation :** si `p` contient le produit des éléments déjà parcourus avant de traiter `x`, alors après `p = p * x`, `p` contient le produit de ces éléments et de `x`, donc de tous les éléments parcourus jusqu'ici. *(2 points si le raisonnement est explicite)*
- Barème global : 1 point retiré par étape si la formulation reste vague ou si l'élève confond invariant et résultat final.

### Exercice 3
1. `gauche=0, droite=7, milieu=3` → `t[3]=7` → trouvé directement en 1 comparaison. *(3 points ; 1 point si une seule erreur d'indice, 0 si la démarche est absente)*
2. Recherche de `4` : `gauche=0, droite=7, milieu=3` → `t[3]=7 > 4` → `droite=2` ; `gauche=0, droite=2, milieu=1` → `t[1]=3 < 4` → `gauche=2` ; `gauche=2, droite=2, milieu=2` → `t[2]=5 > 4` → `droite=1` ; `gauche=2 > droite=1`, la boucle s'arrête : renvoie `-1`. *(3 points, 1 point par erreur isolée)*
3. 1 comparaison pour la valeur trouvée, 3 comparaisons pour la valeur absente. Le tableau contient 8 éléments, et log₂(8) = 3 : ces résultats sont cohérents avec la borne théorique en O(log n), qui majore le nombre de comparaisons dans le pire des cas. *(2 points si la cohérence avec log₂(n) est explicitée)*
