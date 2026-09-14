# Chapitre 7 — Diviser pour régner
## TP sur machine — Tri fusion et traitement d'image

*Terminale NSI — Python 3 — Durée indicative : 1h30 à 2h*

---

## Objectifs

- Implémenter et tester un tri fusion complet.
- Comparer expérimentalement son coût à celui d'un tri quadratique.
- Appliquer la méthode « diviser pour régner » à un problème de traitement d'image.

---

## Partie A — Tri fusion

**A.1.** Recopier `fusionner` et `tri_fusion` du cours. Les tester sur plusieurs tableaux, y compris un tableau vide, un tableau d'un seul élément, et un tableau déjà trié.

**A.2.** Écrire un tri par sélection (vu en première NSI) :
```python
def tri_selection(tableau):
    t = tableau.copy()
    for i in range(len(t)):
        indice_min = i
        for j in range(i + 1, len(t)):
            if t[j] < t[indice_min]:
                indice_min = j
        t[i], t[indice_min] = t[indice_min], t[i]
    return t
```

**A.3.** À l'aide du module `time` et de `random`, comparer les temps d'exécution de `tri_fusion` et `tri_selection` sur des tableaux aléatoires de tailles croissantes (500, 2000, 5000, 10000 éléments). Présenter les résultats dans un tableau.

**A.4.** À partir de quelle taille la différence devient-elle nettement perceptible ? Relier votre observation à l'analyse de coût faite en cours (`n log₂ n` contre `n²`).

---

## Partie B — Rotation d'image

**B.1.** Recopier `rotation_90_degres` du cours.

**B.2.** Tester la fonction sur une image `4×4` de votre choix, puis vérifier qu'appliquer la rotation **quatre fois de suite** redonne l'image d'origine.

**B.3.** Écrire une fonction `rotation_180_degres(image)` qui fait pivoter une image d'un demi-tour, en appelant deux fois `rotation_90_degres`.

**B.4. (bonus)** Écrire une fonction `est_symetrique_verticalement(image)` qui vérifie si une image carrée est symétrique par rapport à son axe vertical, sans la modifier.

---

## Corrigé indicatif

```python
import random
import time

def fusionner(gauche, droite):
    resultat = []
    i, j = 0, 0
    while i < len(gauche) and j < len(droite):
        if gauche[i] <= droite[j]:
            resultat.append(gauche[i]); i += 1
        else:
            resultat.append(droite[j]); j += 1
    resultat.extend(gauche[i:])
    resultat.extend(droite[j:])
    return resultat

def tri_fusion(tableau):
    if len(tableau) <= 1:
        return tableau
    milieu = len(tableau) // 2
    return fusionner(tri_fusion(tableau[:milieu]), tri_fusion(tableau[milieu:]))

def tri_selection(tableau):
    t = tableau.copy()
    for i in range(len(t)):
        indice_min = i
        for j in range(i + 1, len(t)):
            if t[j] < t[indice_min]:
                indice_min = j
        t[i], t[indice_min] = t[indice_min], t[i]
    return t

for taille in [500, 2000, 5000, 10000]:
    tableau = [random.randint(0, 100000) for _ in range(taille)]
    debut = time.perf_counter()
    tri_fusion(tableau)
    duree_fusion = time.perf_counter() - debut

    debut = time.perf_counter()
    tri_selection(tableau)
    duree_selection = time.perf_counter() - debut

    print(f"n={taille:6d}  fusion={duree_fusion:.4f}s  selection={duree_selection:.4f}s")


def rotation_90_degres(image):
    n = len(image)
    for couche in range(n // 2):
        premier = couche
        dernier = n - 1 - couche
        for i in range(premier, dernier):
            decalage = i - premier
            haut = image[premier][i]
            image[premier][i] = image[dernier - decalage][premier]
            image[dernier - decalage][premier] = image[dernier][dernier - decalage]
            image[dernier][dernier - decalage] = image[i][dernier]
            image[i][dernier] = haut
    return image

def rotation_180_degres(image):
    rotation_90_degres(image)
    rotation_90_degres(image)
    return image

def est_symetrique_verticalement(image):
    n = len(image)
    for ligne in image:
        for colonne in range(n // 2):
            if ligne[colonne] != ligne[n - 1 - colonne]:
                return False
    return True
```

**A.4.** À partir de quelques milliers d'éléments, l'écart devient très net : le tri par sélection, en `n²`, voit son temps d'exécution être multiplié par 4 chaque fois que `n` double, alors que le tri fusion, en `n log₂ n`, voit son temps d'exécution à peine plus que doubler.
