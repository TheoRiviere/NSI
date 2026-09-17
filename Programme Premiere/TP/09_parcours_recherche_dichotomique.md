# Chapitre 9 — Parcours séquentiel et recherche dichotomique
## TP sur machine — Mesurer expérimentalement le coût des deux recherches

*Première NSI — Python 3 — Durée indicative : 1h30*

---

## Objectifs

- Instrumenter des fonctions de recherche pour compter leur nombre de comparaisons.
- Comparer expérimentalement la croissance du coût de la recherche linéaire et de la recherche dichotomique.
- Observer concrètement l'écart de performance sur de grands tableaux.

---

## Partie A — Instrumenter les deux algorithmes de recherche

**A.1.** Recopier `recherche_lineaire` et `recherche_dichotomique` du cours, en les modifiant pour qu'elles renvoient chacune un couple `(indice_trouve, nombre_de_comparaisons)` au lieu de simplement `indice_trouve` (fonctions `recherche_lineaire_compte` et `recherche_dichotomique_compte`).

**A.2.** Tester les deux fonctions sur un petit tableau trié de votre choix, pour une valeur présente et une valeur absente, et vérifier que le nombre de comparaisons semble cohérent avec ce que vous avez calculé à la main dans la fiche d'exercices.

---

## Partie B — Mesurer la croissance du coût en fonction de la taille

**B.1.** Écrire une boucle qui, pour des tailles de tableau croissantes (`10`, `100`, `1 000`, `10 000`, `100 000`), construit un tableau trié de nombres pairs (`list(range(0, taille * 2, 2))`), recherche une valeur **absente** (par exemple `1`, qui est impair et n'apparaît donc jamais), et enregistre le nombre de comparaisons effectuées par chacune des deux fonctions.

**B.2.** Afficher les résultats sous forme de tableau (taille, comparaisons en recherche linéaire, comparaisons en recherche dichotomique).

**B.3.** Que constatez-vous sur l'évolution du nombre de comparaisons de la recherche linéaire lorsque la taille est multipliée par 10 ? Et pour la recherche dichotomique ?

**B.4. (bonus, si le module `matplotlib` est installé)** Tracer un graphique représentant le nombre de comparaisons en fonction de la taille du tableau, pour les deux algorithmes (on pourra utiliser une échelle logarithmique sur l'axe des tailles avec `plt.xscale("log")`, pour mieux visualiser les deux courbes sur une même figure).

---

## Partie C — Le cas de la recherche du dernier élément

**C.1.** Pour un tableau trié de 1000 éléments, rechercher le **dernier** élément du tableau (qui est donc présent, mais tout à la fin) avec `recherche_lineaire_compte` et avec `recherche_dichotomique_compte`. Comparer les deux nombres de comparaisons obtenus.

**C.2.** Ce résultat illustre-t-il un pire cas, un meilleur cas, ou un cas intermédiaire pour chacun des deux algorithmes ? Justifier.

---

## Corrigé indicatif

```python
# --- Partie A ---
def recherche_lineaire_compte(tableau, valeur):
    nb_comparaisons = 0
    for i in range(len(tableau)):
        nb_comparaisons += 1
        if tableau[i] == valeur:
            return i, nb_comparaisons
    return -1, nb_comparaisons

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


# --- Partie B ---
print(f"{'Taille':>10} | {'Linéaire':>10} | {'Dichotomique':>13}")
resultats = []
for taille in [10, 100, 1000, 10000, 100000]:
    tableau = list(range(0, taille * 2, 2))   # nombres pairs triés
    valeur_absente = 1                         # impaire, jamais présente

    _, nb_lineaire = recherche_lineaire_compte(tableau, valeur_absente)
    _, nb_dichotomique = recherche_dichotomique_compte(tableau, valeur_absente)
    resultats.append((taille, nb_lineaire, nb_dichotomique))
    print(f"{taille:>10} | {nb_lineaire:>10} | {nb_dichotomique:>13}")

# Résultats obtenus (pire cas, valeur absente) :
#     Taille |   Linéaire | Dichotomique
#         10 |         10 |            3
#        100 |        100 |            7
#       1000 |       1000 |           10
#      10000 |      10000 |           13
#     100000 |     100000 |           17


# --- Partie B.4 (bonus) ---
import matplotlib.pyplot as plt

tailles = [r[0] for r in resultats]
lineaires = [r[1] for r in resultats]
dichotomiques = [r[2] for r in resultats]

plt.plot(tailles, lineaires, marker="o", label="Recherche linéaire")
plt.plot(tailles, dichotomiques, marker="o", label="Recherche dichotomique")
plt.xscale("log")
plt.xlabel("Taille du tableau")
plt.ylabel("Nombre de comparaisons")
plt.legend()
plt.title("Comparaison du coût des deux algorithmes de recherche")
plt.savefig("comparaison_recherches.png")
plt.show()


# --- Partie C ---
tableau_1000 = list(range(0, 2000, 2))
dernier_element = tableau_1000[-1]   # 1998

_, nb_lineaire_dernier = recherche_lineaire_compte(tableau_1000, dernier_element)
_, nb_dichotomique_dernier = recherche_dichotomique_compte(tableau_1000, dernier_element)

print("\nRecherche du dernier élément (tableau de taille 1000) :")
print("Linéaire :", nb_lineaire_dernier)        # 1000
print("Dichotomique :", nb_dichotomique_dernier) # 10
```

**Réponse B.3 :** pour la recherche **linéaire**, le nombre de comparaisons (pire cas) est **multiplié par 10** à chaque fois que la taille est multipliée par 10 (croissance linéaire, proportionnelle à `n`). Pour la recherche **dichotomique**, le nombre de comparaisons n'augmente que de **3 ou 4** environ à chaque multiplication par 10 de la taille (croissance en `log₂(n)`) : l'écart entre les deux algorithmes devient de plus en plus spectaculaire à mesure que la taille grandit.

**Réponse C.2 :** rechercher le dernier élément constitue le **pire cas** pour la recherche linéaire (il faut examiner tous les éléments avant de le trouver, exactement comme pour une valeur absente), alors que pour la recherche dichotomique, ce n'est ni le meilleur cas (qui serait de trouver directement l'élément central) ni un cas particulièrement défavorable : le nombre de comparaisons reste de l'ordre de `log₂(n)`, quelle que soit la position de l'élément recherché, à condition que le tableau soit bien trié.
