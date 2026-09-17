# Chapitre 6 — Réseaux : transmission de données
## Fiche d'exercices

*Première NSI — Python 3*

---

### Exercice 1 — Découpage en paquets

1. En utilisant `decouper_en_paquets` du cours, découper la chaîne `"INFORMATIQUE"` en paquets de taille maximale `4`. Combien de paquets obtient-on ?
2. Que se passerait-il si la longueur du message n'était pas un multiple exact de la taille maximale (par exemple, découper `"INFORMATIQUE"` — 12 caractères — en paquets de taille `5`) ? Vérifier avec Python.

### Exercice 2 — Encapsulation et réassemblage

1. Découper `"INFORMATIQUE"` en paquets de taille 4, puis les encapsuler avec `encapsuler` du cours, avec pour destinataire `"10.0.0.1"`.
2. Mélanger aléatoirement l'ordre des trames obtenues (`random.shuffle`).
3. Vérifier qu'en utilisant `reassembler` du cours sur les trames mélangées, on retrouve bien le message d'origine. Expliquer pourquoi cela fonctionne malgré le mélange.

### Exercice 3 — Somme de contrôle

1. Calculer le checksum (avec `calculer_checksum` du cours) des données `[50, 60, 70]`.
2. Simuler une erreur de transmission en modifiant une des valeurs de la liste (par exemple, remplacer `60` par `61`), et vérifier avec `verifier_checksum` que l'erreur est bien détectée.
3. Trouver (à la main ou en testant plusieurs possibilités) deux listes de données **différentes** mais qui ont **le même checksum** avec cette méthode très simple (indication : le checksum est une somme modulo 256 — deux listes différentes qui ont la même somme totale auront le même checksum, même si leurs valeurs individuelles diffèrent). Que cela révèle-t-il sur les limites de cette méthode de détection d'erreur ?

### Exercice 4 — Protocole du bit alterné

1. En utilisant `simuler_bit_alterne` du cours avec `taux_perte=0.0`, vérifier que le nombre de retransmissions est bien `0`.
2. Avec `taux_perte=0.3` (30% de chance qu'un envoi échoue), exécuter plusieurs fois la simulation sur une liste de 5 paquets et observer que le nombre de retransmissions varie d'une exécution à l'autre. Pourquoi ce nombre n'est-il pas toujours le même ?
3. Sans utiliser `random`, expliquer avec vos propres mots à quoi sert le **bit de séquence** (0 ou 1) dans ce protocole : que se passerait-il si l'émetteur n'utilisait pas de bit de séquence et que l'accusé de réception d'un paquet était perdu (mais pas le paquet lui-même, déjà bien reçu par le destinataire) ?

---

## Corrigés

### Exercice 1

1. `decouper_en_paquets("INFORMATIQUE", 4)` renvoie `["INFO", "RMAT", "IQUE"]` : **3 paquets**.
2. `decouper_en_paquets("INFORMATIQUE", 5)` renvoie `["INFOR", "MATIQ", "UE"]` : le dernier paquet est simplement plus court que les autres (le découpage par tranches, `message[i:i+taille_max]`, s'arrête naturellement à la fin de la chaîne sans provoquer d'erreur).

### Exercice 2

1-2-3.
```python
import random

paquets = decouper_en_paquets("INFORMATIQUE", 4)
trames = encapsuler(paquets, "10.0.0.1")
random.shuffle(trames)
message_reconstitue = reassembler(trames)
assert message_reconstitue == "INFORMATIQUE"
```
Cela fonctionne car chaque trame transporte, dans son en-tête, un **numéro de séquence** (`num`) indiquant sa position d'origine dans le message. La fonction `reassembler` commence par **trier** les trames selon ce numéro avant de les concaténer : l'ordre dans lequel les trames sont arrivées (ou ont été mélangées) n'a donc aucune importance, seul le numéro de séquence compte pour la reconstruction.

### Exercice 3

1. `calculer_checksum([50, 60, 70])` = `(50+60+70) % 256` = `180 % 256` = `180`.
2. `verifier_checksum([50, 61, 70], 180)` renvoie `False` : `50+61+70 = 181 ≠ 180`, l'erreur est détectée.
3. Par exemple, `[50, 60, 70]` (somme 180) et `[51, 59, 70]` (somme également 180) ont le **même checksum**, alors que ce sont des données différentes. Cela montre que cette méthode de checksum très simple (une simple somme) ne détecte **pas toutes** les erreurs possibles : deux erreurs qui se « compensent » (une valeur qui augmente pendant qu'une autre diminue de la même quantité) peuvent passer inaperçues. C'est pourquoi des méthodes plus robustes (hors programme) sont utilisées en pratique.

### Exercice 4

1. Avec `taux_perte=0.0`, aucun envoi n'échoue jamais (`random.random() < 0.0` est toujours faux), donc `nb_retransmissions` vaut bien `0`.
2. Le nombre de retransmissions varie car il dépend d'un tirage **aléatoire** à chaque tentative d'envoi (`random.random() < taux_perte`) : le hasard peut faire qu'un paquet donné échoue 0, 1, 2 fois ou plus avant de réussir, et ce nombre total varie donc d'une exécution à l'autre.
3. Sans bit de séquence, si l'émetteur envoie un paquet, que le destinataire le reçoit bien et envoie un accusé de réception, mais que cet accusé de réception est **perdu** en chemin, l'émetteur (n'ayant reçu aucune confirmation) va **retransmettre** le même paquet, pensant qu'il a été perdu. Sans bit de séquence, le destinataire n'aurait aucun moyen de savoir si ce paquet reçu à nouveau est un **nouveau** paquet ou bien la **même donnée déjà reçue** une première fois : il risquerait de traiter deux fois la même donnée (par exemple, l'afficher deux fois, ou l'ajouter deux fois à un fichier). Le bit alterné permet au destinataire de reconnaître qu'il s'agit d'une retransmission du paquet précédent (même bit que la dernière fois) et de l'ignorer, tout en renvoyant quand même un accusé de réception (au cas où celui-ci aurait de nouveau été perdu).
