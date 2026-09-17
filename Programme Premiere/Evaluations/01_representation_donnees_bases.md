# Chapitre 1 — Représentation des données : bases numériques et types de base
## Évaluation

*Première NSI — Durée : 50 min — Barème sur 20 points*

---

### Partie 1 — Questions de cours (7 points)

**Question 1 (2 pts).** Qu'appelle-t-on un bit ? Un octet ? Combien de valeurs différentes peut-on représenter avec un octet ?

**Question 2 (2 pts).** Expliquer pourquoi on ne doit jamais comparer deux nombres flottants avec l'opérateur `==` en Python. Quelle est la bonne pratique à adopter à la place ?

**Question 3 (3 pts).** Qu'est-ce que le complément à 2 ? Pourquoi ce choix de représentation est-il intéressant pour la réalisation des circuits d'addition d'un processeur (par rapport, par exemple, à une représentation « signe et magnitude » où un bit indiquerait juste le signe) ?

---

### Partie 2 — Conversions et calculs (8 points)

**Question 4 (2 pts).** Convertir `36` (en base 10) en binaire.

**Question 5 (2 pts).** Convertir `110011` (en binaire) en décimal.

**Question 6 (2 pts).** Représenter `9` puis `-9` en complément à 2, sur 8 bits.

**Question 7 (2 pts).** On donne l'écriture en complément à 2 sur 8 bits : `11110000`. Quel entier relatif représente-t-elle ? Détailler le calcul.

---

### Partie 3 — Écrire du code (5 points)

**Question 8 (3 pts).** Écrire une fonction `compter_octets_utf8(texte)` qui renvoie le nombre d'octets nécessaires pour encoder la chaîne `texte` en UTF-8 (indication : utiliser la méthode `.encode('utf-8')` puis `len`).

**Question 9 (2 pts).** Sans exécuter de code, si `texte = "Salut à tous !"` (14 caractères, dont un caractère accentué `à`), que renverra `len(texte)` ? Que renverra `compter_octets_utf8(texte)` ? Justifier la différence éventuelle.

---

## Corrigé et barème détaillé

### Partie 1 (7 pts)

**Q1 (2 pts)** — Un bit est la plus petite unité d'information, ne pouvant prendre que deux valeurs (0 ou 1) (1 pt). Un octet est un regroupement de 8 bits ; il permet de représenter `2⁸ = 256` valeurs différentes (1 pt).

**Q2 (2 pts)** — Les nombres flottants sont représentés en machine de façon **approchée** (la plupart des nombres décimaux, comme `0.1`, n'ont pas d'écriture binaire finie exacte), donc deux calculs mathématiquement égaux peuvent donner des résultats stockés légèrement différents à cause des erreurs d'arrondi (1 pt). La bonne pratique consiste à comparer l'écart absolu entre les deux valeurs à un très petit seuil, par exemple `abs(a - b) < 1e-9` (1 pt).

**Q3 (3 pts)** — Le complément à 2 est une façon de représenter les entiers relatifs sur *n* bits : les nombres positifs s'écrivent normalement, et un nombre négatif `n` s'écrit comme l'écriture binaire de `2ⁿᵇⁱᵗˢ + n` (1,5 pt). Son intérêt principal est que l'**addition binaire classique** (celle utilisée pour les entiers positifs) fonctionne directement et donne le bon résultat, que les opérandes soient positifs ou négatifs, sans traitement particulier du signe — contrairement à une représentation « signe et magnitude » qui nécessiterait un circuit spécifique pour gérer les cas de signes différents, et qui de plus posséderait deux écritures distinctes pour zéro (1,5 pt).

### Partie 2 (8 pts)

**Q4 (2 pts)** — `36 = 32 + 4 = 100100` en binaire.

**Q5 (2 pts)** — `110011 = 1×32 + 1×16 + 0×8 + 0×4 + 1×2 + 1×1 = 32+16+2+1 = 51`.

**Q6 (2 pts)** — `9` sur 8 bits : `00001001` (1 pt). `-9` sur 8 bits : on calcule `256 - 9 = 247`, soit `11110111` (1 pt).

**Q7 (2 pts)** — Le bit de poids fort de `11110000` est `1`, donc le nombre est négatif. Sa valeur binaire lue normalement est `1×128+1×64+1×32+1×16 = 240`. On retranche `2⁸ = 256` : `240 - 256 = -16`. La chaîne représente donc **-16**.

### Partie 3 (5 pts)

**Q8 (3 pts)**
```python
def compter_octets_utf8(texte):
    return len(texte.encode('utf-8'))
```
*(2 pts pour l'utilisation correcte de `.encode('utf-8')`, 1 pt pour `len`.)*

**Q9 (2 pts)** — `len(texte)` renvoie `14` (le nombre de caractères de la chaîne, indépendamment de leur encodage) (1 pt). `compter_octets_utf8(texte)` renvoie `15` : en UTF-8, les caractères ASCII (dont l'espace, le point d'exclamation, les lettres non accentuées) occupent 1 octet chacun, mais le caractère accentué `à` occupe 2 octets, d'où un octet de plus que le nombre de caractères (1 pt).

---

**Barème global : 7 + 8 + 5 = 20 points.**
