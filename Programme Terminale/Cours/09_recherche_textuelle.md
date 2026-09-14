# Terminale NSI — Chapitre 9
# Recherche textuelle : l'algorithme de Boyer-Moore

*Support de cours — Python 3*

---

## Objectifs du chapitre

- Écrire l'algorithme de recherche naïve d'un motif dans un texte.
- Comprendre le principe de l'algorithme de Boyer-Moore (règle du mauvais caractère).
- Comprendre l'intérêt du prétraitement du motif.

**Prérequis :** manipulation de chaînes de caractères, dictionnaires (chapitre 3).

---

## 9.1 Le problème

On cherche à savoir si un **motif** (une courte chaîne de caractères) apparaît dans un **texte** (une chaîne plus longue), et le cas échéant, à quel(s) indice(s). C'est un problème central en informatique : recherche dans un traitement de texte, recherche d'un gène dans une séquence ADN, moteurs de recherche, antivirus, etc.

---

## 9.2 Algorithme naïf

L'approche la plus simple consiste à essayer, pour chaque position possible du texte, si le motif correspond à partir de cette position.

```python
def recherche_naive(texte, motif):
    n, m = len(texte), len(motif)
    positions = []
    for i in range(n - m + 1):
        if texte[i:i + m] == motif:
            positions.append(i)
    return positions
```

**Coût.** Dans le pire des cas, pour chaque position `i` (il y en a environ `n`), on peut être amené à comparer jusqu'à `m` caractères : le coût est donc de l'ordre de `n × m` comparaisons.

---

## 9.3 L'idée de Boyer-Moore : comparer de droite à gauche

L'algorithme de Boyer-Moore repose sur deux idées principales :

1. Pour chaque position d'essai, comparer le motif au texte **en commençant par la fin du motif** (de droite à gauche).
2. Lorsqu'un caractère du texte ne correspond pas au motif, utiliser cette information pour **décaler le motif de plusieurs positions d'un coup**, au lieu d'une seule — c'est la **règle du mauvais caractère**.

### La règle du mauvais caractère

Si la comparaison échoue sur un caractère `c` du texte (qui ne correspond pas au caractère attendu du motif), on regarde la **dernière occurrence de `c` dans le motif** :

- si `c` n'apparaît pas du tout dans le motif, on peut décaler le motif **juste après** la position de `c` dans le texte : aucune correspondance n'est possible tant que le motif recouvre `c` ;
- si `c` apparaît dans le motif, on décale le motif pour aligner cette dernière occurrence de `c` avec la position où l'échec a eu lieu dans le texte.

### Prétraitement du motif

Pour appliquer rapidement cette règle, on **prétraite** le motif une seule fois, avant de parcourir le texte : on construit une table qui associe à chaque caractère la position de sa **dernière occurrence** dans le motif.

```python
def table_dernieres_occurrences(motif):
    table = {}
    for i, caractere in enumerate(motif):
        table[caractere] = i   # on écrase à chaque occurrence : on garde la dernière
    return table
```

**Exemple :** pour le motif `"ANANAS"`, la table est `{"A": 4, "N": 3, "S": 5}` (le `A` apparaît en dernier à l'indice 4, le `N` à l'indice 3).

---

## 9.4 L'algorithme complet

```python
def boyer_moore(texte, motif):
    n, m = len(texte), len(motif)
    if m == 0:
        return list(range(n + 1))
    table = table_dernieres_occurrences(motif)
    positions = []
    i = 0   # position d'alignement du motif dans le texte
    while i <= n - m:
        j = m - 1                     # on compare depuis la fin du motif
        while j >= 0 and motif[j] == texte[i + j]:
            j -= 1
        if j < 0:
            positions.append(i)       # motif trouvé entièrement
            i += 1                     # on avance d'une position pour chercher d'autres occurrences
        else:
            caractere = texte[i + j]
            decalage_table = table.get(caractere, -1)
            decalage = j - decalage_table
            i += max(1, decalage)     # on décale d'au moins 1, pour garantir la progression
    return positions
```

**Exemple :** `boyer_moore("VOICI UNE PHRASE AVEC UN MOTIF ANANAS DEDANS", "ANANAS")` renvoie la position où `"ANANAS"` commence dans le texte.

### Déroulement sur un petit exemple

Recherche de `"ANA"` dans `"BANANE"` :

```
Texte  : B A N A N E
Motif 1: A N A                (aligné à l'indice 0)
```
On compare de droite à gauche : `texte[2]='N'` contre `motif[2]='A'` : échec. `'N'` apparaît dans le motif à l'indice 1 ; on décale le motif pour aligner cette occurrence : décalage de `2 - 1 = 1`.

```
Texte  : B A N A N E
Motif 2:   A N A              (aligné à l'indice 1)
```
Comparaison de droite à gauche : `motif[2]='A'` = `texte[3]='A'` ✓, `motif[1]='N'` = `texte[2]='N'` ✓, `motif[0]='A'` = `texte[1]='A'` ✓ : le motif est trouvé à l'indice 1.

---

## 9.5 Intérêt du prétraitement

Construire la table des dernières occurrences a un coût proportionnel à la taille du motif (`O(m)`), effectué **une seule fois**, avant de parcourir le texte. Ce prétraitement permet ensuite, lors du parcours du texte, de **sauter** potentiellement plusieurs caractères à chaque échec de comparaison, au lieu d'avancer d'une seule position comme le fait l'algorithme naïf.

> **En pratique.** Sur un texte ne contenant presque aucune occurrence des caractères du motif, Boyer-Moore peut examiner beaucoup moins de caractères du texte que l'algorithme naïf — c'est particulièrement efficace pour de longs motifs sur un grand alphabet (texte en langue naturelle, par exemple). L'étude précise du coût dans le cas général est délicate et n'est pas exigible ; on retient surtout l'idée du décalage rendu possible par le prétraitement.

---

## 9.6 Synthèse

| Notion | Définition |
|---|---|
| Recherche naïve | Teste toutes les positions, coût de l'ordre de `n × m` |
| Boyer-Moore | Compare de droite à gauche, décale le motif de plusieurs positions grâce à un prétraitement |
| Règle du mauvais caractère | En cas d'échec sur un caractère, décale le motif pour aligner sa dernière occurrence de ce caractère |
| Prétraitement | Calcul, une seule fois, d'une table exploitée ensuite à chaque étape de la recherche |

*Ce chapitre clôt le bloc « algorithmique » du programme. Les chapitres suivants abordent respectivement la qualité de la programmation, les bases de données, puis les architectures matérielles et les réseaux.*
