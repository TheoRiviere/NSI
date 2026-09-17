# Chapitre 5 — Architecture séquentielle (von Neumann)

## Objectifs

- Décrire les grands composants d'un ordinateur selon l'architecture de von Neumann.
- Comprendre le cycle fetch-decode-execute (chercher-décoder-exécuter).
- Comprendre pourquoi cette architecture est dite « séquentielle » et ses limites.
- Simuler, en Python, l'exécution d'un programme au niveau machine.

## Prérequis

- Représentation binaire des nombres — chapitre 1.

---

## 1. L'architecture de von Neumann

### 1.1 Principe général

La quasi-totalité des ordinateurs actuels repose sur une organisation proposée en 1945 par le mathématicien John von Neumann, appelée **architecture de von Neumann**. Son idée centrale est que les **instructions** d'un programme et les **données** qu'il manipule sont stockées dans la **même mémoire**, sous la même forme (des suites de bits).

Cette architecture comporte quatre grands composants :

- **L'unité centrale de traitement** (CPU, *Central Processing Unit*, aussi appelée processeur), elle-même composée de :
  - **l'unité de commande** (ou unité de contrôle), qui pilote le déroulement du programme (lit les instructions, les décode, coordonne leur exécution) ;
  - **l'unité arithmétique et logique** (UAL, ou ALU en anglais), qui effectue les calculs (additions, comparaisons, opérations logiques...) ;
  - des **registres**, petites zones de mémoire très rapides internes au processeur, utilisées pour stocker temporairement les valeurs en cours de traitement.
- **La mémoire principale** (RAM), qui stocke à la fois le programme (ses instructions) et les données qu'il manipule.
- **Les bus**, qui relient ces composants entre eux et transportent l'information (bus de données, bus d'adresses, bus de commande).
- **Les périphériques d'entrée-sortie** (clavier, écran, disque dur...), qui permettent d'échanger de l'information avec l'extérieur.

### 1.2 Une architecture « séquentielle »

On qualifie cette architecture de **séquentielle** car les instructions sont, par défaut, exécutées **les unes après les autres**, dans l'ordre où elles sont stockées en mémoire — un seul flux d'instructions est traité à la fois par un cœur de processeur donné (les processeurs modernes comportent souvent plusieurs cœurs, capables d'exécuter plusieurs flux d'instructions en parallèle, mais chaque cœur, pris individuellement, reste fondamentalement séquentiel).

---

## 2. Le cycle fetch-decode-execute

Le processeur exécute un programme en répétant indéfiniment un cycle en trois étapes, pour chaque instruction :

1. **Fetch (chercher)** : le processeur va chercher, en mémoire, l'instruction à exécuter, à l'adresse indiquée par un registre spécial appelé **compteur ordinal** (ou *program counter*, PC), qui contient l'adresse de la prochaine instruction à exécuter.
2. **Decode (décoder)** : l'unité de commande interprète l'instruction lue (quel type d'opération, quels opérandes).
3. **Execute (exécuter)** : l'opération correspondante est effectuée, éventuellement en utilisant l'UAL pour un calcul, et en général le compteur ordinal est incrémenté pour pointer vers l'instruction suivante (sauf en cas de **saut**, où le compteur ordinal est directement modifié pour pointer ailleurs).

Ce cycle se répète en boucle jusqu'à ce qu'une instruction d'arrêt soit rencontrée.

---

## 3. Simuler une machine simplifiée en Python

Pour bien comprendre ce mécanisme, on peut écrire un simulateur très simplifié d'un processeur. On représente la mémoire par un dictionnaire `{adresse: valeur}`, et un programme par une liste d'instructions, chaque instruction étant un tuple `(operation, operande)`. On dispose d'un seul registre, l'**accumulateur**, qui joue le rôle de registre de travail pour les calculs.

### 3.1 Le jeu d'instructions

| Instruction | Effet |
|---|---|
| `("LOAD", adresse)` | charge la valeur de `memoire[adresse]` dans l'accumulateur |
| `("STORE", adresse)` | range la valeur de l'accumulateur dans `memoire[adresse]` |
| `("ADD", adresse)` | ajoute `memoire[adresse]` à l'accumulateur |
| `("SUB", adresse)` | soustrait `memoire[adresse]` de l'accumulateur |
| `("JUMP", adresse)` | fait pointer le compteur ordinal vers `adresse` (saut inconditionnel) |
| `("JUMPIFZERO", adresse)` | saute vers `adresse` seulement si l'accumulateur vaut 0 |
| `("HALT",)` | arrête l'exécution |

### 3.2 Implémentation du cycle fetch-decode-execute

```python
def executer_programme(programme, memoire):
    accumulateur = 0
    compteur_ordinal = 0
    while True:
        # --- FETCH ---
        instruction = programme[compteur_ordinal]
        operation = instruction[0]

        # --- DECODE / EXECUTE ---
        if operation == "LOAD":
            accumulateur = memoire[instruction[1]]
            compteur_ordinal += 1
        elif operation == "STORE":
            memoire[instruction[1]] = accumulateur
            compteur_ordinal += 1
        elif operation == "ADD":
            accumulateur += memoire[instruction[1]]
            compteur_ordinal += 1
        elif operation == "SUB":
            accumulateur -= memoire[instruction[1]]
            compteur_ordinal += 1
        elif operation == "JUMP":
            compteur_ordinal = instruction[1]
        elif operation == "JUMPIFZERO":
            if accumulateur == 0:
                compteur_ordinal = instruction[1]
            else:
                compteur_ordinal += 1
        elif operation == "HALT":
            break
    return accumulateur, memoire
```

Remarquez la structure de la boucle `while True`, qui correspond exactement au cycle fetch-decode-execute : à chaque tour, on **cherche** l'instruction pointée par le compteur ordinal (`programme[compteur_ordinal]`), on la **décode** (le test sur `operation`), puis on l'**exécute** (le bloc de code correspondant), avant de recommencer.

### 3.3 Exemple : additionner deux valeurs

```python
programme = [
    ("LOAD", 0),     # accumulateur <- memoire[0]
    ("ADD", 1),      # accumulateur <- accumulateur + memoire[1]
    ("STORE", 2),    # memoire[2] <- accumulateur
    ("HALT",),
]
memoire = {0: 5, 1: 7, 2: 0}

executer_programme(programme, memoire)
# memoire[2] vaut maintenant 12
```

### 3.4 Exemple : une boucle avec un saut

L'instruction `JUMP` permet de revenir en arrière dans le programme, ce qui est le mécanisme de base permettant de réaliser une **boucle** au niveau machine (alors qu'un langage comme Python propose directement des structures `for`/`while`, celles-ci sont, une fois le programme traduit en langage machine, décomposées en instructions de saut de ce type).

```python
# Compte combien de fois on peut soustraire 1 a memoire[0] avant d'atteindre 0
memoire = {0: 5, 1: 0, 2: 1}   # memoire[0]=n, memoire[1]=compteur, memoire[2]=constante 1

programme = [
    ("LOAD", 0),         # 0: charge n
    ("JUMPIFZERO", 8),   # 1: si n == 0, aller a la fin (adresse 8)
    ("SUB", 2),          # 2: n = n - 1
    ("STORE", 0),        # 3: sauvegarde n
    ("LOAD", 1),         # 4: charge le compteur
    ("ADD", 2),          # 5: compteur = compteur + 1
    ("STORE", 1),        # 6: sauvegarde le compteur
    ("JUMP", 0),         # 7: retourne au debut de la boucle
    ("HALT",),           # 8: fin
]

executer_programme(programme, memoire)
# memoire[1] vaut alors 5 : la boucle s'est executee 5 fois
```

Ce petit programme illustre bien le mécanisme fondamental des boucles au niveau matériel : ce n'est rien d'autre qu'un **saut arrière** conditionné par un test, répété jusqu'à ce que la condition change.

---

## Synthèse

| Composant / notion | Rôle |
|---|---|
| Unité de commande | Pilote le déroulement du programme (fetch-decode) |
| UAL (ALU) | Effectue les calculs (execute) |
| Registres | Mémoire rapide interne au processeur (ex : accumulateur, compteur ordinal) |
| Mémoire principale | Stocke instructions **et** données (principe de von Neumann) |
| Bus | Transportent l'information entre les composants |
| Cycle fetch-decode-execute | Chercher l'instruction → la décoder → l'exécuter, en boucle |
| Saut (JUMP) | Mécanisme de base permettant de réaliser boucles et branchements |

*Prochaine étape suggérée : Chapitre 6 — Réseaux : transmission de données.*
