# Chapitre 9 — Recherche textuelle
## TP sur machine — Naïf contre Boyer-Moore

*Terminale NSI — Python 3 — Durée indicative : 1h30*

---

## Objectifs

- Implémenter et tester la recherche naïve et l'algorithme de Boyer-Moore.
- Vérifier que les deux algorithmes donnent toujours le même résultat.
- Comparer expérimentalement leur nombre de comparaisons et leur temps d'exécution.

---

## Partie A — Implémentation et vérification croisée

**A.1.** Recopier `recherche_naive`, `table_dernieres_occurrences` et `boyer_moore` du cours.

**A.2.** Écrire une fonction `verifier(texte, motif)` qui renvoie `True` si `recherche_naive` et `boyer_moore` donnent exactement le même résultat sur ce couple `(texte, motif)`.

**A.3.** À l'aide du module `random`, générer aléatoirement 200 couples `(texte, motif)` sur l'alphabet `{"A", "B", "C"}` (textes de longueur aléatoire entre 0 et 30, motifs entre 1 et 6), et vérifier que `verifier` renvoie `True` dans tous les cas. Ce test ne prouve pas que l'algorithme est correct en toute généralité, mais il permet de détecter une éventuelle erreur d'implémentation.

---

## Partie B — Recherche dans un texte réel

**B.1.** Récupérer un texte assez long (par exemple un extrait de plusieurs paragraphes copié depuis un livre du domaine public, ou un texte fourni par le professeur), et le stocker dans une variable `texte`.

**B.2.** Rechercher plusieurs mots de longueurs différentes dans ce texte avec `boyer_moore`, et afficher, pour chacun, ses positions et son nombre d'occurrences.

**B.3.** Écrire une fonction `souligner(texte, motif)` qui renvoie une version du texte où chaque occurrence du motif est mise en évidence (par exemple entourée de `>>>` et `<<<`), en s'appuyant sur les positions renvoyées par `boyer_moore`.

---

## Partie C — Comparaison de performance

**C.1.** Reprendre les versions « comptées » `recherche_naive_comptee` et `boyer_moore_compte` de la fiche d'exercices.

**C.2.** Construire un texte de test long et répétitif, par exemple `"AB" * 5000`, et y chercher un motif absent comme `"BA" * 3 + "C"`. Comparer le nombre de comparaisons effectuées par les deux algorithmes.

**C.3.** Recommencer avec un texte aléatoire sur un alphabet de 20 caractères différents (pour éviter les répétitions). Le nombre de comparaisons de Boyer-Moore change-t-il beaucoup ? Formuler une conclusion sur les situations où Boyer-Moore est le plus avantageux.

---

## Corrigé indicatif

```python
import random

def recherche_naive(texte, motif):
    n, m = len(texte), len(motif)
    return [i for i in range(n - m + 1) if texte[i:i + m] == motif]

def table_dernieres_occurrences(motif):
    return {c: i for i, c in enumerate(motif)}

def boyer_moore(texte, motif):
    n, m = len(texte), len(motif)
    if m == 0:
        return list(range(n + 1))
    table = table_dernieres_occurrences(motif)
    positions = []
    i = 0
    while i <= n - m:
        j = m - 1
        while j >= 0 and motif[j] == texte[i + j]:
            j -= 1
        if j < 0:
            positions.append(i)
            i += 1
        else:
            decalage = j - table.get(texte[i + j], -1)
            i += max(1, decalage)
    return positions


def verifier(texte, motif):
    return recherche_naive(texte, motif) == boyer_moore(texte, motif)

alphabet = "ABC"
for _ in range(200):
    texte = "".join(random.choice(alphabet) for _ in range(random.randint(0, 30)))
    motif = "".join(random.choice(alphabet) for _ in range(random.randint(1, 6)))
    assert verifier(texte, motif), (texte, motif)
print("Tous les tests aléatoires sont cohérents.")


def souligner(texte, motif):
    positions = boyer_moore(texte, motif)
    resultat = ""
    dernier = 0
    for p in positions:
        resultat += texte[dernier:p] + ">>>" + texte[p:p + len(motif)] + "<<<"
        dernier = p + len(motif)
    resultat += texte[dernier:]
    return resultat
```

**C3.** Dans les deux cas, Boyer-Moore effectue nettement moins de comparaisons que la recherche naïve (l'écart mesuré est typiquement d'un facteur 5 à 10 dans cette expérience). L'intuition générale est la suivante : plus l'alphabet utilisé est riche, plus il est probable qu'un caractère quelconque du texte soit absent du motif (ou situé loin de sa fin), ce qui autorise de grands décalages via la règle du mauvais caractère ; sur un alphabet très réduit (comme les quatre lettres de l'ADN), les décalages obtenus sont en moyenne plus petits, ce qui réduit l'avantage de Boyer-Moore sans le faire disparaître. Cette expérience montre surtout qu'il faut mesurer plutôt que supposer : le gain réel dépend fortement du texte, du motif et de l'alphabet considérés.
