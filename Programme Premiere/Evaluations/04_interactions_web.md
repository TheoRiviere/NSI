# Chapitre 4 — Interactions Homme-Machine sur le Web
## Évaluation

*Première NSI — Durée : 50 min — Barème sur 20 points*

---

### Partie 1 — Questions de cours (8 points)

**Question 1 (2 pts).** Qu'est-ce que le DOM ? Quel est son rôle ?

**Question 2 (2 pts).** Expliquer ce qu'est un gestionnaire d'événement (*event listener*) en JavaScript, et donner sa syntaxe générale avec `addEventListener`.

**Question 3 (2 pts).** Où sont transmises les données d'une requête GET ? Où sont transmises celles d'une requête POST ?

**Question 4 (2 pts).** Pourquoi un formulaire de connexion (identifiant + mot de passe) doit-il impérativement utiliser la méthode POST plutôt que GET ?

---

### Partie 2 — HTML et JavaScript (7 points)

**Question 5 (3 pts).** Écrire le code HTML d'un formulaire simple avec un champ de texte d'identifiant `"pseudo"` (attribut `name="pseudo"`), un bouton de soumission, l'attribut `action="/inscription"`, et la méthode `POST`.

**Question 6 (4 pts).** Écrire le code JavaScript qui, lorsqu'on clique sur un bouton d'identifiant `"btn-favoris"`, ajoute la classe CSS `"actif"` à cet élément s'il ne l'a pas déjà, et la retire s'il l'a déjà (indication : l'objet `classList` d'un élément possède une méthode `toggle(nom_classe)` qui fait exactement cela — vous pouvez soit l'utiliser directement, soit réécrire cette logique avec `contains`, `add` et `remove`).

---

### Partie 3 — Écrire du code Python (5 points)

**Question 7 (5 pts).** On dispose d'un dictionnaire représentant les paramètres reçus dans l'URL d'une requête GET, par exemple :
```python
params = {"recherche": ["ordinateur"], "page": ["3"]}
```
(chaque valeur est une liste, comme le renvoie `urllib.parse.parse_qs`). Écrire une fonction `page_demandee(params)` qui renvoie le numéro de page demandé sous forme d'entier (clé `"page"`), avec une valeur par défaut de `1` si cette clé est absente du dictionnaire.

---

## Corrigé et barème détaillé

### Partie 1 (8 pts)

**Q1 (2 pts)** — Le DOM (Document Object Model) est la représentation en mémoire, sous forme d'arbre d'objets, du document HTML affiché par le navigateur (1 pt). Son rôle est de permettre à du code JavaScript de lire et de modifier dynamiquement le contenu et la structure de la page (1 pt).

**Q2 (2 pts)** — Un gestionnaire d'événement est une fonction associée à un événement (clic, saisie...) sur un élément, exécutée automatiquement par le navigateur lorsque cet événement se produit (1 pt). Syntaxe : `element.addEventListener("nom_evenement", fonction)` (1 pt).

**Q3 (2 pts)** — En GET, les données sont transmises **dans l'URL**, après le `?` (1 pt). En POST, elles sont transmises **dans le corps** de la requête, et ne sont pas visibles dans l'URL (1 pt).

**Q4 (2 pts)** — Avec GET, le mot de passe apparaîtrait en clair dans l'URL, donc dans l'historique du navigateur, dans les journaux (logs) du serveur, et pourrait être visible par-dessus l'épaule de l'utilisateur ou partagé accidentellement (1 pt). POST transmet les données dans le corps de la requête, ce qui évite cette exposition directe (1 pt).

### Partie 2 (7 pts)

**Q5 (3 pts)**
```html
<form action="/inscription" method="POST">
  <input type="text" id="pseudo" name="pseudo">
  <button type="submit">Envoyer</button>
</form>
```
*(1 pt pour `action`/`method` corrects, 1 pt pour le champ avec `name`, 1 pt pour le bouton de soumission.)*

**Q6 (4 pts)**
```javascript
const bouton = document.getElementById("btn-favoris");
bouton.addEventListener("click", function() {
    bouton.classList.toggle("actif");
});
```
Version équivalente sans `toggle` :
```javascript
bouton.addEventListener("click", function() {
    if (bouton.classList.contains("actif")) {
        bouton.classList.remove("actif");
    } else {
        bouton.classList.add("actif");
    }
});
```
*(2 pts pour l'ajout correct du gestionnaire d'événement, 2 pts pour la bascule correcte de la classe.)*

### Partie 3 (5 pts)

**Q7 (5 pts)**
```python
def page_demandee(params):
    if "page" in params:
        return int(params["page"][0])
    else:
        return 1
```
ou, de façon équivalente avec `.get` :
```python
def page_demandee(params):
    return int(params.get("page", ["1"])[0])
```
*(3 pts pour la gestion correcte de la valeur par défaut, 2 pts pour la conversion en entier et l'extraction correcte de la valeur dans la liste.)*

---

**Barème global : 8 + 7 + 5 = 20 points.**
