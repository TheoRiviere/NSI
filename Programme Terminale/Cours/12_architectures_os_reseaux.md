# Terminale NSI — Chapitre 12
# Architectures matérielles, systèmes d'exploitation et réseaux

*Support de cours — Python 3*

---

## Objectifs du chapitre

- Identifier les composants d'un système sur puce.
- Décrire la création et l'ordonnancement des processus, comprendre le risque d'interblocage.
- Comprendre les principes des protocoles de routage RIP et OSPF, en lien avec les graphes.
- Décrire les principes du chiffrement symétrique et asymétrique.

**Prérequis :** graphes (chapitre 5), pour la partie sur le routage.

---

## 12.1 Systèmes sur puce (SoC)

Un **système sur puce** (*System on Chip*, SoC) regroupe, sur un seul circuit intégré, des composants qui étaient autrefois séparés : un **microprocesseur**, une ou plusieurs **mémoires locales**, des **interfaces radio et filaires** (Wi-Fi, Bluetooth, USB...), des circuits de **gestion d'énergie**, un **contrôleur vidéo**, parfois un **accélérateur graphique**, et des **réseaux sur puce** qui relient ces composants entre eux.

> **Exemple.** Le circuit intégré d'un smartphone est un SoC typique : il intègre le processeur principal, la puce graphique, les modems Wi-Fi/4G/5G, et la gestion de la batterie, le tout sur quelques millimètres carrés.

**Intérêt de l'intégration.** Rassembler ces composants sur une seule puce réduit la distance que les signaux électriques doivent parcourir (gain de **vitesse**) et limite le nombre de composants séparés à alimenter (gain en **consommation d'énergie**), au prix d'une moindre flexibilité (on ne peut pas remplacer un seul composant défectueux indépendamment des autres).

---

## 12.2 Gestion des processus par le système d'exploitation

Un **processus** est un programme en cours d'exécution. Le **système d'exploitation** (OS) a pour rôle de créer les processus, de leur allouer des ressources (mémoire, temps de calcul du processeur...), et de gérer leur exécution.

### Création et ordonnancement

Lorsqu'un programme est lancé, l'OS crée un processus, lui alloue une zone mémoire, puis planifie son exécution : plusieurs processus se partagent en réalité le temps du (ou des) processeur(s), chacun exécutant tour à tour une petite tranche de temps (*ordonnancement*). Une stratégie simple d'ordonnancement, le **tourniquet** (*round-robin*), attribue à chaque processus, à tour de rôle, une tranche de temps fixe.

```python
def simuler_tourniquet(processus, tranche):
    """Simule un ordonnancement en tourniquet.
    processus : liste de tuples (nom, temps_restant)
    tranche : durée maximale allouée à chaque passage
    """
    file = list(processus)
    trace = []
    while len(file) > 0:
        nom, temps_restant = file.pop(0)
        temps_execute = min(tranche, temps_restant)
        trace.append((nom, temps_execute))
        temps_restant -= temps_execute
        if temps_restant > 0:
            file.append((nom, temps_restant))
    return trace
```

**Exemple :** `simuler_tourniquet([("A", 5), ("B", 3), ("C", 8)], 4)` simule l'exécution de trois processus, chacun recevant des tranches de 4 unités de temps à tour de rôle, jusqu'à leur terminaison.

### Interblocage (*deadlock*)

Un **interblocage** se produit lorsque plusieurs processus attendent chacun une ressource détenue par un autre, sans qu'aucun ne puisse jamais progresser.

> **Exemple classique.** Le processus `P1` détient la ressource `R1` et attend `R2` ; le processus `P2` détient `R2` et attend `R1`. Ni `P1` ni `P2` ne peut avancer : ils sont bloqués indéfiniment, chacun attendant que l'autre libère sa ressource.

On peut représenter la situation « P1 attend une ressource détenue par P2 » comme un arc `P1 → P2` dans un **graphe d'attente**. Un interblocage correspond alors exactement à un **cycle** dans ce graphe — on retrouve ainsi la détection de cycle du chapitre 5 :

```python
# Illustration "débranchée" d'un interblocage, à l'aide du graphe d'attente
def detecter_interblocage_simple(attente_de):
    """attente_de : dictionnaire {processus: processus dont il attend une ressource}.
    Renvoie True si un cycle d'attente est détecté (interblocage)."""
    for depart in attente_de:
        visites = set()
        courant = depart
        while courant in attente_de:
            if courant in visites:
                return True   # on retombe sur un processus déjà vu : cycle d'attente
            visites.add(courant)
            courant = attente_de[courant]
    return False

# P1 détient R1 et attend R2 (détenue par P2) ; P2 détient R2 et attend R1 (détenue par P1)
graphe_attente = {"P1": "P2", "P2": "P1"}
print(detecter_interblocage_simple(graphe_attente))   # True : interblocage détecté
```

---

## 12.3 Protocoles de routage

Sur internet, les **routeurs** acheminent les paquets de données d'un réseau à un autre, en utilisant une **table de routage** qui indique, pour chaque destination, le prochain routeur (le prochain « saut ») vers lequel transmettre le paquet.

### RIP (Routing Information Protocol)

RIP choisit la route qui minimise le **nombre de sauts** (le nombre de routeurs intermédiaires traversés), sans tenir compte d'autre critère (comme le débit ou la congestion des liaisons). Cela revient exactement à chercher le plus court chemin, en nombre d'arêtes, dans un graphe non pondéré — l'algorithme vu au chapitre 5 (`plus_court_chemin`, basé sur un parcours en largeur) s'applique directement.

```python
reseau_routeurs = {
    "R1": ["R2", "R3"],
    "R2": ["R1", "R4"],
    "R3": ["R1", "R4"],
    "R4": ["R2", "R3", "R5"],
    "R5": ["R4"],
}

def plus_court_chemin(graphe, depart, arrivee):
    file = [depart]
    predecesseur = {depart: None}
    while len(file) > 0:
        sommet = file.pop(0)
        if sommet == arrivee:
            chemin = []
            while sommet is not None:
                chemin.append(sommet)
                sommet = predecesseur[sommet]
            chemin.reverse()
            return chemin
        for voisin in graphe[sommet]:
            if voisin not in predecesseur:
                predecesseur[voisin] = sommet
                file.append(voisin)
    return None

print(plus_court_chemin(reseau_routeurs, "R1", "R5"))   # route RIP : ["R1", "R2", "R4", "R5"] (3 sauts)
```

### OSPF (Open Shortest Path First)

OSPF choisit la route qui minimise un **coût** associé à chaque liaison (qui peut refléter le débit, la latence, la fiabilité...), et non simplement le nombre de sauts. Une liaison rapide mais longue en nombre de sauts peut ainsi être préférée à une liaison courte mais lente.

```python
reseau_pondere = {
    "R1": [("R2", 2), ("R3", 5)],
    "R2": [("R1", 2), ("R4", 1)],
    "R3": [("R1", 5), ("R4", 1)],
    "R4": [("R2", 1), ("R3", 1), ("R5", 3)],
    "R5": [("R4", 3)],
}

def route_moindre_cout(graphe, depart, arrivee):
    cout = {depart: 0}
    predecesseur = {depart: None}
    a_traiter = [depart]
    while len(a_traiter) > 0:
        # on choisit le sommet non encore validé de plus petit coût connu (recherche naïve)
        sommet = min(a_traiter, key=lambda s: cout[s])
        a_traiter.remove(sommet)
        for voisin, poids in graphe[sommet]:
            nouveau_cout = cout[sommet] + poids
            if voisin not in cout or nouveau_cout < cout[voisin]:
                cout[voisin] = nouveau_cout
                predecesseur[voisin] = sommet
                a_traiter.append(voisin)
    chemin = []
    sommet = arrivee
    while sommet is not None:
        chemin.append(sommet)
        sommet = predecesseur[sommet]
    chemin.reverse()
    return chemin, cout[arrivee]
```

Sur ce réseau pondéré, la route de moindre coût de `"R1"` à `"R5"` passe par `R2 → R4` (coût `2 + 1 + 3 = 6`) plutôt que par `R3` (coût `5 + 1 + 3 = 9`), alors que RIP, qui ignore les coûts, aurait pu considérer les deux routes comme équivalentes (3 sauts chacune).

> **Lien avec le cours d'algorithmique.** `route_moindre_cout` est une version simplifiée de l'algorithme de Dijkstra, qui généralise le parcours en largeur à des graphes pondérés.

---

## 12.4 Sécurisation des communications

### Chiffrement symétrique

En chiffrement **symétrique**, la **même clé** sert à chiffrer et à déchiffrer un message. Elle doit donc être connue des deux parties, et rester secrète pour quiconque d'autre.

```python
def chiffrer_xor(message, cle):
    """Chiffrement symétrique simple (XOR), à but pédagogique uniquement."""
    return bytes(c ^ cle[i % len(cle)] for i, c in enumerate(message.encode()))

def dechiffrer_xor(chiffre, cle):
    return bytes(c ^ cle[i % len(cle)] for i, c in enumerate(chiffre)).decode()

cle_secrete = bytes([42, 17, 99])
message_chiffre = chiffrer_xor("SALUT", cle_secrete)
message_dechiffre = dechiffrer_xor(message_chiffre, cle_secrete)
print(message_dechiffre)   # "SALUT"
```

> **Avantage / inconvénient.** Le chiffrement symétrique est rapide, mais pose un problème : comment les deux parties peuvent-elles se transmettre la clé secrète sans qu'elle soit interceptée sur un réseau non sécurisé ?

### Chiffrement asymétrique

En chiffrement **asymétrique**, chaque utilisateur possède une **paire de clés** : une **clé publique** (diffusée à tous) et une **clé privée** (gardée secrète). Ce qui est chiffré avec la clé publique d'une personne ne peut être déchiffré qu'avec sa clé privée correspondante.

```python
# Exemple pédagogique très simplifié, inspiré du principe de RSA (nombres volontairement petits)
def generer_cles(p, q, e):
    n = p * q
    indicatrice = (p - 1) * (q - 1)
    # on suppose e choisi premier avec indicatrice ; on calcule d tel que e*d = 1 (mod indicatrice)
    d = pow(e, -1, indicatrice)
    return (e, n), (d, n)   # (clé publique), (clé privée)

def chiffrer_asymetrique(message, cle_publique):
    e, n = cle_publique
    return [pow(ord(caractere), e, n) for caractere in message]

def dechiffrer_asymetrique(chiffre, cle_privee):
    d, n = cle_privee
    return "".join(chr(pow(c, d, n)) for c in chiffre)

cle_publique, cle_privee = generer_cles(61, 53, 17)   # exemple pédagogique, nombres trop petits pour être sûrs
chiffre = chiffrer_asymetrique("HI", cle_publique)
clair = dechiffrer_asymetrique(chiffre, cle_privee)
print(clair)   # "HI"
```

> **Attention.** Cet exemple illustre le **principe mathématique** (exponentiation modulaire) sur lequel repose RSA, un algorithme de chiffrement asymétrique réel — mais avec des nombres bien trop petits pour offrir une quelconque sécurité en pratique (un vrai système RSA utilise des nombres de plusieurs centaines de chiffres).

### Utilisation conjointe : sécuriser une connexion HTTPS

En pratique, le chiffrement asymétrique est **plus lent** que le chiffrement symétrique. On combine donc les deux : lors de l'établissement d'une connexion HTTPS, le navigateur et le serveur utilisent le chiffrement **asymétrique** uniquement pour échanger, de façon sécurisée, une **clé symétrique** temporaire (appelée clé de session) ; le reste de la communication est ensuite chiffré avec cette clé symétrique, beaucoup plus rapide à utiliser pour de gros volumes de données.

---

## 12.5 Synthèse

| Notion | Définition |
|---|---|
| Système sur puce (SoC) | Circuit intégrant plusieurs composants auparavant séparés (processeur, mémoire, interfaces, gestion d'énergie...) |
| Processus | Programme en cours d'exécution, créé et géré par le système d'exploitation |
| Ordonnancement | Répartition du temps processeur entre plusieurs processus (par exemple, en tourniquet) |
| Interblocage | Situation où plusieurs processus s'attendent mutuellement sans pouvoir progresser |
| RIP | Protocole de routage basé sur le nombre de sauts (plus court chemin non pondéré) |
| OSPF | Protocole de routage basé sur un coût associé à chaque liaison (plus court chemin pondéré) |
| Chiffrement symétrique | Une même clé pour chiffrer et déchiffrer |
| Chiffrement asymétrique | Une clé publique pour chiffrer, une clé privée pour déchiffrer |

*Ce chapitre conclut le programme de Terminale NSI couvert par cette série de documents.*
