# Chapitre 7 — Diviser pour régner
## Fiche d'exercices

*Terminale NSI — Python 3*

---

### Exercice 1 — Vocabulaire

1. Rappeler les trois étapes de la méthode « diviser pour régner ».
2. Dans le tri fusion, à quelle étape correspond la fonction `fusionner` ?
3. La recherche dichotomique (chapitre 6) est-elle un algorithme « diviser pour régner » ? Justifier (en particulier : combien de sous-problèmes génère-t-elle à chaque étape ?).

### Exercice 2 — Fusionner à la main

Dérouler à la main l'appel `fusionner([2, 5, 8], [1, 3, 9])` en indiquant, à chaque étape, le contenu de `resultat`, `i` et `j`.

### Exercice 3 — Compter les comparaisons

1. Modifier `fusionner` pour qu'elle renvoie, en plus du tableau fusionné, le nombre de comparaisons effectuées (chaque test `gauche[i] <= droite[j]` compte pour une comparaison).
2. Quel est le nombre maximal de comparaisons lors de la fusion de deux tableaux de tailles `p` et `q` ?

### Exercice 4 — Maximum par diviser pour régner

Écrire une fonction `maximum(tableau)` qui calcule le maximum d'un tableau non vide selon le principe « diviser pour régner » : diviser le tableau en deux moitiés, calculer récursivement le maximum de chaque moitié, puis combiner en prenant le plus grand des deux.

### Exercice 5 — Tri fusion, variante avec compteur d'appels

Modifier `tri_fusion` pour qu'elle affiche, à chaque appel, la taille du tableau qu'elle est en train de trier (`print(f"tri_fusion appelé sur un tableau de taille {len(tableau)}")`). Exécuter sur un tableau de 8 éléments et compter le nombre total d'appels effectués.

### Exercice 6 — Rotation d'image : cas particuliers

1. Que se passe-t-il si on applique `rotation_90_degres` à une image `1×1` ? Expliquer pourquoi le résultat est correct sans qu'aucune boucle ne s'exécute.
2. Pourquoi la boucle externe de `rotation_90_degres` s'arrête-t-elle à `n // 2` et non à `n` ?

---

## Corrigés

### Exercice 1

1. Diviser (découper en sous-problèmes plus petits), régner (résoudre récursivement chaque sous-problème), combiner (assembler les solutions).
2. `fusionner` correspond à l'étape **combiner**.
3. Oui, dans un sens dégénéré : on divise le tableau en éliminant une moitié, on ne « règne » que sur **un seul** sous-problème (la moitié restante) au lieu de deux, et il n'y a pas d'étape de combinaison à proprement parler (le résultat du sous-problème est directement le résultat final).

### Exercice 2

| Étape | `resultat` | `i` | `j` |
|---|---|---|---|
| départ | `[]` | 0 | 0 |
| `2 <= 1` faux | `[1]` | 0 | 1 |
| `2 <= 3` vrai | `[1, 2]` | 1 | 1 |
| `5 <= 3` faux | `[1, 2, 3]` | 1 | 2 |
| `5 <= 9` vrai | `[1, 2, 3, 5]` | 2 | 2 |
| `8 <= 9` vrai | `[1, 2, 3, 5, 8]` | 3 | 2 |
| `i` atteint la fin de `gauche` | `[1, 2, 3, 5, 8, 9]` | 3 | 3 |

### Exercice 3

```python
def fusionner_comptee(gauche, droite):
    resultat = []
    i, j = 0, 0
    comparaisons = 0
    while i < len(gauche) and j < len(droite):
        comparaisons += 1
        if gauche[i] <= droite[j]:
            resultat.append(gauche[i])
            i += 1
        else:
            resultat.append(droite[j])
            j += 1
    resultat.extend(gauche[i:])
    resultat.extend(droite[j:])
    return resultat, comparaisons
```

2. Le nombre maximal de comparaisons est `p + q - 1` : à chaque comparaison, un élément est placé dans `resultat`, et l'on s'arrête dès que l'un des deux tableaux est épuisé — au pire, les `p + q - 1` premiers éléments nécessitent chacun une comparaison, le tout dernier étant ajouté sans comparaison (par les `extend` finaux).

### Exercice 4

```python
def maximum(tableau):
    if len(tableau) == 1:
        return tableau[0]
    milieu = len(tableau) // 2
    max_gauche = maximum(tableau[:milieu])
    max_droite = maximum(tableau[milieu:])
    return max(max_gauche, max_droite)
```

### Exercice 5

Pour un tableau de 8 éléments, le nombre total d'appels à `tri_fusion` (cas de base inclus) est **15** : 1 appel sur 8 éléments, 2 appels sur 4 éléments, 4 appels sur 2 éléments, 8 appels sur 1 élément (`1 + 2 + 4 + 8 = 15`), ce qui correspond à un arbre binaire complet de hauteur 3.

### Exercice 6

1. Pour une image `1×1`, `n // 2 = 0`, donc la boucle externe `for couche in range(0)` ne s'exécute jamais : l'image reste inchangée, ce qui est le résultat correct (une image d'un seul pixel est invariante par rotation).
2. Chaque itération de la boucle externe traite une couche extérieure **et**, simultanément (via les échanges à quatre éléments), la couche symétrique correspondante côté intérieur n'a pas besoin d'être traitée séparément : traiter les couches au-delà de `n // 2` reviendrait à traiter deux fois les mêmes éléments (ou, pour une taille impaire, à essayer de faire pivoter l'unique pixel central, qui reste toujours à sa place).
