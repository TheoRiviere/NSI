# Chapitre 5 — Graphes
## TP sur machine — Itinéraires dans un réseau de villes

*Terminale NSI — Python 3 — Durée indicative : 1h30 à 2h*

---

## Objectifs

- Représenter un réseau routier par un graphe.
- Mettre en œuvre les parcours en profondeur et en largeur.
- Calculer un plus court chemin (en nombre d'étapes) entre deux villes.

## Mise en situation

On modélise un petit réseau de villes reliées par des routes directes (graphe non orienté).

```python
reseau = {
    "Paris": ["Lille", "Rouen", "Orleans"],
    "Lille": ["Paris"],
    "Rouen": ["Paris", "Caen"],
    "Caen": ["Rouen", "Rennes"],
    "Rennes": ["Caen", "Nantes"],
    "Nantes": ["Rennes", "Orleans"],
    "Orleans": ["Paris", "Nantes", "Limoges"],
    "Limoges": ["Orleans"],
}
```

---

## Partie A — Prise en main

**A.1.** Recopier le dictionnaire `reseau` et vérifier qu'il est cohérent (si `"Lille"` apparaît dans la liste de `"Paris"`, alors `"Paris"` doit apparaître dans la liste de `"Lille"`, puisque le graphe est non orienté).

**A.2.** Écrire une fonction `nombre_villes(reseau)` et une fonction `nombre_routes(reseau)` (attention à ne pas compter deux fois chaque route, puisqu'elle apparaît dans les deux listes).

**A.3.** Reprendre les fonctions `parcours_profondeur` et `parcours_largeur` du cours et les tester depuis `"Paris"`.

---

## Partie B — Existence et calcul d'un itinéraire

**B.1.** Écrire une fonction `relie(reseau, ville1, ville2)` qui renvoie `True` si l'on peut aller de `ville1` à `ville2` en empruntant une suite de routes (on pourra utiliser `parcours_profondeur` ou `parcours_largeur`).

**B.2.** Reprendre `plus_court_chemin` du cours et calculer le plus court itinéraire (en nombre d'étapes) entre `"Lille"` et `"Limoges"`.

**B.3.** Écrire une fonction `nombre_etapes(reseau, ville1, ville2)` qui renvoie le nombre de routes empruntées sur le plus court chemin entre deux villes (la longueur de la liste renvoyée par `plus_court_chemin`, moins 1).

---

## Partie C — Une nouvelle ville isolée

**C.1.** Ajouter au réseau une ville `"IleDOleron"` reliée à aucune autre ville (`reseau["IleDOleron"] = []`). Que renvoie `relie(reseau, "Paris", "IleDOleron")` ?

**C.2. (bonus)** En vous inspirant de l'exercice sur les composantes connexes, écrire une fonction qui renvoie la liste des villes injoignables depuis `"Paris"`.

---

## Corrigé indicatif

```python
reseau = {
    "Paris": ["Lille", "Rouen", "Orleans"],
    "Lille": ["Paris"],
    "Rouen": ["Paris", "Caen"],
    "Caen": ["Rouen", "Rennes"],
    "Rennes": ["Caen", "Nantes"],
    "Nantes": ["Rennes", "Orleans"],
    "Orleans": ["Paris", "Nantes", "Limoges"],
    "Limoges": ["Orleans"],
}

def nombre_villes(reseau):
    return len(reseau)

def nombre_routes(reseau):
    total = sum(len(voisins) for voisins in reseau.values())
    return total // 2   # chaque route est comptée deux fois (une fois par extrémité)


def parcours_profondeur(graphe, depart):
    visites = []
    def explorer(sommet):
        if sommet not in visites:
            visites.append(sommet)
            for voisin in graphe[sommet]:
                explorer(voisin)
    explorer(depart)
    return visites


def parcours_largeur(graphe, depart):
    visites = [depart]
    file = [depart]
    while len(file) > 0:
        sommet = file.pop(0)
        for voisin in graphe[sommet]:
            if voisin not in visites:
                visites.append(voisin)
                file.append(voisin)
    return visites


def relie(reseau, ville1, ville2):
    return ville2 in parcours_profondeur(reseau, ville1)


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


def nombre_etapes(reseau, ville1, ville2):
    chemin = plus_court_chemin(reseau, ville1, ville2)
    return len(chemin) - 1
```

Résultat attendu pour `plus_court_chemin(reseau, "Lille", "Limoges")` : `["Lille", "Paris", "Orleans", "Limoges"]`, soit 3 étapes.
