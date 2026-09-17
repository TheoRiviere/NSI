# Chapitre 5 — Architecture séquentielle (von Neumann)
## TP sur machine — Étendre le simulateur de processeur

*Première NSI — Python 3 — Durée indicative : 1h30 à 2h*

---

## Objectifs

- Ajouter une trace d'exécution au simulateur du cours (visualiser le cycle fetch-decode-execute en action).
- Ajouter une nouvelle instruction au jeu d'instructions.
- Écrire un programme machine réalisant une division euclidienne par soustractions successives.

---

## Partie A — Tracer l'exécution

**A.1.** Recopier `executer_programme` du cours, en la renommant `executer_programme_trace`, et en ajoutant un paramètre `tracer=False`. Lorsque `tracer` vaut `True`, la fonction doit enregistrer, à **chaque cycle** (avant d'exécuter l'instruction), un tuple `(compteur_ordinal, instruction, accumulateur)` dans une liste `historique`, qui sera renvoyée à la fin en plus des résultats habituels (indication : la fonction renverra donc `accumulateur, memoire, nb_cycles, historique`).

**A.2.** La fonction doit aussi compter et renvoyer le **nombre total de cycles** (nombre de tours de la boucle `while`) effectués.

**A.3.** Tester sur le programme d'addition du cours (`LOAD 0 ; ADD 1 ; STORE 2 ; HALT`) et afficher l'historique complet. Combien de cycles ce programme effectue-t-il ?

---

## Partie B — Ajouter une instruction : le saut conditionnel négatif

Le jeu d'instructions du cours ne permet de tester que l'égalité à zéro (`JUMPIFZERO`). On souhaite ajouter une nouvelle instruction `("JUMPIFNEG", adresse)`, qui saute vers `adresse` uniquement si l'accumulateur est **strictement négatif**.

**B.1.** Copier votre fonction d'exécution et y ajouter la gestion de cette nouvelle instruction.

**B.2.** Cette instruction va permettre d'écrire un programme calculant le **reste** de la division euclidienne de `memoire[0]` par `memoire[1]`, en soustrayant `memoire[1]` de `memoire[0]` de façon répétée, jusqu'à ce que le résultat devienne négatif (à ce moment-là, on est allé « un tour de trop », donc le reste est la valeur de `memoire[0]` juste **avant** cette dernière soustraction).

On donne le squelette suivant à compléter (les numéros de ligne correspondent aux adresses des instructions) :
```python
memoire = {0: 17, 1: 5, 2: 0}   # a = 17, b = 5 -> on veut calculer 17 % 5

programme = [
    ("LOAD", 0),          # 0: charge a
    ("SUB", 1),           # 1: acc = a - b
    ("JUMPIFNEG", ???),   # 2: si acc < 0, on s'arrête : a (non modifié) est le reste -> aller à HALT
    ("STORE", 0),         # 3: sinon, a = a - b (on valide la soustraction)
    ("LOAD", 0),          # 4: recharge a (pour reboucler proprement)
    ("JUMP", ???),        # 5: retourne à l'adresse de SUB
    ("HALT",),            # 6
]
```

**B.3.** Compléter les adresses manquantes (`???`), exécuter le programme, et vérifier que `memoire[0]` vaut bien `2` à la fin (puisque `17 = 3×5 + 2`).

**B.4.** Combien de cycles ce programme effectue-t-il au total ? Le compter avec votre fonction de la partie A.

---

## Corrigé indicatif

```python
# --- Partie A ---
def executer_programme_trace(programme, memoire, tracer=False):
    accumulateur = 0
    compteur_ordinal = 0
    nb_cycles = 0
    historique = []
    while True:
        nb_cycles += 1
        instruction = programme[compteur_ordinal]
        operation = instruction[0]
        if tracer:
            historique.append((compteur_ordinal, instruction, accumulateur))

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
            compteur_ordinal = instruction[1] if accumulateur == 0 else compteur_ordinal + 1
        elif operation == "JUMPIFNEG":
            compteur_ordinal = instruction[1] if accumulateur < 0 else compteur_ordinal + 1
        elif operation == "HALT":
            break
    return accumulateur, memoire, nb_cycles, historique


programme_addition = [
    ("LOAD", 0),
    ("ADD", 1),
    ("STORE", 2),
    ("HALT",),
]
memoire_addition = {0: 5, 1: 7, 2: 0}
acc, mem, cycles, historique = executer_programme_trace(programme_addition, memoire_addition, tracer=True)
print("Nombre de cycles :", cycles)   # 4
for etape in historique:
    print(etape)


# --- Partie B ---
memoire = {0: 17, 1: 5, 2: 0}

programme = [
    ("LOAD", 0),          # 0
    ("SUB", 1),            # 1
    ("JUMPIFNEG", 6),      # 2 : si négatif, aller directement au HALT (adresse 6)
    ("STORE", 0),           # 3
    ("LOAD", 0),             # 4
    ("JUMP", 1),               # 5 : reboucle vers SUB
    ("HALT",),                   # 6
]

acc, mem, cycles, _ = executer_programme_trace(programme, memoire)
print("Reste de 17 par 5 :", mem[0])   # 2
print("Nombre de cycles :", cycles)     # 19
```

**Remarque sur B.4 :** ce programme effectue `19` cycles pour calculer `17 % 5`. On observe que le nombre de cycles dépend directement du **nombre de soustractions nécessaires** (ici 4 soustractions, car `17 - 5 - 5 - 5 = 2 < 5`, puis une soustraction de trop détectée), donc du quotient de la division : plus `a` est grand par rapport à `b`, plus le programme prend de cycles pour s'exécuter. C'est une première illustration, au niveau machine, de ce qui deviendra plus tard la notion de **coût d'un algorithme** (chapitre sur l'algorithmique).
