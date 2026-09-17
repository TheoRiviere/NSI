# Chapitre 6 — Réseaux : transmission de données
## TP sur machine — Simuler une transmission fiable avec détection d'erreur

*Première NSI — Python 3 — Durée indicative : 1h30 à 2h*

---

## Objectifs

- Combiner découpage en paquets, checksum et détection d'erreur dans un scénario complet.
- Simuler des erreurs de transmission et observer leur détection.
- Simuler une demande de retransmission des paquets corrompus.

---

## Partie A — Encapsulation avec somme de contrôle

**A.1.** Recopier `decouper_en_paquets`, `encapsuler`, `reassembler` du cours.

**A.2.** Écrire une fonction `calculer_checksum(donnees)` qui calcule la somme de contrôle d'une chaîne de caractères, en sommant le code Unicode (`ord`) de chacun de ses caractères, modulo 256.

**A.3.** Écrire une fonction `encapsuler_avec_checksum(paquets, destinataire)`, semblable à `encapsuler` du cours, mais dont l'en-tête de chaque trame contient en plus une clé `"checksum"`, calculée avec la fonction précédente sur le paquet correspondant.

**A.4.** Tester sur le message `"TRANSMISSION DE DONNEES SUR LE RESEAU"`, découpé en paquets de taille 6.

---

## Partie B — Simuler des erreurs de transmission

**B.1.** Écrire une fonction `simuler_transmission_avec_erreurs(trames, taux_erreur)` qui, pour chaque trame, tire un nombre aléatoire pour décider si une erreur se produit (avec la probabilité `taux_erreur`) ; en cas d'erreur, on modifie **un caractère au hasard** du paquet (par exemple en changeant son code Unicode de 1), simulant ainsi une corruption de donnée pendant le transport. La fonction renvoie la liste des trames reçues (avec, éventuellement, des paquets corrompus).

**B.2.** Écrire une fonction `detecter_paquets_corrompus(trames_recues)` qui renvoie la liste des numéros de séquence des paquets dont le checksum recalculé à la réception ne correspond pas au checksum transmis dans l'en-tête.

**B.3.** Tester avec `taux_erreur=0.0` : vérifier qu'aucun paquet n'est détecté comme corrompu, et que le message reconstitué (avec `reassembler`) est identique au message d'origine.

**B.4.** Tester avec `taux_erreur=0.5` : afficher la liste des paquets détectés comme corrompus. Ce nombre est-il le même à chaque exécution ? Pourquoi ?

---

## Partie C — Demander une retransmission

Dans un vrai protocole réseau, lorsqu'un paquet corrompu est détecté, le destinataire demande à l'émetteur de le **retransmettre** (au lieu de simplement le rejeter), afin de pouvoir reconstituer le message complet et correct.

**C.1.** Écrire une fonction `demander_retransmission(trames_originales, numeros_corrompus)` qui renvoie un dictionnaire associant, pour chaque numéro de paquet corrompu, la trame **originale** (non corrompue) correspondante — on suppose ici que l'émetteur a conservé une copie de toutes les trames originales, ce qui est réaliste en pratique.

**C.2.** En utilisant ce dictionnaire, reconstruire la liste des trames reçues en **remplaçant** chaque trame détectée comme corrompue par sa version originale (simulant ainsi la réception réussie de la retransmission).

**C.3.** Vérifier qu'après cette correction, `detecter_paquets_corrompus` ne détecte plus aucune erreur, et que `reassembler` redonne exactement le message d'origine.

---

## Corrigé indicatif

```python
import random

# --- Partie A ---
def decouper_en_paquets(message, taille_max):
    paquets = []
    for i in range(0, len(message), taille_max):
        paquets.append(message[i:i + taille_max])
    return paquets

def reassembler(trames):
    trames_triees = sorted(trames, key=lambda t: t[0]["num"])
    return "".join(paquet for entete, paquet in trames_triees)

def calculer_checksum(donnees):
    return sum(ord(c) for c in donnees) % 256

def encapsuler_avec_checksum(paquets, destinataire):
    trames = []
    for i, paquet in enumerate(paquets):
        entete = {
            "num": i,
            "total": len(paquets),
            "dest": destinataire,
            "checksum": calculer_checksum(paquet),
        }
        trames.append((entete, paquet))
    return trames

message = "TRANSMISSION DE DONNEES SUR LE RESEAU"
paquets = decouper_en_paquets(message, 6)
trames = encapsuler_avec_checksum(paquets, "192.168.0.5")


# --- Partie B ---
def simuler_transmission_avec_erreurs(trames, taux_erreur):
    trames_recues = []
    for entete, paquet in trames:
        if random.random() < taux_erreur and len(paquet) > 0:
            indice = random.randint(0, len(paquet) - 1)
            paquet_corrompu = (
                paquet[:indice]
                + chr((ord(paquet[indice]) + 1) % 256)
                + paquet[indice + 1:]
            )
            trames_recues.append((entete, paquet_corrompu))
        else:
            trames_recues.append((entete, paquet))
    return trames_recues

def detecter_paquets_corrompus(trames_recues):
    corrompus = []
    for entete, paquet in trames_recues:
        if calculer_checksum(paquet) != entete["checksum"]:
            corrompus.append(entete["num"])
    return corrompus

recues_sans_erreur = simuler_transmission_avec_erreurs(trames, 0.0)
assert detecter_paquets_corrompus(recues_sans_erreur) == []
assert reassembler(recues_sans_erreur) == message
print("Sans erreur : message correctement reconstitué.")

recues_avec_erreurs = simuler_transmission_avec_erreurs(trames, 0.5)
corrompus = detecter_paquets_corrompus(recues_avec_erreurs)
print("Paquets détectés comme corrompus :", corrompus)


# --- Partie C ---
def demander_retransmission(trames_originales, numeros_corrompus):
    return {
        entete["num"]: (entete, paquet)
        for entete, paquet in trames_originales
        if entete["num"] in numeros_corrompus
    }

corrections = demander_retransmission(trames, corrompus)
recues_corrigees = list(recues_avec_erreurs)
for i, (entete, paquet) in enumerate(recues_corrigees):
    if entete["num"] in corrections:
        recues_corrigees[i] = corrections[entete["num"]]

assert detecter_paquets_corrompus(recues_corrigees) == []
assert reassembler(recues_corrigees) == message
print("Après retransmission : message correctement reconstitué :", reassembler(recues_corrigees))
```

**Réponse B.4 :** le nombre de paquets corrompus détectés varie à chaque exécution car il dépend d'un tirage aléatoire indépendant pour chaque paquet (`random.random() < taux_erreur`) : avec un taux de 50 %, chaque paquet a environ une chance sur deux d'être corrompu, mais le résultat précis dépend du hasard à chaque exécution.
