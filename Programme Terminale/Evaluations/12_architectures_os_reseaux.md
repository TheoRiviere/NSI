# Chapitre 12 — Architectures matérielles, OS et réseaux
## Évaluation

*Terminale NSI — Durée : 55 min — Barème sur 20 points*

---

### Partie 1 — Questions de cours (9 points)

**Question 1 (2 pts).** Qu'est-ce qu'un système sur puce ? Citer deux composants qu'il peut intégrer.

**Question 2 (2 pts).** Qu'est-ce qu'un interblocage ? À quelle notion algorithmique vue en cours peut-on le relier ?

**Question 3 (3 pts).** Expliquer la différence entre les protocoles de routage RIP et OSPF.

**Question 4 (2 pts).** Quelle est la différence fondamentale entre chiffrement symétrique et chiffrement asymétrique ?

---

### Partie 2 — Application (7 points)

On donne le réseau de routeurs pondéré suivant :
```python
reseau = {
    "X": [("Y", 3), ("Z", 8)],
    "Y": [("X", 3), ("Z", 2), ("W", 6)],
    "Z": [("X", 8), ("Y", 2), ("W", 1)],
    "W": [("Y", 6), ("Z", 1)],
}
```

**Question 5 (3 pts).** Avec un protocole de type RIP, combien de sauts sépare-t-il `X` de `W`, et quelle route obtient-on (on pourra en proposer plusieurs si elles sont équivalentes) ?

**Question 6 (4 pts).** Avec un protocole de type OSPF, quelle est la route de moindre coût de `X` à `W`, et quel est son coût total ? Détailler le calcul.

---

### Partie 3 — Écrire du code (4 points)

**Question 7 (4 pts).** On donne un dictionnaire `attente_de` représentant un graphe d'attente entre processus (comme dans le cours). Écrire une fonction `nombre_de_processus_bloques(attente_de)` qui renvoie le nombre de processus impliqués dans **au moins un** cycle d'attente (on pourra s'appuyer sur `detecter_interblocage_simple` du cours, appelée pour chaque processus, en adaptant la fonction pour qu'elle renvoie aussi la liste des processus visités en cas de cycle détecté).

---

## Corrigé et barème détaillé

### Partie 1 (9 pts)

**Q1 (2 pts)** — Un système sur puce intègre, sur un seul circuit, plusieurs composants autrefois séparés (1 pt). Exemples : microprocesseur, mémoire, interfaces radio/filaires, gestion d'énergie, contrôleur vidéo (1 pt pour deux exemples corrects).

**Q2 (2 pts)** — Un interblocage est une situation où plusieurs processus attendent chacun une ressource détenue par un autre, si bien qu'aucun ne peut progresser (1 pt). On peut le relier à la détection de **cycle dans un graphe orienté** (le graphe d'attente) (1 pt).

**Q3 (3 pts)** — RIP choisit la route qui minimise le nombre de sauts, sans tenir compte d'autre critère (1,5 pt). OSPF choisit la route qui minimise un coût associé à chaque liaison (débit, latence...), ce qui peut conduire à une route différente de celle de RIP même si elle compte plus de sauts (1,5 pt).

**Q4 (2 pts)** — Le chiffrement symétrique utilise une seule et même clé pour chiffrer et déchiffrer (1 pt), alors que le chiffrement asymétrique utilise une paire de clés distinctes : une clé publique pour chiffrer, une clé privée pour déchiffrer (1 pt).

### Partie 2 (7 pts)

**Q5 (3 pts)** — La route directe `X → Z → W` compte 2 sauts. Une autre route à 2 sauts n'existe pas ici via `Y` seul (`X → Y → W` compte aussi 2 sauts). RIP pourrait donc choisir l'une ou l'autre de ces routes à 2 sauts. *(2 pts pour le nombre de sauts correct, 1 pt pour une route valide.)*

**Q6 (4 pts)** — Coût de `X → Z → W` : `8 + 1 = 9`. Coût de `X → Y → W` : `3 + 6 = 9`. Coût de `X → Y → Z → W` : `3 + 2 + 1 = 6`. La route de moindre coût est donc `X → Y → Z → W`, de coût total **6**. *(2 pts pour l'exploration d'au moins deux routes candidates, 2 pts pour l'identification correcte de la route optimale et son coût.)*

### Partie 3 (4 pts)

**Q7 (4 pts)**
```python
def detecter_cycle_depuis(attente_de, depart):
    visites = []
    courant = depart
    while courant in attente_de:
        if courant in visites:
            return visites[visites.index(courant):]   # le cycle proprement dit
        visites.append(courant)
        courant = attente_de[courant]
    return []

def nombre_de_processus_bloques(attente_de):
    bloques = set()
    for processus in attente_de:
        cycle = detecter_cycle_depuis(attente_de, processus)
        bloques.update(cycle)
    return len(bloques)
```
*(2 pts pour une détection de cycle correcte par processus ; 2 pts pour l'agrégation correcte sans double comptage, via un ensemble.)*

---

**Barème global : 9 + 7 + 4 = 20 points.**
