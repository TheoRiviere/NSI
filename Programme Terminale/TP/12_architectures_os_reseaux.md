# Chapitre 12 — Architectures matérielles, OS et réseaux
## TP sur machine — Ordonnancement, routage et chiffrement

*Terminale NSI — Python 3 — Durée indicative : 1h30 à 2h*

---

## Objectifs

- Simuler un ordonnanceur de processus et observer l'effet de la taille de la tranche de temps.
- Comparer RIP et OSPF sur un même réseau.
- Mettre en œuvre un échange de clé inspiré du principe utilisé en HTTPS.

---

## Partie A — Ordonnancement

**A.1.** Recopier `simuler_tourniquet` du cours.

**A.2.** Écrire une fonction `temps_de_completion(processus, tranche)` qui renvoie, pour chaque processus, le temps total écoulé avant qu'il ait fini de s'exécuter (indication : additionner les tranches successives jusqu'à ce que chaque processus atteigne un temps restant nul).

**A.3.** Comparer les temps de complétion obtenus pour `[("A", 10), ("B", 1), ("C", 1)]` avec une tranche de `1` puis avec une tranche de `10`. Quel est l'effet d'une petite tranche sur les processus courts (`B` et `C`) ?

---

## Partie B — Routage

**B.1.** Recopier `plus_court_chemin` (RIP) et `route_moindre_cout` (OSPF) du cours.

**B.2.** Construire un réseau pondéré d'au moins 6 routeurs de votre choix, avec des poids variés.

**B.3.** Pour trois couples de routeurs différents, comparer la route choisie par RIP et celle choisie par OSPF. Trouver, si possible, un couple où les deux routes diffèrent.

**B.4. (bonus)** Modifier `route_moindre_cout` pour qu'elle affiche, à chaque étape, le sommet en cours de traitement et son coût, afin de visualiser le déroulement de l'algorithme.

---

## Partie C — Chiffrement : simuler un échange de clé

On simule le scénario d'une connexion sécurisée : le client génère une clé symétrique, la chiffre avec la clé publique du serveur, puis l'envoie ; le serveur la déchiffre avec sa clé privée ; ensuite, les deux communiquent avec cette clé symétrique.

**C.1.** Recopier `generer_cles`, `chiffrer_asymetrique`, `dechiffrer_asymetrique`, `chiffrer_xor`, `dechiffrer_xor` du cours.

**C.2.** Écrire un script qui :
1. génère une paire de clés asymétriques pour le « serveur » ;
2. côté « client », choisit une clé symétrique aléatoire (par exemple 3 octets tirés avec `random.randint(0, 255)`) ;
3. chiffre cette clé symétrique avec la clé publique du serveur, puis simule son envoi (elle est stockée dans une variable, comme si elle transitait sur le réseau) ;
4. côté « serveur », déchiffre la clé symétrique reçue avec sa clé privée ;
5. vérifie que la clé symétrique obtenue côté serveur est identique à celle choisie côté client ;
6. utilise ensuite cette clé symétrique pour chiffrer et déchiffrer un message avec `chiffrer_xor`/`dechiffrer_xor`.

**C.3.** Expliquer, en reliant votre script au cours, pourquoi cette combinaison illustre le principe utilisé pour sécuriser une connexion HTTPS.

---

## Corrigé indicatif

```python
import random

def simuler_tourniquet(processus, tranche):
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


def temps_de_completion(processus, tranche):
    trace = simuler_tourniquet(processus, tranche)
    completions = {}
    temps_ecoule = 0
    for nom, duree in trace:
        temps_ecoule += duree
        completions[nom] = temps_ecoule   # la dernière tranche d'un processus fixe son temps de complétion
    return completions

print(temps_de_completion([("A", 10), ("B", 1), ("C", 1)], 1))
print(temps_de_completion([("A", 10), ("B", 1), ("C", 1)], 10))


def generer_cles(p, q, e):
    n = p * q
    indicatrice = (p - 1) * (q - 1)
    d = pow(e, -1, indicatrice)
    return (e, n), (d, n)

def chiffrer_asymetrique(valeurs, cle_publique):
    e, n = cle_publique
    return [pow(v, e, n) for v in valeurs]

def dechiffrer_asymetrique(chiffre, cle_privee):
    d, n = cle_privee
    return [pow(c, d, n) for c in chiffre]

def chiffrer_xor(message, cle):
    return bytes(c ^ cle[i % len(cle)] for i, c in enumerate(message.encode()))

def dechiffrer_xor(chiffre, cle):
    return bytes(c ^ cle[i % len(cle)] for i, c in enumerate(chiffre)).decode()


# --- Simulation de l'échange ---
cle_publique_serveur, cle_privee_serveur = generer_cles(61, 53, 17)

# 1. Le client choisit une clé symétrique aléatoire (valeurs < n pour rester dans le domaine de chiffrement)
cle_symetrique_client = [random.randint(0, 200) for _ in range(3)]

# 2. Le client chiffre cette clé avec la clé publique du serveur
cle_chiffree = chiffrer_asymetrique(cle_symetrique_client, cle_publique_serveur)

# 3. Le serveur déchiffre avec sa clé privée
cle_symetrique_serveur = dechiffrer_asymetrique(cle_chiffree, cle_privee_serveur)

assert cle_symetrique_client == cle_symetrique_serveur
print("Clé symétrique bien transmise :", cle_symetrique_serveur)

# 4. Utilisation de la clé symétrique pour la suite de la communication
cle_octets = bytes(cle_symetrique_serveur)
message_chiffre = chiffrer_xor("Bonjour serveur", cle_octets)
message_recu = dechiffrer_xor(message_chiffre, cle_octets)
print(message_recu)
```

**C.3.** Comme lors de la négociation HTTPS, la partie **asymétrique** n'est utilisée qu'une seule fois, pour transmettre en toute confidentialité une **petite** quantité d'information (ici, une clé de quelques octets) ; le reste de la communication (le message, potentiellement volumineux) est ensuite chiffré avec la clé **symétrique**, plus rapide à utiliser. Cela illustre concrètement pourquoi les deux types de chiffrement sont combinés plutôt qu'utilisés isolément.
