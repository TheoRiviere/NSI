# Chapitre 2 — Interface et implémentation
## TP sur machine — Comparer des implémentations d'une même structure

*Terminale NSI — Python 3 — Durée indicative : 1h30*

---

## Objectifs

- Implémenter une même interface de deux façons différentes.
- Écrire un code client qui ne dépend que de l'interface, pas de l'implémentation.
- Mesurer expérimentalement une différence de performance entre deux implémentations.

---

## Partie A — Deux implémentations d'une pile

**A.1.** Recopier les classes `PileListe` et `PileTableauFixe` du cours.

**A.2.** Écrire une fonction `evaluer_polonaise(expression, pile)` qui évalue une expression arithmétique écrite en **notation polonaise inversée** (RPN), où `expression` est une liste de chaînes comme `["3", "4", "+", "2", "*"]` (ce qui représente `(3 + 4) * 2`). Le paramètre `pile` doit être utilisé pour stocker les résultats intermédiaires, en n'utilisant que son interface (`empiler`, `depiler`, `est_vide`).

*Rappel du principe :* on parcourt l'expression ; si on lit un nombre, on l'empile ; si on lit un opérateur, on dépile les deux derniers opérandes, on applique l'opérateur, et on empile le résultat.

**A.3.** Tester `evaluer_polonaise` avec `PileListe()` **et** avec `PileTableauFixe(20)` sur plusieurs expressions. Vérifier que les deux implémentations donnent le même résultat.

---

## Partie B — Deux implémentations d'une file

**B.1.** Recopier les classes `FileListe` et `FileDeuxPiles` du cours.

**B.2.** Écrire une fonction `simuler_guichet(file, arrivees)` qui reçoit une file et une liste de noms de clients, enfile tous les clients dans l'ordre, puis les défile un par un en affichant `"Client servi : <nom>"`.

**B.3.** Tester cette fonction avec les deux implémentations sur une même liste de clients, et vérifier que l'ordre de passage est identique.

---

## Partie C — Mesurer une différence de performance

**C.1.** À l'aide du module `time`, écrire un script qui :
1. crée une `FileListe` et une `FileDeuxPiles` ;
2. enfile `20000` entiers dans chacune ;
3. défile tous les éléments de chacune ;
4. affiche le temps d'exécution total pour chaque implémentation.

```python
import time

def chronometrer(file):
    debut = time.perf_counter()
    for i in range(20000):
        file.enfiler(i)
    while not file.est_vide():
        file.defiler()
    fin = time.perf_counter()
    return fin - debut
```

**C.2.** Comparer les deux durées obtenues. Le résultat est-il cohérent avec l'analyse théorique du coût de `defiler()` faite en cours ? Rédiger une phrase de conclusion.

---

## Corrigé indicatif

```python
class PileListe:
    def __init__(self):
        self._elements = []
    def empiler(self, e):
        self._elements.append(e)
    def depiler(self):
        return self._elements.pop()
    def sommet(self):
        return self._elements[-1]
    def est_vide(self):
        return len(self._elements) == 0


def evaluer_polonaise(expression, pile):
    operateurs = {
        "+": lambda a, b: a + b,
        "-": lambda a, b: a - b,
        "*": lambda a, b: a * b,
        "/": lambda a, b: a / b,
    }
    for token in expression:
        if token in operateurs:
            b = pile.depiler()
            a = pile.depiler()
            pile.empiler(operateurs[token](a, b))
        else:
            pile.empiler(float(token))
    return pile.depiler()


def simuler_guichet(file, arrivees):
    for client in arrivees:
        file.enfiler(client)
    while not file.est_vide():
        client = file.defiler()
        print(f"Client servi : {client}")
```

Résultat attendu pour `evaluer_polonaise(["3", "4", "+", "2", "*"], PileListe())` : `14.0`.

Pour la partie C, on observe expérimentalement que `FileListe` devient sensiblement plus lente que `FileDeuxPiles` lorsque le nombre d'éléments augmente : c'est la conséquence directe du coût de `pop(0)` (proportionnel à la taille de la file, donc un coût total quadratique sur `n` opérations) contre le coût amorti constant de `FileDeuxPiles`.
