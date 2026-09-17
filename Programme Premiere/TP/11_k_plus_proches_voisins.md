# Chapitre 11 — Algorithme des k plus proches voisins
## TP sur machine — Classifier des données synthétiques et choisir k

*Première NSI — Python 3 — Durée indicative : 1h30 à 2h*

---

## Objectifs

- Générer un jeu de données synthétique à deux catégories.
- Séparer les données en un jeu d'entraînement et un jeu de test.
- Étudier expérimentalement l'effet du choix de `k` sur la précision du classifieur.

---

## Partie A — Générer un jeu de données synthétique

On souhaite simuler deux « espèces » de fleurs, chacune caractérisée par deux mesures (par exemple longueur et largeur d'un pétale), les points de chaque espèce étant dispersés aléatoirement autour d'un centre.

**A.1.** Recopier `distance_euclidienne`, `k_plus_proches_voisins`, `classifier` du cours.

**A.2.** Écrire une fonction `generer_donnees(centre, rayon, etiquette, n)` qui génère `n` points aléatoires autour du point `centre` (un tuple `(x, y)`), chaque coordonnée étant tirée avec `random.uniform(-rayon, rayon)` ajouté à celle du centre, tous associés à l'`etiquette` donnée. La fonction renvoie une liste de couples `(point, etiquette)`.

**A.3.** Générer 40 points d'« espèceA » autour de `(5, 5)` avec un rayon de `3`, et 40 points d'« espèceB » autour de `(8, 8)`, également avec un rayon de `3` (ces deux zones se chevauchent partiellement, ce qui rendra la classification plus intéressante à étudier). Fixer une graine aléatoire (`random.seed(42)`) pour obtenir des résultats reproductibles.

---

## Partie B — Séparer entraînement et test

**B.1.** Fusionner les deux listes de points générées, puis les mélanger avec `random.shuffle`.

**B.2.** Répartir 70% des données dans un jeu d'entraînement, et les 30% restants dans un jeu de test (indication : calculer `n_train = int(0.7 * len(toutes_donnees))`, puis découper la liste mélangée en deux tranches).

**B.3.** Recopier `evaluer_precision` du cours.

---

## Partie C — Étudier l'effet de `k`

**C.1.** Calculer la précision du classifieur sur le jeu de test, pour chacune des valeurs de `k` suivantes : `1, 3, 5, 7, 11, 15`. Afficher les résultats dans un tableau.

**C.2.** Quelle valeur de `k` donne la meilleure précision sur ce jeu de données ? Le résultat est-il le même pour tout le monde (en tenant compte du fait que la génération des données est aléatoire, même avec une graine fixée, un choix différent de graine donnera des données différentes) ?

**C.3.** Pourquoi la précision n'atteint-elle jamais 100%, quel que soit `k`, sur ce jeu de données en particulier (contrairement à des données bien séparées, sans chevauchement) ?

**C.4. (bonus)** Refaire l'expérience en réduisant le rayon de dispersion à `1` au lieu de `3` (les deux groupes de points seront alors beaucoup plus séparés). La précision obtenue est-elle meilleure ? Est-ce cohérent avec votre réponse à la question C.3 ?

---

## Corrigé indicatif

```python
import math
import random
from collections import Counter

def distance_euclidienne(p1, p2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(p1, p2)))

def k_plus_proches_voisins(donnees, nouveau_point, k):
    distances = []
    for point, etiquette in donnees:
        d = distance_euclidienne(point, nouveau_point)
        distances.append((d, etiquette))
    distances.sort(key=lambda x: x[0])
    return distances[:k]

def classifier(donnees, nouveau_point, k):
    voisins = k_plus_proches_voisins(donnees, nouveau_point, k)
    etiquettes = [etiquette for distance, etiquette in voisins]
    compteur = Counter(etiquettes)
    return compteur.most_common(1)[0][0]

def evaluer_precision(donnees_entrainement, donnees_test, k):
    bonnes_predictions = 0
    for point, vraie_etiquette in donnees_test:
        prediction = classifier(donnees_entrainement, point, k)
        if prediction == vraie_etiquette:
            bonnes_predictions += 1
    return bonnes_predictions / len(donnees_test)


# --- Partie A ---
def generer_donnees(centre, rayon, etiquette, n):
    points = []
    for _ in range(n):
        x = centre[0] + random.uniform(-rayon, rayon)
        y = centre[1] + random.uniform(-rayon, rayon)
        points.append(((x, y), etiquette))
    return points

random.seed(42)
espece_a = generer_donnees((5, 5), 3, "especeA", 40)
espece_b = generer_donnees((8, 8), 3, "especeB", 40)


# --- Partie B ---
toutes_donnees = espece_a + espece_b
random.shuffle(toutes_donnees)

n_train = int(0.7 * len(toutes_donnees))
donnees_entrainement = toutes_donnees[:n_train]
donnees_test = toutes_donnees[n_train:]

print("Entraînement :", len(donnees_entrainement), "| Test :", len(donnees_test))


# --- Partie C ---
print(f"\n{'k':>4} | {'Précision':>10}")
for k in [1, 3, 5, 7, 11, 15]:
    precision = evaluer_precision(donnees_entrainement, donnees_test, k)
    print(f"{k:>4} | {precision:>10.2f}")

# Résultats obtenus (avec la graine 42) :
#    k | Précision
#    1 |      0.71
#    3 |      0.67
#    5 |      0.67
#    7 |      0.71
#   11 |      0.75
#   15 |      0.75
```

**Réponse C.3 :** les deux zones de génération (`(5,5)` et `(8,8)`, chacune avec un rayon de 3) se **chevauchent** partiellement : certains points d'« espèceA » se retrouvent, par hasard, plus proches du centre d'« espèceB » que de leur propre groupe, et inversement. Aucun classifieur — pas seulement k-NN — ne peut atteindre 100% de précision lorsque les catégories ne sont pas parfaitement séparables dans l'espace des caractéristiques utilisées : il existe une limite théorique de précision imposée par le chevauchement des données elles-mêmes, indépendamment de la qualité de l'algorithme.

**Réponse C.4 (bonus) :** en réduisant le rayon à `1`, les deux groupes de points deviennent beaucoup plus compacts et donc beaucoup mieux séparés (les zones `(5,5)±1` et `(8,8)±1` ne se chevauchent presque plus) : la précision obtenue devrait alors être nettement plus proche de 100%, quel que soit `k`, ce qui confirme que la limite observée en C.3 provenait bien du chevauchement des données, et non d'une faiblesse de l'algorithme k-NN lui-même.
