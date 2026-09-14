# Chapitre 7 — Diviser pour régner
## Évaluation

*Terminale NSI — Durée : 50 min — Barème sur 20 points*

---

### Partie 1 — Questions de cours (6 points)

**Question 1 (3 pts).** Décrire les trois étapes de la méthode « diviser pour régner », en illustrant chacune par ce qu'elle représente dans le tri fusion.

**Question 2 (3 pts).** Pourquoi le tri fusion est-il, pour de grands tableaux, plus rapide qu'un tri en `n²` comme le tri par sélection ? Justifier en comparant l'ordre de grandeur des deux coûts.

---

### Partie 2 — Tri fusion (8 points)

On donne :
```python
def fusionner(gauche, droite):
    resultat = []
    i, j = 0, 0
    while i < len(gauche) and j < len(droite):
        if gauche[i] <= droite[j]:
            resultat.append(gauche[i])
            i += 1
        else:
            resultat.append(droite[j])
            j += 1
    resultat.extend(gauche[i:])
    resultat.extend(droite[j:])
    return resultat
```

**Question 3 (2 pts).** Donner le résultat de `fusionner([1, 4, 6], [2, 3, 9, 10])`.

**Question 4 (6 pts).** Écrire, sans regarder le cours, la fonction complète `tri_fusion(tableau)` qui trie un tableau en utilisant `fusionner`.

---

### Partie 3 — Appliquer la méthode (6 points)

**Question 5 (6 pts).** On souhaite écrire une fonction `compter(tableau)` qui compte le nombre d'éléments d'un tableau, **selon le principe « diviser pour régner »** (sans utiliser `len` sur le tableau complet, et sans boucle) : diviser le tableau en deux moitiés, compter récursivement les éléments de chaque moitié, puis additionner les deux résultats. Écrire cette fonction (cas de base : tableau vide ou d'un seul élément).

---

## Corrigé et barème détaillé

### Partie 1 (6 pts)

**Q1 (3 pts, 1 pt/étape)** — Diviser : couper le tableau en deux moitiés. Régner : trier récursivement chaque moitié. Combiner : fusionner les deux moitiés triées en un seul tableau trié (fonction `fusionner`).

**Q2 (3 pts)** — Le tri fusion a un coût en `n log₂ n`, alors que le tri par sélection a un coût en `n²` (1 pt). Pour un grand `n`, `n log₂ n` croît beaucoup plus lentement que `n²` : par exemple pour `n = 1 000 000`, `n log₂ n` vaut environ 20 millions contre 10¹² pour `n²`, un facteur 50 000 (2 pts pour l'illustration chiffrée ou une comparaison qualitative correcte de la croissance).

### Partie 2 (8 pts)

**Q3 (2 pts)** — `[1, 2, 3, 4, 6, 9, 10]`.

**Q4 (6 pts)**
```python
def tri_fusion(tableau):
    if len(tableau) <= 1:
        return tableau
    milieu = len(tableau) // 2
    gauche = tri_fusion(tableau[:milieu])
    droite = tri_fusion(tableau[milieu:])
    return fusionner(gauche, droite)
```
*(2 pts cas de base correct ; 2 pts découpage correct en deux moitiés avec appels récursifs ; 2 pts appel final à `fusionner` et valeur de retour.)*

### Partie 3 (6 pts)

**Q5 (6 pts)**
```python
def compter(tableau):
    if len(tableau) <= 1:
        return len(tableau)
    milieu = len(tableau) // 2
    return compter(tableau[:milieu]) + compter(tableau[milieu:])
```
*(2 pts cas de base correct ; 2 pts division en deux moitiés ; 2 pts combinaison par addition et valeur de retour correcte.)*

---

**Barème global : 6 + 8 + 6 = 20 points.**
