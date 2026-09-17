# Chapitre 9 — Parcours séquentiel et recherche dichotomique
## Évaluation

*Première NSI — Durée : 55 min — Barème sur 20 points*

---

### Partie 1 — Questions de cours (7 points)

**Question 1 (2 pts).** Quelle condition un tableau doit-il vérifier pour que l'on puisse y appliquer une recherche dichotomique ?

**Question 2 (2 pts).** Qu'est-ce qu'un invariant de boucle ? À quoi sert-il ?

**Question 3 (3 pts).** Qu'est-ce qu'un variant de boucle ? Pourquoi permet-il de prouver qu'une boucle `while` se termine ?

---

### Partie 2 — Tracer une recherche dichotomique (7 points)

On donne le tableau trié `t = [3, 8, 12, 17, 25, 31, 40, 55]` (indices de 0 à 7).

**Question 4 (4 pts).** Dérouler à la main la recherche dichotomique de la valeur `31` : donner, à chaque itération, les valeurs de `gauche`, `droite`, `milieu`, et la comparaison effectuée.

**Question 5 (3 pts).** Dérouler de même la recherche de la valeur `20` (absente du tableau). Combien de comparaisons sont effectuées avant que l'algorithme ne conclue à l'absence de la valeur ?

---

### Partie 3 — Écrire du code et preuve (6 points)

**Question 6 (3 pts).** Écrire une fonction `tous_positifs(tableau)` qui renvoie `True` si tous les éléments du tableau sont positifs ou nuls, et `False` sinon (on utilisera un parcours séquentiel).

**Question 7 (3 pts).** Proposer un invariant de boucle pour la fonction que vous venez d'écrire (que peut-on dire, à un instant donné du parcours, sur les éléments déjà examinés, sachant qu'aucun test n'a encore renvoyé `False` ?).

---

## Corrigé et barème détaillé

### Partie 1 (7 pts)

**Q1 (2 pts)** — Le tableau doit être **trié** (par ordre croissant, ou décroissant selon la convention choisie) : le principe de la dichotomie repose entièrement sur le fait de pouvoir éliminer une moitié du tableau en le comparant à l'élément central, ce qui n'est valide que si l'ordre est garanti.

**Q2 (2 pts)** — Un invariant de boucle est une propriété qui est vraie avant la boucle et qui reste vraie après chaque itération (1 pt). Il sert à **prouver la correction** d'un algorithme itératif : en le combinant à la condition d'arrêt de la boucle, on peut démontrer que le résultat final est bien celui attendu (1 pt).

**Q3 (3 pts)** — Un variant de boucle est une quantité entière positive ou nulle qui diminue strictement à chaque itération (1,5 pt). Comme une suite d'entiers strictement décroissante ne peut pas décroître indéfiniment, l'existence d'un tel variant garantit que la boucle se termine en un nombre fini d'étapes (1,5 pt).

### Partie 2 (7 pts)

**Q4 (4 pts)** —
- `gauche=0, droite=7, milieu=3` → `t[3]=17 < 31` → `gauche=4`
- `gauche=4, droite=7, milieu=5` → `t[5]=31` → trouvé, indice `5`.

*(2 pts par itération correctement détaillée.)*

**Q5 (3 pts)** —
- `gauche=0, droite=7, milieu=3` → `t[3]=17 < 20` → `gauche=4`
- `gauche=4, droite=7, milieu=5` → `t[5]=31 > 20` → `droite=4`
- `gauche=4, droite=4, milieu=4` → `t[4]=25 > 20` → `droite=3`
- `gauche=4, droite=3` → `gauche > droite`, arrêt : valeur absente, après **3 comparaisons**.

*(2 pts pour le déroulement correct, 1 pt pour le bon nombre de comparaisons.)*

### Partie 3 (6 pts)

**Q6 (3 pts)**
```python
def tous_positifs(tableau):
    for x in tableau:
        if x < 0:
            return False
    return True
```

**Q7 (3 pts)** — **Invariant proposé :** à chaque étape du parcours, si la fonction n'a pas encore renvoyé `False`, alors tous les éléments examinés jusqu'ici sont positifs ou nuls. *(Toute formulation équivalente correcte est acceptée : 1,5 pt pour l'idée que l'invariant porte sur les éléments déjà examinés, 1,5 pt pour la formulation correcte de la propriété — « tous positifs ou nuls tant qu'aucun False n'a été renvoyé ».)*

---

**Barème global : 7 + 7 + 6 = 20 points.**
