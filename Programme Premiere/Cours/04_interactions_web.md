# Chapitre 4 — Interactions Homme-Machine sur le Web

## Objectifs

- Identifier les composants graphiques d'une page Web (structure HTML).
- Comprendre le mécanisme des événements et leur traitement en JavaScript.
- Distinguer les méthodes HTTP GET et POST et savoir quand utiliser chacune.
- Comprendre le fonctionnement d'un formulaire HTML et son interaction avec un serveur.

## Prérequis

- Aucun prérequis de programmation Web spécifique ; connaissances Python de base pour la partie serveur.

---

## 1. Structure d'une page Web (HTML)

Une page Web est décrite par un document **HTML** (HyperText Markup Language), qui définit sa structure à l'aide de **balises**. Chaque balise délimite un élément (un titre, un paragraphe, une image, un bouton...).

```html
<!DOCTYPE html>
<html>
  <head>
    <title>Ma page</title>
  </head>
  <body>
    <h1>Bienvenue</h1>
    <p>Ceci est un paragraphe.</p>
    <button id="mon-bouton">Cliquez ici</button>
  </body>
</html>
```

Quelques balises et attributs essentiels : `<h1>` à `<h6>` (titres, du plus important au moins important), `<p>` (paragraphe), `<a href="...">` (lien), `<img src="...">` (image), `<button>` (bouton), `<input>` (champ de saisie), `<div>` (bloc générique). L'attribut `id` permet de donner un identifiant unique à un élément, pour pouvoir le retrouver facilement depuis du code JavaScript.

Le navigateur construit, à partir du HTML, une représentation en mémoire appelée **DOM** (Document Object Model) : un arbre d'objets correspondant à chaque élément de la page, que l'on peut manipuler dynamiquement avec JavaScript.

---

## 2. Les événements

### 2.1 Principe

Une page Web interactive doit réagir aux actions de l'utilisateur (clic de souris, saisie au clavier, chargement de la page...). Ces actions génèrent des **événements**, auxquels on peut associer une fonction à exécuter : un **gestionnaire d'événement** (*event handler*, ou *event listener*).

```javascript
const bouton = document.getElementById("mon-bouton");

bouton.addEventListener("click", function() {
    alert("Vous avez cliqué !");
});
```

La méthode `addEventListener(type_evenement, fonction)` associe la fonction donnée à l'événement indiqué, sur l'élément concerné. Parmi les types d'événements les plus courants : `"click"` (clic de souris), `"input"` (saisie dans un champ de texte, à chaque caractère tapé), `"submit"` (validation d'un formulaire), `"load"` (chargement terminé d'une page ou d'une image).

### 2.2 Exemple : un compteur de clics

```javascript
let compte = 0;
const bouton = document.getElementById("mon-bouton");
const affichage = document.getElementById("affichage");

bouton.addEventListener("click", function() {
    compte = compte + 1;
    affichage.textContent = "Nombre de clics : " + compte;
});
```

Ici, `document.getElementById("affichage")` récupère un élément du DOM (par exemple un `<span id="affichage">`), et `.textContent` permet de modifier le texte affiché à l'intérieur de cet élément — c'est ainsi que JavaScript peut mettre à jour dynamiquement le contenu d'une page sans avoir à la recharger entièrement.

### 2.3 La fonction comme valeur : le rôle central des fonctions en JavaScript

Ce mécanisme repose sur le fait qu'en JavaScript (comme en Python, où l'on manipule les fonctions comme des valeurs, par exemple en argument de `sorted` avec `key`), une **fonction peut être passée en paramètre** d'une autre fonction. `addEventListener` ne connaît pas à l'avance ce qu'il doit faire lors d'un clic : c'est la fonction qu'on lui fournit qui définit ce comportement, et cette fonction sera appelée automatiquement par le navigateur au moment où l'événement se produit.

---

## 3. Les requêtes HTTP : GET et POST

### 3.1 Le protocole HTTP

Lorsqu'un navigateur affiche une page Web, il communique avec un serveur distant grâce au protocole **HTTP** (HyperText Transfer Protocol) : il envoie une **requête**, le serveur traite cette requête et renvoie une **réponse**.

### 3.2 La méthode GET

La méthode **GET** est utilisée pour **demander** une ressource (une page, une image, des données) au serveur. Les éventuels paramètres de la requête sont inclus directement dans l'**URL**, après un point d'interrogation, sous forme de paires `clé=valeur` séparées par des `&` :

```
http://exemple.fr/salut?nom=Alice&age=17
```

Cette requête demande la ressource `/salut` en transmettant les paramètres `nom=Alice` et `age=17`. Une requête GET n'est, en principe, pas censée modifier l'état du serveur (elle est dite *idempotente* : la répéter plusieurs fois produit le même effet qu'une seule fois) — c'est pourquoi les paramètres d'une recherche ou d'une pagination sont typiquement transmis en GET.

### 3.3 La méthode POST

La méthode **POST** est utilisée pour **envoyer** des données au serveur, généralement pour créer ou modifier une ressource (envoyer un formulaire, publier un message, s'inscrire à un service...). Contrairement à GET, les données sont transmises dans le **corps** de la requête, et non dans l'URL : elles ne sont donc pas visibles dans la barre d'adresse, et il n'y a pas de limite pratique de taille comme c'est le cas avec une URL.

### 3.4 GET vs POST : quand utiliser chacune ?

| Critère | GET | POST |
|---|---|---|
| Emplacement des données | dans l'URL | dans le corps de la requête |
| Visible dans l'URL / l'historique | Oui | Non |
| Limite de taille | oui (limite pratique des URL) | non (ou très large) |
| Effet sur le serveur | ne devrait pas modifier l'état du serveur | peut créer/modifier des données |
| Exemple d'usage typique | recherche, filtre, pagination | connexion (mot de passe), envoi d'un formulaire, upload |

**Attention :** un mot de passe ne doit jamais être transmis en GET, car il apparaîtrait en clair dans l'URL (visible dans l'historique du navigateur, dans les journaux du serveur...) — c'est une raison essentielle pour laquelle les formulaires de connexion utilisent systématiquement POST.

---

## 4. Les formulaires HTML

Un formulaire permet à l'utilisateur de saisir des données et de les envoyer au serveur.

```html
<form action="/inscription" method="POST">
  <label for="nom">Nom :</label>
  <input type="text" id="nom" name="nom">

  <label for="email">Email :</label>
  <input type="email" id="email" name="email">

  <button type="submit">Envoyer</button>
</form>
```

- L'attribut `action` indique l'URL à laquelle la requête sera envoyée.
- L'attribut `method` indique la méthode HTTP utilisée (`GET` ou `POST`).
- L'attribut `name` de chaque champ `<input>` détermine le nom sous lequel la valeur saisie sera transmise au serveur (par exemple, `nom=Alice&email=alice%40mail.fr` en GET, ou dans le corps de la requête en POST).

Lorsque l'utilisateur clique sur le bouton `submit`, le navigateur déclenche automatiquement un événement `"submit"`, collecte les valeurs des champs, et envoie la requête HTTP correspondante vers l'URL indiquée par `action`, avec la méthode indiquée par `method`.

### 4.1 Valider un formulaire côté client avec JavaScript

On peut intercepter l'événement de soumission pour vérifier les données saisies **avant** de les envoyer au serveur (validation côté client), ce qui améliore l'expérience utilisateur (retour immédiat, sans attendre une réponse du serveur) :

```javascript
function validerFormulaire(nom, email) {
    const erreurs = [];
    if (nom.trim() === "") {
        erreurs.push("Le nom est obligatoire.");
    }
    if (!email.includes("@")) {
        erreurs.push("L'email doit contenir un @.");
    }
    return erreurs;
}
```

**Point de vigilance important :** la validation côté client (en JavaScript, dans le navigateur) est une aide pour l'utilisateur, mais elle ne constitue **jamais** une sécurité suffisante, car un utilisateur malveillant peut désactiver JavaScript ou envoyer directement une requête HTTP fabriquée à la main, en contournant totalement la page. Toute donnée reçue doit donc **impérativement** être revalidée côté serveur.

---

## Synthèse

| Notion | Point clé à retenir |
|---|---|
| HTML | Décrit la structure d'une page avec des balises ; construit le DOM |
| Événement | Action (clic, saisie...) associée à une fonction via `addEventListener` |
| GET | Paramètres dans l'URL, ne modifie pas l'état du serveur |
| POST | Données dans le corps de la requête, utilisé pour créer/modifier des données |
| Formulaire | `action` (URL cible), `method` (GET/POST), déclenche un événement `submit` |
| Validation client vs serveur | La validation JavaScript aide l'utilisateur mais ne remplace jamais une validation côté serveur |

*Prochaine étape suggérée : Chapitre 5 — Architecture séquentielle (von Neumann).*
