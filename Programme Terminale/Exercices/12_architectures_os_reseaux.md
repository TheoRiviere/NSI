# Chapitre 12 — Architectures matérielles, OS et réseaux
## Fiche d'exercices

*Terminale NSI — Python 3*

---

### Exercice 1 — Systèmes sur puce

1. Citer trois composants que l'on peut trouver intégrés sur un système sur puce de smartphone.
2. Quel est l'intérêt principal d'intégrer ces composants sur une seule puce plutôt que de les séparer ?

### Exercice 2 — Ordonnancement en tourniquet

En reprenant `simuler_tourniquet` du cours :

1. Dérouler à la main `simuler_tourniquet([("A", 6), ("B", 2)], 3)` : donner la trace complète (liste des passages).
2. Calculer, pour chaque processus de la question 1, le temps total écoulé avant sa dernière tranche d'exécution (temps de complétion).
3. Modifier `simuler_tourniquet` pour qu'elle renvoie, en plus de la trace, le nombre total de « passages » (changements de processus actif) effectués.

### Exercice 3 — Interblocage

1. Construire un exemple de graphe d'attente à **trois** processus (`P1`, `P2`, `P3`) formant un interblocage (un cycle).
2. Vérifier votre exemple avec `detecter_interblocage_simple` du cours.
3. Construire un exemple à trois processus **sans** interblocage, où pourtant `P1` attend `P2` et `P2` attend `P3`.

### Exercice 4 — Routage

On donne le réseau pondéré suivant :
```python
reseau = {
    "A": [("B", 4), ("C", 1)],
    "B": [("A", 4), ("D", 1)],
    "C": [("A", 1), ("D", 6)],
    "D": [("B", 1), ("C", 6)],
}
```

1. Avec un protocole de type **RIP** (nombre de sauts), quelle serait la route choisie de `A` à `D` ? Combien de sauts compte-t-elle ?
2. Avec un protocole de type **OSPF** (coût), quelle serait la route choisie de `A` à `D`, en utilisant `route_moindre_cout` du cours ? Quel est son coût total ?
3. Ces deux routes sont-elles identiques ? Commenter.

### Exercice 5 — Chiffrement

1. Chiffrer le message `"OUI"` avec `chiffrer_xor` et la clé `bytes([5, 5, 5])`, puis vérifier que le déchiffrement redonne bien `"OUI"`.
2. Pourquoi ce chiffrement XOR très simple ne serait-il pas utilisable tel quel pour sécuriser de vraies communications (donner au moins une raison) ?
3. Expliquer, en une phrase, pourquoi on combine en pratique chiffrement symétrique et asymétrique plutôt que d'utiliser uniquement l'un des deux.

---

## Corrigés

### Exercice 1

1. Par exemple : microprocesseur, mémoire, interface Wi-Fi/Bluetooth, gestion d'énergie, contrôleur vidéo.
2. Réduire la distance parcourue par les signaux (gain de vitesse) et le nombre de composants à alimenter séparément (gain en consommation d'énergie).

### Exercice 2

1. Trace : `[("A", 3), ("B", 2), ("A", 3)]` — `A` (temps restant 6) exécute 3, puis `B` (temps restant 2, inférieur à la tranche) exécute ses 2 unités et se termine, puis `A` (temps restant 3) termine ses 3 dernières unités.
2. `B` se termine après `3 + 2 = 5` unités de temps écoulées. `A` se termine après `3 + 2 + 3 = 8` unités de temps écoulées.

```python
def simuler_tourniquet_compte(processus, tranche):
    file = list(processus)
    trace = []
    passages = 0
    while len(file) > 0:
        nom, temps_restant = file.pop(0)
        temps_execute = min(tranche, temps_restant)
        trace.append((nom, temps_execute))
        passages += 1
        temps_restant -= temps_execute
        if temps_restant > 0:
            file.append((nom, temps_restant))
    return trace, passages
```

### Exercice 3

1. Par exemple : `{"P1": "P2", "P2": "P3", "P3": "P1"}` (P1 attend P2, qui attend P3, qui attend à nouveau P1 : cycle).
2. `detecter_interblocage_simple({"P1": "P2", "P2": "P3", "P3": "P1"})` renvoie `True`.
3. Par exemple : `{"P1": "P2", "P2": "P3"}` — `P3` n'attend rien, il finira par libérer sa ressource, ce qui permettra à `P2` puis à `P1` de progresser : pas de cycle, pas d'interblocage.

### Exercice 4

1. RIP (nombre de sauts) : la route `A → C → D` compte 2 sauts, tout comme `A → B → D` : les deux sont équivalentes pour RIP (2 sauts chacune).
2. OSPF (coût) : la route `A → B → D` a un coût de `4 + 1 = 5` ; la route `A → C → D` a un coût de `1 + 6 = 7`. OSPF choisit donc `A → B → D`, de coût `5`.
3. Non : bien que les deux routes comptent le même nombre de sauts (2), OSPF préfère `A → B → D` car son coût total est plus faible, alors que RIP, indifférent au coût, pourrait tout aussi bien choisir `A → C → D`, moins performante en pratique.

### Exercice 5

1.
```python
cle = bytes([5, 5, 5])
chiffre = chiffrer_xor("OUI", cle)
assert dechiffrer_xor(chiffre, cle) == "OUI"
```
2. Une clé aussi courte et répétée (3 octets) serait très facile à retrouver par analyse statistique du message chiffré (surtout si l'on connaît une partie du texte en clair) ; de plus, un chiffrement XOR simple ne garantit aucune protection contre la modification du message par un tiers (il ne garantit que la confidentialité, pas l'intégrité).
3. Le chiffrement asymétrique est trop lent pour chiffrer de gros volumes de données, mais permet d'échanger une clé de façon sécurisée sans rencontre préalable ; on l'utilise donc uniquement pour transmettre une clé symétrique, qui elle-même chiffre rapidement le reste de la communication.
