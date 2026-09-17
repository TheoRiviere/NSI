# Chapitre 1 — Représentation des données : bases numériques et types de base

## Objectifs

- Convertir un nombre entre les bases 2, 10 et 16.
- Représenter un nombre entier relatif en complément à 2.
- Comprendre pourquoi les nombres flottants sont représentés de façon imprécise en machine.
- Manipuler le type booléen et ses opérateurs.
- Comprendre les principes des encodages de caractères (ASCII, Unicode).

## Prérequis

- Notion de division euclidienne (quotient, reste).
- Types de base en Python (`int`, `float`, `bool`, `str`).

---

## 1. Pourquoi représenter l'information en binaire ?

Un ordinateur est constitué de circuits électroniques qui ne connaissent que deux états stables : un courant présent ou absent, une tension haute ou basse. On associe conventionnellement le chiffre `1` à l'un de ces états et `0` à l'autre. Toute donnée manipulée par un ordinateur — un nombre, un texte, une image, un son — est donc, au niveau le plus bas, une suite de **bits** (binary digit), c'est-à-dire de 0 et de 1.

On regroupe généralement les bits par paquets de 8, appelés **octets** (en anglais *bytes*). Un octet permet de représenter `2^8 = 256` valeurs différentes (de 0 à 255).

---

## 2. Conversion entre les bases 2, 10 et 16

### 2.1 Principe d'un système de numération en base *b*

Dans le système décimal (base 10), le nombre `present as 2024` signifie :

```
2024 = 2×10³ + 0×10² + 2×10¹ + 4×10⁰
```

De la même façon, un nombre écrit en base *b* avec des chiffres `dₙ dₙ₋₁ ... d₁ d₀` vaut :

```
dₙ×bⁿ + dₙ₋₁×bⁿ⁻¹ + ... + d₁×b¹ + d₀×b⁰
```

- En **base 2** (binaire), les chiffres possibles sont 0 et 1.
- En **base 16** (hexadécimale), les chiffres possibles sont 0 à 9 puis A, B, C, D, E, F (pour 10 à 15). La base 16 est très utilisée en informatique car elle permet d'écrire de façon compacte des groupes de 4 bits (un chiffre hexadécimal code exactement 4 bits).

### 2.2 Conversion binaire → décimal

On applique directement la formule ci-dessus.

```python
def binaire_vers_decimal(b):
    """Convertit une chaîne binaire (ex: '1101') en entier décimal."""
    resultat = 0
    for bit in b:
        resultat = resultat * 2 + int(bit)
    return resultat

binaire_vers_decimal("1101")   # 13
```

**Astuce de lecture (méthode de Horner) :** on parcourt les bits de gauche à droite, en multipliant le résultat courant par 2 et en ajoutant le bit lu. C'est ce que fait le code ci-dessus.

### 2.3 Conversion décimal → binaire

On effectue des divisions euclidiennes successives par 2 ; les restes obtenus, lus de bas en haut (du dernier au premier), forment l'écriture binaire.

```python
def decimal_vers_binaire(n):
    """Convertit un entier positif en chaîne binaire."""
    if n == 0:
        return "0"
    chiffres = []
    while n > 0:
        chiffres.append(str(n % 2))
        n //= 2
    return "".join(reversed(chiffres))

decimal_vers_binaire(13)   # '1101'
```

**Vérification :** `13 = 8+4+1 = 1×2³+1×2²+0×2¹+1×2⁰`, ce qui s'écrit bien `1101`.

En Python, ces conversions existent aussi nativement :

```python
bin(13)        # '0b1101'   (préfixe 0b pour le binaire)
int("1101", 2) # 13         (conversion binaire -> décimal)
hex(255)       # '0xff'     (préfixe 0x pour l'hexadécimal)
int("ff", 16)  # 255
```

### 2.4 Conversion binaire ↔ hexadécimal

Comme `16 = 2⁴`, on peut convertir directement en regroupant les bits par paquets de 4, sans passer par le décimal :

```
1111 1011  →  F B  →  0xFB
```

---

## 3. Représentation des entiers relatifs : le complément à 2

### 3.1 Le problème

Comment représenter un nombre **négatif** avec des 0 et des 1 ? On pourrait imaginer réserver un bit pour le signe, mais cette solution (dite « signe et magnitude ») complique les calculs (il existe alors deux écritures de 0) et n'est pas celle utilisée en pratique par les ordinateurs.

La solution retenue est le **complément à 2**.

### 3.2 Principe, sur *n* bits

- Si le nombre `n` est **positif ou nul**, on l'écrit simplement en binaire classique, complété par des 0 à gauche jusqu'à occuper les *n* bits.
- Si le nombre `n` est **négatif**, on calcule sa représentation comme l'écriture binaire de `2ⁿᵇⁱᵗˢ + n` (qui est un nombre positif puisque `n` est négatif).

```python
def complement_a_2(n, nb_bits):
    """Représente l'entier relatif n sur nb_bits bits, en complément à 2."""
    if n >= 0:
        return decimal_vers_binaire(n).zfill(nb_bits)
    else:
        valeur = 2**nb_bits + n
        return decimal_vers_binaire(valeur).zfill(nb_bits)

complement_a_2(5, 8)    # '00000101'
complement_a_2(-5, 8)   # '11111011'
```

Pour décoder une écriture en complément à 2, le principe est symétrique : si le bit de poids fort (le premier bit) vaut 1, le nombre est négatif, et on retranche `2ⁿᵇⁱᵗˢ` à sa valeur binaire lue normalement.

```python
def decoder_complement_a_2(b):
    """Décode une chaîne binaire en complément à 2 vers un entier relatif."""
    nb_bits = len(b)
    valeur = binaire_vers_decimal(b)
    if b[0] == "1":
        valeur -= 2**nb_bits
    return valeur

decoder_complement_a_2("11111011")   # -5
```

### 3.3 Pourquoi ce choix ? L'intérêt du complément à 2

Le complément à 2 a une propriété remarquable : l'**addition binaire habituelle** (celle qu'on ferait « à la main », en posant l'addition et en gérant les retenues) donne directement le bon résultat, que les nombres soient positifs ou négatifs, sans qu'il soit nécessaire de traiter le signe à part. C'est ce qui rend les circuits arithmétiques des processeurs beaucoup plus simples : un seul circuit d'addition suffit pour tous les cas.

Le bit de poids fort joue le rôle d'indicateur de signe (0 pour un nombre positif ou nul, 1 pour un nombre négatif), mais ce n'est qu'une **conséquence** de la construction, pas une règle appliquée séparément.

### 3.4 Plage de valeurs représentables

Sur *n* bits en complément à 2, on peut représenter les entiers de `-2ⁿ⁻¹` à `2ⁿ⁻¹ - 1`. Par exemple, sur 8 bits : de -128 à 127 (soit 256 valeurs au total, ce qui est cohérent avec les `2⁸ = 256` combinaisons de bits possibles).

C'est cette plage limitée qui explique le phénomène de **dépassement de capacité** (*overflow*) : si un calcul produit un résultat en dehors de cette plage, le résultat stocké sera erroné (il « boucle » silencieusement). Python, contrairement au langage C par exemple, gère automatiquement des entiers de taille arbitraire et ne connaît donc pas ce problème pour le type `int` — mais celui-ci reste bien réel dans la plupart des langages et dans le matériel.

---

## 4. Les nombres flottants : une représentation approchée

### 4.1 Le problème de la représentation des nombres réels

Un nombre réel comme `1/3` a une infinité de chiffres après la virgule en base 10, et cela reste vrai en base 2 pour de nombreux nombres qui pourtant s'écrivent simplement en base 10, comme `0.1`. Comme la mémoire d'un ordinateur est finie, il est impossible de stocker exactement tous les nombres réels : on utilise une représentation **approchée**, appelée représentation à **virgule flottante**, normalisée par la norme IEEE 754 (que le programme officiel ne demande pas de détailler, mais dont il faut connaître la conséquence pratique).

### 4.2 Conséquence pratique : des erreurs d'arrondi

```python
>>> 0.1 + 0.2
0.30000000000000004
>>> 0.1 + 0.2 == 0.3
False
```

Ce résultat surprenant n'est **pas un bug** de Python : `0.1` et `0.2` ne peuvent pas être représentés exactement en binaire (de la même façon que `1/3` ne peut pas s'écrire exactement avec un nombre fini de chiffres en base 10), donc de minuscules erreurs d'arrondi s'accumulent au fil des calculs.

**Conséquence pour la programmation :** il ne faut **jamais** comparer deux flottants avec `==`. On compare plutôt que leur écart est suffisamment petit :

```python
abs((0.1 + 0.2) - 0.3) < 1e-9   # True : bonne pratique de comparaison
```

---

## 5. Le type booléen

Le type `bool` ne contient que deux valeurs : `True` et `False`. Il est fondamental en informatique car il correspond exactement à un bit d'information (0 ou 1), et il est au cœur de toutes les structures de décision (`if`) et de répétition conditionnelle (`while`).

### 5.1 Les opérateurs logiques de base

| Opérateur | Signification | Exemple |
|---|---|---|
| `and` | ET logique | `True and False` → `False` |
| `or` | OU logique (inclusif) | `True or False` → `True` |
| `not` | NON logique | `not True` → `False` |

Le OU **exclusif** (xor, vrai si les deux valeurs diffèrent) n'est pas un opérateur natif de Python, mais peut se construire :

```python
def xor(a, b):
    return (a or b) and not (a and b)

xor(True, False)   # True
xor(True, True)    # False
```

### 5.2 Tables de vérité

| a | b | a and b | a or b | xor(a, b) |
|---|---|---|---|---|
| Faux | Faux | Faux | Faux | Faux |
| Faux | Vrai | Faux | Vrai | Vrai |
| Vrai | Faux | Faux | Vrai | Vrai |
| Vrai | Vrai | Vrai | Vrai | Faux |

---

## 6. Encodage des caractères

### 6.1 Le principe

Pour stocker du texte, il faut associer à chaque caractère un nombre entier (son **code**), qui sera lui-même représenté en binaire. C'est ce qu'on appelle un encodage.

### 6.2 ASCII

Le code **ASCII** (American Standard Code for Information Interchange), datant des années 1960, encode 128 caractères (lettres non accentuées, chiffres, ponctuation, caractères de contrôle) sur 7 bits.

```python
ord('A')   # 65
chr(65)    # 'A'
ord('a')   # 97   (notez : 'a' et 'A' ont des codes différents)
```

### 6.3 Les limites de l'ASCII, et l'arrivée d'Unicode

L'ASCII ne permet pas de représenter les lettres accentuées (é, à, ç...), ni les caractères d'autres écritures (cyrillique, chinois, arabe...) ni les émojis. De nombreux encodages « étendus » sur 8 bits sont apparus (comme Latin-1/ISO-8859-1 pour l'Europe de l'Ouest), mais ils étaient incompatibles entre eux : un même octet pouvait représenter un caractère différent selon l'encodage utilisé.

**Unicode** a été créé pour résoudre ce problème en attribuant un identifiant unique (un *code point*) à chaque caractère existant dans le monde, indépendamment de la façon dont il est ensuite stocké en mémoire.

### 6.4 UTF-8 : un encodage à taille variable

**UTF-8** est aujourd'hui l'encodage Unicode le plus utilisé (notamment sur le Web). Son principe : les caractères ASCII (les 128 premiers) sont codés sur **un seul octet**, exactement comme en ASCII (ce qui assure la compatibilité avec les anciens textes), tandis que les autres caractères sont codés sur 2, 3 ou 4 octets.

```python
texte = "café"
texte.encode('utf-8')     # b'caf\xc3\xa9'  -> 5 octets (le "é" prend 2 octets)
len(texte)                 # 4  (4 caractères)
len(texte.encode('utf-8')) # 5  (5 octets)

texte.encode('latin-1')    # b'caf\xe9'     -> 4 octets (le "é" prend 1 octet ici)
```

Ce exemple illustre bien la différence entre le **nombre de caractères** d'une chaîne et le **nombre d'octets** nécessaires pour la stocker, qui dépend de l'encodage choisi.

---

## Synthèse

| Notion | Point clé à retenir |
|---|---|
| Base 2 / 10 / 16 | Même principe positionnel ; la base 16 regroupe 4 bits par chiffre |
| Complément à 2 | Représentation des entiers relatifs permettant l'addition binaire directe |
| Plage sur *n* bits (signé) | de `-2ⁿ⁻¹` à `2ⁿ⁻¹ - 1` |
| Flottants | Représentation approchée : ne jamais comparer avec `==` |
| Booléens | `and`, `or`, `not` ; le xor se construit à partir de ces opérateurs |
| ASCII | 128 caractères, 7 bits, pas d'accents |
| Unicode / UTF-8 | Identifiant universel par caractère ; UTF-8 encode sur 1 à 4 octets |

*Prochaine étape suggérée : Chapitre 2 — Types construits : p-uplets, tableaux, dictionnaires.*
