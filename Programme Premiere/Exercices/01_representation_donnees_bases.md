# Chapitre 1 — Représentation des données : bases numériques et types de base
## Fiche d'exercices

*Première NSI — Python 3*

---

### Exercice 1 — Conversions de bases

1. Convertir à la main `42` (en base 10) en binaire, puis vérifier avec `decimal_vers_binaire` du cours.
2. Convertir à la main `101010` (en binaire) en décimal, puis vérifier avec `binaire_vers_decimal`.
3. Convertir `200` (en base 10) en hexadécimal à l'aide de la fonction native `hex`.
4. Convertir `"A3"` (en hexadécimal) en décimal à l'aide de la fonction native `int`.
5. Écrire une fonction `binaire_vers_hexadecimal(b)` qui convertit une chaîne binaire (dont la longueur est un multiple de 4) directement en chaîne hexadécimale, **sans passer par un entier Python** (on pourra découper la chaîne en paquets de 4 bits).

### Exercice 2 — Complément à 2

On travaille sur 8 bits.

1. Représenter `7` et `-7` en complément à 2 sur 8 bits.
2. Décoder la chaîne `"11111111"` : quel entier relatif représente-t-elle sur 8 bits ? Et `"01111111"` ?
3. Quelle est la plus petite valeur représentable sur 4 bits en complément à 2 ? La plus grande ?
4. On représente `8` avec la fonction `complement_a_2` du cours mais avec `nb_bits = 4`. Que se passe-t-il ? Décoder le résultat obtenu avec `decoder_complement_a_2` : que constate-t-on ? Comment appelle-t-on ce phénomène ?

### Exercice 3 — Flottants

1. Calculer `0.1 + 0.1 + 0.1` en Python. Le résultat est-il exactement égal à `0.3` ?
2. Un(e) élève écrit le code suivant pour vérifier qu'un compte est à zéro après une série d'opérations :
   ```python
   if solde == 0.0:
       print("Compte soldé")
   ```
   Pourquoi ce test est-il dangereux ? Proposer une version corrigée.
3. Que renvoie `round(0.1 + 0.2, 2)` ? En quoi cela peut-il être utile pour afficher un résultat à un utilisateur, sans pour autant résoudre le problème de la comparaison stricte ?

### Exercice 4 — Booléens

1. Construire la table de vérité de l'expression `(a or b) and not a`.
2. Sans utiliser directement l'opérateur `and`, écrire une fonction `mon_and(a, b)` qui se comporte comme `and`, en utilisant uniquement `or` et `not` (indication : lois de De Morgan).
3. Écrire une fonction `nand(a, b)` qui renvoie `not (a and b)`. Vérifier que l'on peut exprimer `not a` comme `nand(a, a)`.

### Exercice 5 — Encodages

1. Quel est le code ASCII (décimal) du caractère `'e'` ? de `'E'` ? de `'z'` ? Que remarque-t-on entre `'e'` et `'E'` ?
2. La chaîne `"Noël"` contient 4 caractères. Combien d'octets occupe-t-elle en UTF-8 ? En Latin-1 ? Justifier la différence.
3. Afficher `list("Noël".encode('utf-8'))`. Combien de valeurs (octets) obtient-on pour le caractère `'ë'` ? Que peut-on en déduire sur l'encodage UTF-8 des caractères non-ASCII ?

---

## Corrigés

### Exercice 1

1. `42 = 32+8+2 = 101010` en binaire. `decimal_vers_binaire(42)` renvoie bien `'101010'`.
2. `101010 = 1×32+0×16+1×8+0×4+1×2+0×1 = 42`. `binaire_vers_decimal("101010")` renvoie bien `42`.
3. `hex(200)` renvoie `'0xc8'`.
4. `int("A3", 16)` renvoie `163`.
5.
```python
TABLE = {
    "0000": "0", "0001": "1", "0010": "2", "0011": "3",
    "0100": "4", "0101": "5", "0110": "6", "0111": "7",
    "1000": "8", "1001": "9", "1010": "A", "1011": "B",
    "1100": "C", "1101": "D", "1110": "E", "1111": "F",
}

def binaire_vers_hexadecimal(b):
    paquets = [b[i:i+4] for i in range(0, len(b), 4)]
    return "".join(TABLE[p] for p in paquets)
```

### Exercice 2

1. `7` sur 8 bits : `00000111`. `-7` sur 8 bits (complément à 2) : `11111001` (on calcule `256 - 7 = 249`, soit `11111001` en binaire).
2. `"11111111"` décode en `-1` (bit de poids fort à 1, donc on retranche `256` à `255`, ce qui donne `-1`). `"01111111"` décode en `127` (bit de poids fort à 0, donc lecture normale).
3. Sur 4 bits, la plage va de `-2³ = -8` à `2³ - 1 = 7`.
4. `complement_a_2(8, 4)` renvoie `"1000"` — la fonction ne détecte pas d'erreur, elle renvoie simplement l'écriture binaire de `8` sur 4 bits (qui « occupe » toute la plage sans avertissement). Or, décoder `"1000"` avec `decoder_complement_a_2` donne `-8` : le bit de poids fort étant à 1, la valeur `8`, qui pourtant est positive, est interprétée à tort comme négative ! C'est exactement le phénomène de **dépassement de capacité** (*overflow*) : `8` n'est pas représentable sur 4 bits signés (la plage s'arrête à `7`), donc son écriture binaire est mal interprétée.

### Exercice 3

1. `0.1 + 0.1 + 0.1` vaut `0.30000000000000004` en Python, donc **non**, ce n'est pas exactement `0.3` (erreurs d'arrondi liées à la représentation binaire approchée des flottants).
2. Ce test est dangereux car, après une série de calculs, le `solde` peut valoir quelque chose comme `1e-17` au lieu de `0.0` exactement, à cause des erreurs d'arrondi accumulées : le test `== 0.0` échouerait alors à tort. Version corrigée :
   ```python
   if abs(solde) < 1e-9:
       print("Compte soldé")
   ```
3. `round(0.1 + 0.2, 2)` renvoie `0.3` (affiché avec 2 décimales, l'erreur d'arrondi de la 17ᵉ décimale disparaît). Cela peut être utile pour un **affichage** lisible à l'utilisateur, mais ne résout pas le problème pour une **comparaison** interne : la valeur stockée en mémoire reste imprécise même si son affichage arrondi paraît exact ; on continue donc à comparer avec une tolérance (`abs(x-y) < 1e-9`) plutôt qu'avec `==`, y compris après un `round`.

### Exercice 4

1.

| a | b | a or b | not a | (a or b) and not a |
|---|---|---|---|---|
| F | F | F | V | F |
| F | V | V | V | V |
| V | F | V | F | F |
| V | V | V | F | F |

2. Loi de De Morgan : `a and b` équivaut à `not ((not a) or (not b))`.
```python
def mon_and(a, b):
    return not ((not a) or (not b))
```
3.
```python
def nand(a, b):
    return not (a and b)

# Vérification : nand(a, a) == not (a and a) == not a
assert nand(True, True) == (not True)
assert nand(False, False) == (not False)
```

### Exercice 5

1. `ord('e')` vaut `101`, `ord('E')` vaut `69`, `ord('z')` vaut `122`. On remarque que le code d'une lettre minuscule est différent (plus grand, de 32) que celui de la même lettre en majuscule : `101 - 69 = 32`.
2. `"Noël".encode('utf-8')` occupe **5 octets** (le `ë` est codé sur 2 octets, les 3 autres caractères ASCII sur 1 octet chacun). `"Noël".encode('latin-1')` occupe **4 octets** (Latin-1 code tous les caractères qu'il connaît, dont `ë`, sur exactement 1 octet).
3. `list("Noël".encode('utf-8'))` renvoie `[78, 111, 195, 171, 108]` : 5 valeurs pour 4 caractères. Le `ë` (un seul caractère) est codé par **deux octets** (`195` et `171`). On en déduit qu'en UTF-8, un caractère non-ASCII peut occuper plusieurs octets : le nombre d'octets d'une chaîne encodée en UTF-8 n'est donc pas toujours égal à son nombre de caractères.
