# Chapitre 6 — Réseaux : transmission de données
## Évaluation

*Première NSI — Durée : 50 min — Barème sur 20 points*

---

### Partie 1 — Questions de cours (9 points)

**Question 1 (2 pts).** Pourquoi découpe-t-on un message en paquets avant de le transmettre sur un réseau, plutôt que de l'envoyer en une seule fois ?

**Question 2 (2 pts).** Qu'appelle-t-on « encapsulation » ? Citer deux informations que peut contenir l'en-tête d'un paquet.

**Question 3 (3 pts).** Décrire le principe du protocole du bit alterné. À quoi sert précisément le bit de séquence ?

**Question 4 (2 pts).** Dans le modèle en couches TCP/IP, quelle couche est responsable de l'adressage et de l'acheminement des paquets à travers le réseau ? Citer le protocole associé.

---

### Partie 2 — Manipulations (6 points)

**Question 5 (2 pts).** Découper la chaîne `"BONJOURATOUS"` en paquets de taille maximale `5`, en utilisant le principe de `decouper_en_paquets` du cours. Donner le résultat.

**Question 6 (4 pts).** On donne les données `[100, 150, 90]`. Calculer leur somme de contrôle (checksum), définie comme la somme des valeurs modulo 256. Un paquet est reçu avec les données `[100, 149, 91]` et le checksum transmis est celui calculé précédemment. Ce paquet serait-il détecté comme corrompu par une vérification de checksum ? Justifier.

---

### Partie 3 — Écrire du code (5 points)

**Question 7 (5 pts).** On donne une liste de trames sous la forme de tuples `(entete, paquet)`, où `entete` est un dictionnaire contenant au moins la clé `"num"` (numéro de séquence). Écrire une fonction `numero_manquant(trames, nombre_total_attendu)` qui renvoie la liste des numéros de séquence **absents** parmi les trames reçues, sachant que les paquets attendus sont numérotés de `0` à `nombre_total_attendu - 1` (indication : construire l'ensemble des numéros présents avec une compréhension, puis comparer avec l'ensemble des numéros attendus).

---

## Corrigé et barème détaillé

### Partie 1 (9 pts)

**Q1 (2 pts)** — Le découpage en paquets permet de partager les liaisons réseau entre plusieurs communications (1 pt), et de limiter l'impact d'une perte de données : seul le paquet perdu doit être retransmis, pas le message entier (1 pt).

**Q2 (2 pts)** — L'encapsulation consiste à ajouter à une donnée un en-tête contenant les informations nécessaires à son acheminement et à son traitement (1 pt). Exemples d'informations dans l'en-tête : adresse de destination, numéro de séquence, taille, somme de contrôle (1 pt pour deux exemples corrects).

**Q3 (3 pts)** — L'émetteur envoie un paquet accompagné d'un bit de séquence, et attend un accusé de réception avant d'envoyer le paquet suivant ; en l'absence d'accusé de réception, il retransmet le même paquet (2 pts). Le bit de séquence permet au destinataire de distinguer un nouveau paquet d'une retransmission d'un paquet déjà reçu — utile notamment lorsque l'accusé de réception, et non le paquet, a été perdu (1 pt).

**Q4 (2 pts)** — La couche **Internet (réseau)** est responsable de l'adressage et de l'acheminement des paquets (1 pt). Le protocole associé est **IP** (1 pt).

### Partie 2 (6 pts)

**Q5 (2 pts)** — `decouper_en_paquets("BONJOURATOUS", 5)` renvoie `["BONJO", "URATO", "US"]`.

**Q6 (4 pts)** — Checksum des données `[100, 150, 90]` : `(100+150+90) % 256 = 340 % 256 = 84` (2 pts). Pour les données reçues `[100, 149, 91]`, la somme est `100+149+91 = 340`, soit un checksum de `340 % 256 = 84`, **identique** au checksum transmis (2 pts) : l'erreur ne serait **pas détectée**, car les deux erreurs (−1 sur la deuxième valeur, +1 sur la troisième) se compensent exactement dans la somme totale — ceci illustre une limite connue de cette méthode de détection très simple.

### Partie 3 (5 pts)

**Q7 (5 pts)**
```python
def numero_manquant(trames, nombre_total_attendu):
    numeros_presents = {entete["num"] for entete, paquet in trames}
    numeros_attendus = set(range(nombre_total_attendu))
    return sorted(numeros_attendus - numeros_presents)
```
*(2 pts pour la construction correcte de l'ensemble des numéros présents, 2 pts pour la comparaison avec l'ensemble attendu, 1 pt pour un résultat trié et correctement formé.)*

---

**Barème global : 9 + 6 + 5 = 20 points.**
