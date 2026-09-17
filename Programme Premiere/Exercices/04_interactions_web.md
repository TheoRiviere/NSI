# Chapitre 4 — Interactions Homme-Machine sur le Web
## Fiche d'exercices

*Première NSI*

---

### Exercice 1 — Structure HTML

1. Écrire le code HTML d'une page contenant un titre principal `"Mon blog"`, un paragraphe de présentation, et une image (balise `<img>`, avec un attribut `src` de votre choix et un attribut `alt` décrivant l'image).
2. À quoi sert l'attribut `alt` d'une image ? Citer une situation où il est particulièrement utile.
3. Ajouter à cette page un lien (`<a>`) pointant vers `"https://exemple.fr"`, avec le texte `"En savoir plus"`.

### Exercice 2 — Événements

1. Écrire le code HTML d'un bouton avec l'identifiant `"btn-masquer"` et d'un paragraphe avec l'identifiant `"texte"`.
2. Écrire le code JavaScript qui, au clic sur ce bouton, bascule la visibilité du paragraphe (indication : on peut utiliser la propriété `style.display`, qui vaut `"none"` pour masquer un élément et `""` ou `"block"` pour l'afficher).
3. Sur le principe de l'exercice précédent, écrire une fonction JavaScript `creerBasculeur()` qui renvoie une fonction : chaque appel de cette fonction renvoyée doit inverser et renvoyer un état booléen interne (`visible`), initialisé à `true` (indication : on utilise une **fermeture**, *closure*, comme dans le cours pour le compteur de clics — la variable `visible` reste accessible d'un appel à l'autre car elle est définie dans la fonction englobante).
4. Vérifier que trois appels successifs à la fonction renvoyée par `creerBasculeur()` renvoient, dans l'ordre, `false`, `true`, `false`.

### Exercice 3 — GET ou POST ?

Pour chacune des situations suivantes, indiquer si l'on devrait utiliser GET ou POST, et justifier brièvement :

1. Rechercher des articles contenant un mot-clé sur un site marchand.
2. Envoyer un formulaire de connexion (identifiant + mot de passe).
3. Changer de page dans une liste de résultats paginée (page 1, page 2...).
4. Publier un nouveau message sur un réseau social.
5. Uploader une photo de profil.

### Exercice 4 — Construire une URL de requête GET

1. Écrire une fonction JavaScript `construireURL(base, params)` qui prend une URL de base (chaîne) et un objet `params` (paires clé/valeur), et renvoie l'URL complète avec les paramètres ajoutés (indication : utiliser l'objet natif `URL` et sa propriété `searchParams`, avec la méthode `.set(cle, valeur)`).
2. Vérifier que `construireURL("http://exemple.fr/recherche", {q: "NSI", page: "2"})` renvoie `"http://exemple.fr/recherche?q=NSI&page=2"`.

### Exercice 5 — Formulaire et validation

On donne le formulaire HTML suivant :
```html
<form id="mon-formulaire">
  <input type="text" id="nom" name="nom">
  <input type="email" id="email" name="email">
  <button type="submit">Envoyer</button>
</form>
```

1. Pourquoi est-il important de revalider, côté serveur, les données envoyées par ce formulaire, même si une validation a déjà été faite en JavaScript côté client ?
2. Écrire une fonction JavaScript `validerFormulaire(nom, email)` (reprise du cours) et l'utiliser pour vérifier les couples suivants : `("Alice", "alice@mail.fr")`, `("", "bob@mail.fr")`, `("Chloé", "pasuneemail")`. Pour chacun, indiquer si le formulaire serait accepté et, sinon, quelles erreurs seraient renvoyées.

---

## Corrigés

### Exercice 1

1.
```html
<!DOCTYPE html>
<html>
  <head><title>Mon blog</title></head>
  <body>
    <h1>Mon blog</h1>
    <p>Bienvenue sur mon blog, où je partage mes découvertes en informatique.</p>
    <img src="photo.jpg" alt="Photo de l'auteur du blog">
  </body>
</html>
```
2. L'attribut `alt` fournit une description textuelle de l'image, affichée si l'image ne peut pas se charger, et lue par les **lecteurs d'écran** utilisés par les personnes malvoyantes (accessibilité). Il est donc indispensable pour l'accessibilité du site et utile en cas d'échec de chargement de l'image.
3.
```html
<a href="https://exemple.fr">En savoir plus</a>
```

### Exercice 2

1.
```html
<button id="btn-masquer">Afficher/masquer</button>
<p id="texte">Ce texte peut être masqué.</p>
```
2.
```javascript
const bouton = document.getElementById("btn-masquer");
const paragraphe = document.getElementById("texte");

bouton.addEventListener("click", function() {
    if (paragraphe.style.display === "none") {
        paragraphe.style.display = "";
    } else {
        paragraphe.style.display = "none";
    }
});
```
3-4.
```javascript
function creerBasculeur() {
    let visible = true;
    return function() {
        visible = !visible;
        return visible;
    };
}

const basculer = creerBasculeur();
basculer();   // false
basculer();   // true
basculer();   // false
```

### Exercice 3

1. **GET** : c'est une recherche, elle ne modifie pas l'état du serveur, et il est pratique de pouvoir partager ou mettre en favori l'URL de résultats.
2. **POST** : les identifiants (en particulier le mot de passe) ne doivent jamais apparaître dans l'URL.
3. **GET** : le numéro de page est un paramètre de consultation, ne modifiant rien côté serveur ; c'est aussi pratique pour pouvoir revenir en arrière ou partager le lien d'une page précise.
4. **POST** : cette action crée une nouvelle ressource (le message) sur le serveur.
5. **POST** : il s'agit d'un envoi de données (potentiellement volumineuses) qui modifie l'état du serveur (le profil de l'utilisateur) ; une image ne pourrait de toute façon pas être transmise raisonnablement dans une URL.

### Exercice 4

```javascript
function construireURL(base, params) {
    const url = new URL(base);
    for (const cle in params) {
        url.searchParams.set(cle, params[cle]);
    }
    return url.toString();
}

construireURL("http://exemple.fr/recherche", {q: "NSI", page: "2"});
// "http://exemple.fr/recherche?q=NSI&page=2"
```

### Exercice 5

1. Une validation uniquement côté client peut être **contournée** : un utilisateur peut désactiver JavaScript dans son navigateur, ou envoyer directement une requête HTTP fabriquée « à la main » (avec un outil comme `curl` ou un script), sans jamais passer par le formulaire ni son JavaScript de validation. Seule une vérification effectuée **sur le serveur**, qui ne peut pas être contournée par l'utilisateur, garantit réellement l'intégrité et la sécurité des données traitées.
2.
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
- `("Alice", "alice@mail.fr")` : aucune erreur, formulaire **accepté**.
- `("", "bob@mail.fr")` : une erreur, `"Le nom est obligatoire."` — formulaire **refusé**.
- `("Chloé", "pasuneemail")` : une erreur, `"L'email doit contenir un @."` — formulaire **refusé**.
