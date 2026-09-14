# Chapitre 9 — Recherche textuelle
## Fiche d'exercices

*Terminale NSI — Python 3*

---

### Exercice 1 — Recherche naïve

1. Dérouler à la main `recherche_naive("AABAACAADAABAABA", "AABA")` : donner la liste des positions trouvées.
2. Combien de comparaisons de caractères, au maximum, l'algorithme naïf effectue-t-il pour un texte de longueur `n` et un motif de longueur `m` ?

### Exercice 2 — Table des dernières occurrences

Construire, sans exécuter de code, la table des dernières occurrences pour chacun des motifs suivants :
1. `"BOYER"`
2. `"MOORE"`
3. `"ABRACADABRA"`

### Exercice 3 — Dérouler Boyer-Moore à la main

Dérouler à la main la recherche de `"MOTIF"` par l'algorithme de Boyer-Moore dans le texte `"CE TEXTE NE CONTIENT PAS DE MOTIF EVIDENT"`, en indiquant à chaque étape la position d'alignement testée et le décalage effectué.

### Exercice 4 — Décalage minimal

Dans la fonction `boyer_moore` du cours, la ligne `i += max(1, decalage)` garantit un décalage d'au moins 1. Donner un exemple concret de motif et de texte pour lequel `decalage` calculé serait négatif ou nul sans cette précaution, et expliquer pourquoi.

### Exercice 5 — Compter les comparaisons

1. Modifier `recherche_naive` pour qu'elle compte le nombre total de comparaisons de caractères effectuées (`texte[i+k] == motif[k]`).
2. Modifier `boyer_moore` de la même façon.
3. Comparer les deux compteurs sur `recherche("AAAAAAAAAAAAAAAAAAAA", "BBBBB")` (un motif absent du texte). Que constatez-vous, et pourquoi ce cas est-il particulièrement favorable à Boyer-Moore ?

### Exercice 6 — Occurrences chevauchantes

Écrire une fonction `compte_occurrences_naif(texte, motif)` qui compte le nombre d'occurrences, **éventuellement chevauchantes**, d'un motif dans un texte (par exemple, `"AA"` apparaît deux fois, en position 0 et 1, dans `"AAA"`).

---

## Corrigés

### Exercice 1

1. Positions trouvées : `0, 9, 12` (le motif `"AABA"` apparaît à l'indice 0, à l'indice 9, puis à l'indice 12 du texte `"AABAACAADAABAABA"`).
2. Au maximum, `(n - m + 1) × m` comparaisons (une comparaison caractère par caractère à chacune des `n - m + 1` positions possibles).

### Exercice 2

1. `"BOYER"` → `{"B": 0, "O": 1, "Y": 2, "E": 3, "R": 4}`
2. `"MOORE"` → `{"M": 0, "O": 2, "R": 3, "E": 4}` (le `O` apparaît deux fois, on garde la dernière occurrence, à l'indice 2)
3. `"ABRACADABRA"` → `{"A": 10, "B": 8, "R": 9, "C": 4, "D": 6}`

### Exercice 3

Table des dernières occurrences de `"MOTIF"` : `{"M": 0, "O": 1, "T": 2, "I": 3, "F": 4}`.

- Alignement à l'indice 0 (`"CE TE"`) : comparaison en position 4, `motif[4]='F'` contre `texte[4]='T'` : échec. `'T'` est dans le motif à l'indice 2, décalage = `4 - 2 = 2`. Nouvel alignement à l'indice 2.
- Ce processus se répète, le motif glissant par sauts de plusieurs caractères à chaque échec, jusqu'à atteindre l'indice où `"MOTIF"` apparaît réellement dans le texte (à la fin de la phrase). *(L'objectif pédagogique est de faire manipuler le décalage ; le détail exhaustif de chaque étape peut être vérifié avec le code du cours.)*

### Exercice 4

Prenons le motif `"AAAA"` et le texte `"AAAB"`, alignés à l'indice 0. La comparaison de droite à gauche échoue dès `j = 3` (`motif[3]='A'` contre `texte[3]='B'`). La table du motif donne `{"A": 3}`. Le caractère `'B'` n'est pas dans la table, donc `decalage_table = -1`, et `decalage = j - decalage_table = 3 - (-1) = 4`. Ici le décalage est bien positif. En revanche, avec un motif comme `"ABAB"` et un échec sur `j = 1` où le caractère du texte est `'B'` (présent dans le motif à l'indice 3, **après** la position `j`), on obtiendrait `decalage = 1 - 3 = -2` : un décalage **négatif**, qui ferait reculer le motif au lieu de le faire avancer. La précaution `max(1, decalage)` garantit alors que l'on avance malgré tout d'au moins une position, évitant une boucle infinie.

### Exercice 5

```python
def recherche_naive_comptee(texte, motif):
    n, m = len(texte), len(motif)
    positions = []
    comparaisons = 0
    for i in range(n - m + 1):
        k = 0
        while k < m:
            comparaisons += 1
            if texte[i + k] != motif[k]:
                break
            k += 1
        else:
            positions.append(i)
    return positions, comparaisons


def boyer_moore_compte(texte, motif):
    n, m = len(texte), len(motif)
    table = {c: i for i, c in enumerate(motif)}
    positions = []
    comparaisons = 0
    i = 0
    while i <= n - m:
        j = m - 1
        while j >= 0:
            comparaisons += 1
            if motif[j] != texte[i + j]:
                break
            j -= 1
        if j < 0:
            positions.append(i)
            i += 1
        else:
            caractere = texte[i + j]
            decalage = j - table.get(caractere, -1)
            i += max(1, decalage)
    return positions, comparaisons
```

3. Sur `"A" × 20` contre le motif `"BBBBB"` (absent du texte), la recherche naïve effectue 16 comparaisons (une par position testée, l'échec étant immédiat dès le premier caractère comparé à chaque position), alors que Boyer-Moore n'en effectue que 4 : comme aucun `'A'` n'apparaît dans le motif, chaque échec entraîne un décalage maximal (de la longueur du motif), si bien que très peu de positions sont testées au total. Ce cas est particulièrement favorable à Boyer-Moore car le mauvais caractère rencontré (`'A'`) est totalement absent du motif, ce qui permet le plus grand décalage possible à chaque étape.

### Exercice 6

```python
def compte_occurrences_naif(texte, motif):
    n, m = len(texte), len(motif)
    compteur = 0
    for i in range(n - m + 1):
        if texte[i:i + m] == motif:
            compteur += 1
    return compteur
```
