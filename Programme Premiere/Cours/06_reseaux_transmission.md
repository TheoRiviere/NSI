# Chapitre 6 — Réseaux : transmission de données

## Objectifs

- Comprendre le découpage d'un message en paquets et le principe d'encapsulation.
- Comprendre l'intérêt d'une somme de contrôle pour détecter une erreur de transmission.
- Comprendre le principe du protocole du bit alterné.
- Situer le modèle en couches TCP/IP.

## Prérequis

- Représentation binaire — chapitre 1.
- Listes et dictionnaires — chapitre 2.

---

## 1. Pourquoi découper un message en paquets ?

Lorsqu'un ordinateur souhaite transmettre un message volumineux (un fichier, une vidéo...) à un autre ordinateur via Internet, il ne l'envoie pas en une seule fois. Le message est découpé en **paquets** de taille limitée, qui sont envoyés indépendamment les uns des autres, et peuvent même emprunter des chemins différents à travers le réseau avant d'être réassemblés à l'arrivée.

Cette approche présente plusieurs avantages : elle permet à plusieurs communications de **partager** les mêmes liaisons réseau (les paquets de différentes communications peuvent s'entrelacer), elle limite l'impact de la perte d'une portion de données (seul le paquet concerné doit être retransmis, pas tout le message), et elle permet d'acheminer les paquets par des chemins différents selon l'état du réseau.

```python
def decouper_en_paquets(message, taille_max):
    """Découpe une chaîne en une liste de paquets de taille au plus taille_max."""
    paquets = []
    for i in range(0, len(message), taille_max):
        paquets.append(message[i:i + taille_max])
    return paquets
```

---

## 2. Encapsulation

Chaque paquet transmis sur le réseau est accompagné d'un **en-tête** (*header*), qui contient les informations nécessaires à son acheminement et à son traitement par le destinataire : adresse de destination, numéro de séquence (position du paquet dans le message d'origine), taille, informations de contrôle d'erreur... On appelle ce processus l'**encapsulation** : la donnée « utile » (la charge utile, ou *payload*) est enveloppée dans un en-tête qui décrit comment la traiter.

```python
def encapsuler(paquets, destinataire):
    """Ajoute un en-tête à chaque paquet."""
    trames = []
    for i, paquet in enumerate(paquets):
        entete = {"num": i, "total": len(paquets), "dest": destinataire}
        trames.append((entete, paquet))
    return trames
```

### 2.1 Réassemblage

Comme les paquets peuvent arriver **dans le désordre** (ils peuvent suivre des chemins différents et de longueurs différentes à travers le réseau), le numéro de séquence inclus dans l'en-tête est essentiel : il permet au destinataire de remettre les paquets dans le bon ordre avant de reconstituer le message d'origine.

```python
def reassembler(trames):
    """Reconstitue le message d'origine à partir de trames éventuellement désordonnées."""
    trames_triees = sorted(trames, key=lambda t: t[0]["num"])
    return "".join(paquet for entete, paquet in trames_triees)
```

---

## 3. Détecter une erreur de transmission : la somme de contrôle

Une transmission sur un support physique (câble, fibre, ondes radio) n'est jamais parfaitement fiable : des perturbations peuvent altérer un ou plusieurs bits en cours de route. Pour détecter (et non corriger) ce type d'erreur, on associe souvent aux données une **somme de contrôle** (*checksum*) : une valeur calculée à partir des données, transmise en même temps qu'elles, et que le destinataire recalcule pour vérifier qu'elle correspond bien à ce qu'il a reçu.

```python
def calculer_checksum(donnees):
    """Calcule une somme de contrôle très simple (somme modulo 256)."""
    return sum(donnees) % 256

def verifier_checksum(donnees, checksum_recu):
    return calculer_checksum(donnees) == checksum_recu
```

Si les données reçues sont différentes des données envoyées (même sur un seul octet), le checksum recalculé a de bonnes chances de différer du checksum transmis, ce qui permet de détecter l'erreur (cette méthode très simple n'est cependant pas infaillible : certaines altérations particulières peuvent, par un hasard malheureux, laisser le checksum inchangé — des méthodes plus robustes, hors programme, existent en pratique).

---

## 4. Le protocole du bit alterné

### 4.1 Le problème

Comment être sûr qu'un paquet envoyé a bien été reçu par le destinataire ? Et comment gérer le cas où un paquet serait perdu en cours de route, ou reçu en double ?

### 4.2 Principe

Le **protocole du bit alterné** (*alternating bit protocol*) est un mécanisme simple pour transmettre des données de façon fiable, un paquet à la fois :

1. L'émetteur envoie un paquet, accompagné d'un **bit de séquence** (0 ou 1).
2. Il attend un **accusé de réception** (acquittement, ou *ACK*) du destinataire, confirmant que ce paquet précis (identifié par son bit) a bien été reçu.
3. Si l'accusé de réception n'arrive pas (paquet perdu, ou accusé lui-même perdu) dans un certain délai, l'émetteur **retransmet** le même paquet, avec le même bit.
4. Une fois l'accusé de réception obtenu, l'émetteur passe au paquet suivant, en **inversant** le bit de séquence (0 devient 1, et inversement).

Ce bit alterné permet au destinataire de distinguer un nouveau paquet d'une simple retransmission d'un paquet déjà reçu (si l'accusé de réception lui-même a été perdu, l'émetteur renverrait sinon le même paquet, que le destinataire risquerait de traiter deux fois).

```python
import random

def simuler_bit_alterne(paquets, taux_perte=0.0):
    """Simule l'envoi de paquets avec le protocole du bit alterné.
    taux_perte : probabilité qu'un envoi échoue et doive être retransmis."""
    bit_emetteur = 0
    paquets_recus = []
    nb_retransmissions = 0
    for paquet in paquets:
        accuse_recu = False
        while not accuse_recu:
            perdu = random.random() < taux_perte
            if not perdu:
                paquets_recus.append(paquet)
                accuse_recu = True
            else:
                nb_retransmissions += 1
        bit_emetteur = 1 - bit_emetteur   # on passe au bit suivant
    return paquets_recus, nb_retransmissions
```

**Remarque sur l'efficacité :** ce protocole garantit la fiabilité, mais il est lent, car il attend l'accusé de réception d'un paquet avant d'envoyer le suivant (un seul paquet « en vol » à la fois). Des protocoles plus élaborés (hors programme, comme les *fenêtres glissantes* utilisées par TCP) permettent d'envoyer plusieurs paquets sans attendre chaque accusé individuellement, pour de meilleures performances.

---

## 5. Le modèle en couches TCP/IP

La transmission d'une donnée sur Internet repose sur plusieurs protocoles, organisés en **couches**, chacune ayant un rôle précis et s'appuyant sur les couches inférieures :

| Couche | Rôle | Exemple de protocole |
|---|---|---|
| Application | Format des données échangées par les applications | HTTP, HTTPS |
| Transport | Fiabilité de bout en bout, découpage en segments | TCP (fiable, avec accusés de réception), UDP (rapide, non fiable) |
| Internet (réseau) | Adressage et acheminement des paquets à travers le réseau | IP |
| Accès réseau (liaison) | Transmission physique sur un support donné | Ethernet, Wi-Fi |

Chaque couche encapsule les données de la couche supérieure en y ajoutant son propre en-tête (un principe d'encapsulation semblable à celui vu à la section 2, mais appliqué successivement à plusieurs niveaux) : une donnée HTTP est encapsulée dans un segment TCP, lui-même encapsulé dans un paquet IP, lui-même encapsulé dans une trame Ethernet, avant d'être effectivement transmise sur le support physique.

---

## Synthèse

| Notion | Point clé à retenir |
|---|---|
| Paquet | Fragment de taille limitée d'un message découpé |
| Encapsulation | Ajout d'un en-tête (destination, numéro de séquence...) à une donnée |
| Réassemblage | Remise en ordre des paquets grâce au numéro de séquence |
| Checksum | Valeur de contrôle permettant de détecter (pas corriger) une erreur |
| Protocole du bit alterné | Fiabilise l'envoi paquet par paquet, via accusé de réception + bit de séquence |
| Modèle TCP/IP | Organisation en couches (application, transport, internet, accès réseau) |

*Prochaine étape suggérée : Chapitre 7 — Systèmes d'exploitation et périphériques.*
