# Chapitre 1 — Représentation des données : bases numériques et types de base
## TP sur machine — Bases, complément à 2, flottants et encodages

*Première NSI — Python 3 — Durée indicative : 1h30*

---

## Objectifs

- Écrire un convertisseur de base généralisé (pas seulement binaire/décimal/hexadécimal).
- Détecter automatiquement un dépassement de capacité en complément à 2.
- Observer expérimentalement l'accumulation des erreurs d'arrondi sur les flottants.
- Manipuler `ord`/`chr` pour construire un chiffrement simple.

---

## Partie A — Convertisseur de base généralisé

On souhaite généraliser les fonctions du cours pour qu'elles fonctionnent avec **n'importe quelle base entre 2 et 16**, pas seulement 2 et 16.

**A.1.** On donne la chaîne de chiffres possibles :
```python
CHIFFRES = "0123456789ABCDEF"
```
Écrire une fonction `decimal_vers_base(n, base)` qui convertit un entier positif `n` en une chaîne représentant `n` dans la base donnée (entre 2 et 16), en utilisant `CHIFFRES` pour obtenir le bon symbole (indication : reprendre le principe des divisions successives du cours, mais diviser par `base` au lieu de 2, et utiliser `CHIFFRES[reste]` pour obtenir le chiffre correspondant).

**A.2.** Écrire la fonction réciproque `base_vers_decimal(s, base)` qui convertit une chaîne `s` écrite dans la base donnée vers un entier décimal (indication : `CHIFFRES.index(c)` donne la valeur du chiffre `c`).

**A.3.** Vérifier que `decimal_vers_base(42, 2) == "101010"`, `decimal_vers_base(255, 16) == "FF"` et `decimal_vers_base(42, 8) == "52"` (base octale).

**A.4.** Écrire un petit programme de test qui tire 200 entiers aléatoires entre 0 et 100000 (`random.randint`), les convertit dans une base aléatoire parmi {2, 8, 16} avec `decimal_vers_base`, puis reconvertit le résultat en décimal avec `base_vers_decimal`, et vérifie par un `assert` que l'on retrouve le nombre de départ.

---

## Partie B — Détecter un dépassement de capacité

**B.1.** Recopier `complement_a_2` du cours.

**B.2.** Écrire une fonction `complement_a_2_securise(n, nb_bits)` qui commence par vérifier si `n` est bien représentable sur `nb_bits` bits signés (c'est-à-dire s'il appartient à l'intervalle `[-2^(nb_bits-1), 2^(nb_bits-1) - 1]`) ; si ce n'est pas le cas, elle doit **lever une exception** avec `raise ValueError(...)` et un message explicite ; sinon, elle renvoie le résultat de `complement_a_2(n, nb_bits)`.

**B.3.** Vérifier que `complement_a_2_securise(8, 4)` lève bien une exception, alors que `complement_a_2_securise(7, 4)` et `complement_a_2_securise(-8, 4)` fonctionnent normalement.

**B.4. (bonus)** Modifier la fonction pour qu'elle affiche aussi, en cas de dépassement, ce que renverrait (à tort) la fonction non sécurisée `complement_a_2`, afin de bien visualiser l'erreur silencieuse que produirait un système qui ne vérifierait pas les dépassements.

---

## Partie C — Mesurer expérimentalement l'imprécision des flottants

**C.1.** Écrire une fonction `somme_naive(valeur, n)` qui additionne `n` fois la valeur `valeur` dans une boucle (en partant d'un total de `0.0`), et renvoie le total.

**C.2.** Pour `n` prenant successivement les valeurs `10`, `100`, `1000`, `10000`, calculer `somme_naive(0.1, n)`, la valeur théoriquement attendue (`n * 0.1`), et l'écart absolu entre les deux (`abs(total - attendu)`). Afficher les résultats dans un tableau.

**C.3.** Que constate-t-on sur l'évolution de l'écart lorsque `n` augmente ? Cela signifie-t-il que Python « se trompe de plus en plus » à chaque opération, ou bien que les petites erreurs d'arrondi s'accumulent au fil des additions répétées ?

---

## Partie D — Chiffrement de César avec `ord`/`chr`

Le chiffrement de César consiste à décaler chaque lettre de l'alphabet d'un nombre fixe de rangs (par exemple, avec un décalage de 3, `A` devient `D`, `B` devient `E`, etc., et l'alphabet « boucle » après `Z`).

**D.1.** Écrire une fonction `chiffrer_cesar(texte, decalage)` qui chiffre un texte (on suppose qu'il peut contenir des majuscules, des minuscules, et d'autres caractères comme des espaces, qui doivent rester inchangés). Indication : pour une lettre minuscule `c`, sa position dans l'alphabet est `ord(c) - ord('a')` ; après décalage et « bouclage » avec l'opérateur `%`, on reconstruit le caractère avec `chr(...)`. On distinguera les lettres majuscules et minuscules avec `c.isupper()`.

**D.2.** Écrire la fonction `dechiffrer_cesar(texte, decalage)` (indication : c'est un chiffrement avec un décalage opposé).

**D.3.** Vérifier que `dechiffrer_cesar(chiffrer_cesar("Bonjour NSI", 3), 3) == "Bonjour NSI"`.

**D.4. (bonus)** Ce chiffrement protège-t-il efficacement un message ? Combien existe-t-il de décalages possibles (donc de clés) au total ? Écrire un petit programme qui essaie tous les décalages possibles sur un message chiffré inconnu et affiche chaque résultat, pour montrer qu'on peut « casser » ce chiffrement très rapidement par force brute.

---

## Corrigé indicatif

```python
import random

# --- Partie A ---
CHIFFRES = "0123456789ABCDEF"

def decimal_vers_base(n, base):
    if n == 0:
        return "0"
    chiffres = []
    while n > 0:
        chiffres.append(CHIFFRES[n % base])
        n //= base
    return "".join(reversed(chiffres))

def base_vers_decimal(s, base):
    resultat = 0
    for c in s:
        resultat = resultat * base + CHIFFRES.index(c)
    return resultat

assert decimal_vers_base(42, 2) == "101010"
assert decimal_vers_base(255, 16) == "FF"
assert decimal_vers_base(42, 8) == "52"

for _ in range(200):
    n = random.randint(0, 100000)
    base = random.choice([2, 8, 16])
    s = decimal_vers_base(n, base)
    assert base_vers_decimal(s, base) == n
print("Partie A : tests réussis")


# --- Partie B ---
def complement_a_2(n, nb_bits):
    if n >= 0:
        return bin(n)[2:].zfill(nb_bits)
    else:
        valeur = 2**nb_bits + n
        return bin(valeur)[2:].zfill(nb_bits)

def complement_a_2_securise(n, nb_bits):
    minimum = -(2**(nb_bits - 1))
    maximum = 2**(nb_bits - 1) - 1
    if n < minimum or n > maximum:
        raise ValueError(
            f"{n} non représentable sur {nb_bits} bits (plage [{minimum}, {maximum}])"
        )
    return complement_a_2(n, nb_bits)

try:
    complement_a_2_securise(8, 4)
except ValueError as e:
    print("Partie B : exception bien levée ->", e)

assert complement_a_2_securise(7, 4) == "0111"
assert complement_a_2_securise(-8, 4) == "1000"


# --- Partie C ---
def somme_naive(valeur, n):
    total = 0.0
    for _ in range(n):
        total += valeur
    return total

print("\nPartie C :")
print(f"{'n':>6} | {'total':>20} | {'écart':>22}")
for n in [10, 100, 1000, 10000]:
    total = somme_naive(0.1, n)
    attendu = n * 0.1
    erreur = abs(total - attendu)
    print(f"{n:>6} | {total:>20} | {erreur:>22}")


# --- Partie D ---
def chiffrer_cesar(texte, decalage):
    resultat = ""
    for c in texte:
        if c.isalpha():
            base = ord('A') if c.isupper() else ord('a')
            resultat += chr((ord(c) - base + decalage) % 26 + base)
        else:
            resultat += c
    return resultat

def dechiffrer_cesar(texte, decalage):
    return chiffrer_cesar(texte, -decalage)

message = "Bonjour NSI"
chiffre = chiffrer_cesar(message, 3)
print("\nPartie D :", chiffre)
assert dechiffrer_cesar(chiffre, 3) == message

# Bonus D.4 : attaque par force brute
for decalage_essai in range(26):
    print(decalage_essai, "->", dechiffrer_cesar(chiffre, decalage_essai))
```

**Réponse C.3 :** l'écart absolu augmente avec `n`, mais cela ne signifie pas que chaque opération devient plus imprécise : chaque addition introduit une toute petite erreur d'arrondi (de l'ordre de `10⁻¹⁶`), et plus on effectue d'additions, plus ces petites erreurs s'accumulent (l'écart croît globalement avec le nombre d'opérations effectuées, même si la relation n'est pas parfaitement linéaire). C'est pour cette raison qu'il faut être particulièrement prudent avec les flottants lors de sommes portant sur de très nombreuses valeurs.

**Réponse D.4 :** il n'existe que 26 décalages possibles (un alphabet de 26 lettres), donc 26 « clés » : un programme peut essayer systématiquement les 26 possibilités en une fraction de seconde et repérer celle qui donne un texte lisible. Le chiffrement de César n'offre donc **aucune sécurité réelle** face à une attaque par force brute informatique.
