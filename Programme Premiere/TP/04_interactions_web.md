# Chapitre 4 — Interactions Homme-Machine sur le Web
## TP sur machine — Page interactive et petit serveur HTTP

*Première NSI — HTML / JavaScript / Python 3 — Durée indicative : 1h30 à 2h*

---

## Objectifs

- Construire une page HTML interactive avec des événements JavaScript.
- Observer concrètement une requête GET et une requête POST.
- Écrire un mini serveur HTTP en Python qui répond à ces deux types de requêtes.

---

## Partie A — Une page HTML/JS interactive

**A.1.** Créer un fichier `page.html` contenant un titre, un bouton d'identifiant `"btn"`, et un paragraphe vide d'identifiant `"resultat"`.

**A.2.** Dans une balise `<script>` en bas de la page, ajouter un gestionnaire d'événement sur le bouton qui, à chaque clic, incrémente un compteur et affiche `"Nombre de clics : N"` dans le paragraphe `"resultat"` (reprendre l'exemple du cours).

**A.3.** Ouvrir `page.html` directement dans un navigateur (double-clic sur le fichier, ou glisser-déposer dans le navigateur) et vérifier que le compteur fonctionne.

**A.4.** Ajouter un second bouton `"Réinitialiser"` qui remet le compteur à 0 et met à jour l'affichage.

---

## Partie B — Un mini serveur HTTP en Python

On va maintenant écrire un petit serveur qui répond à des requêtes GET et POST, afin d'observer concrètement la différence entre les deux méthodes vues en cours.

**B.1.** Créer un fichier `serveur.py` et importer les modules nécessaires :
```python
import http.server
import socketserver
import urllib.parse
```

**B.2.** Définir une classe `Handler` héritant de `http.server.BaseHTTPRequestHandler`, avec une méthode `do_GET(self)` qui :
- récupère les paramètres de la requête depuis `self.path` (indication : `urllib.parse.urlparse(self.path)` sépare le chemin des paramètres, et `urllib.parse.parse_qs(...)` transforme la chaîne de paramètres en dictionnaire) ;
- si le chemin est `/salut`, récupère le paramètre `nom` (avec une valeur par défaut `"visiteur"` s'il est absent), et répond avec le texte `"Bonjour, <nom> !"` ;
- sinon, répond avec un code d'erreur `404`.

**B.3.** Ajouter une méthode `do_POST(self)` qui :
- lit le corps de la requête (indication : la taille du corps est indiquée par l'en-tête `Content-Length`, et le corps se lit avec `self.rfile.read(longueur)`) ;
- décode ce corps avec `urllib.parse.parse_qs` pour récupérer le paramètre `message` ;
- répond avec le texte `"Message reçu : <message>"`.

**B.4.** Lancer le serveur sur le port `8123` :
```python
server = socketserver.TCPServer(("127.0.0.1", 8123), Handler)
server.serve_forever()
```

**B.5.** Une fois le serveur lancé (dans un premier terminal), ouvrir un **second terminal** (ou utiliser `urllib.request` dans un autre script Python) et tester :
- une requête GET : ouvrir dans un navigateur `http://127.0.0.1:8123/salut?nom=Alice` et observer la réponse ;
- une requête POST : envoyer par exemple, depuis un script Python séparé, une requête POST avec `urllib.request` (voir le corrigé) et observer la réponse.

**B.6.** Modifier la page HTML de la partie A pour qu'elle contienne un champ de saisie et un bouton `"Envoyer"`, qui, au clic, effectue une requête vers `http://127.0.0.1:8123/salut?nom=...` avec la fonction `fetch` de JavaScript, et affiche la réponse reçue dans la page (indication : `fetch(url).then(reponse => reponse.text()).then(texte => { ... })`).

---

## Corrigé indicatif

### Partie A — `page.html`

```html
<!DOCTYPE html>
<html>
<head><title>Compteur de clics</title></head>
<body>
  <h1>Compteur de clics</h1>
  <button id="btn">Cliquez ici</button>
  <button id="btn-reset">Réinitialiser</button>
  <p id="resultat">Nombre de clics : 0</p>

  <script>
    let compte = 0;
    const bouton = document.getElementById("btn");
    const boutonReset = document.getElementById("btn-reset");
    const resultat = document.getElementById("resultat");

    bouton.addEventListener("click", function() {
        compte = compte + 1;
        resultat.textContent = "Nombre de clics : " + compte;
    });

    boutonReset.addEventListener("click", function() {
        compte = 0;
        resultat.textContent = "Nombre de clics : " + compte;
    });
  </script>
</body>
</html>
```

### Partie B — `serveur.py`

```python
import http.server
import socketserver
import urllib.parse

class Handler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        chemin_analyse = urllib.parse.urlparse(self.path)
        if chemin_analyse.path == "/salut":
            params = urllib.parse.parse_qs(chemin_analyse.query)
            nom = params.get("nom", ["visiteur"])[0]
            reponse = f"Bonjour, {nom} !"
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")   # pour autoriser fetch() depuis page.html
            self.end_headers()
            self.wfile.write(reponse.encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        longueur = int(self.headers["Content-Length"])
        corps = self.rfile.read(longueur).decode("utf-8")
        donnees = urllib.parse.parse_qs(corps)
        message = donnees.get("message", [""])[0]
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(f"Message reçu : {message}".encode("utf-8"))


if __name__ == "__main__":
    server = socketserver.TCPServer(("127.0.0.1", 8123), Handler)
    print("Serveur lancé sur http://127.0.0.1:8123")
    server.serve_forever()
```

**Test de la requête GET** (dans un navigateur, une fois le serveur lancé) :
```
http://127.0.0.1:8123/salut?nom=Alice
```
affiche : `Bonjour, Alice !`

**Test de la requête POST** (script Python séparé, pendant que `serveur.py` tourne) :
```python
import urllib.request
import urllib.parse

donnees = urllib.parse.urlencode({"message": "Bonjour serveur"}).encode("utf-8")
requete = urllib.request.Request("http://127.0.0.1:8123/salut", data=donnees, method="POST")
reponse = urllib.request.urlopen(requete)
print(reponse.read().decode("utf-8"))
# Message reçu : Bonjour serveur
```

**B.6 — extrait JavaScript avec `fetch`, à ajouter dans `page.html` :**
```html
<input type="text" id="champ-nom" placeholder="Votre nom">
<button id="btn-envoyer">Envoyer</button>
<p id="reponse-serveur"></p>

<script>
  document.getElementById("btn-envoyer").addEventListener("click", function() {
      const nom = document.getElementById("champ-nom").value;
      fetch("http://127.0.0.1:8123/salut?nom=" + encodeURIComponent(nom))
          .then(reponse => reponse.text())
          .then(texte => {
              document.getElementById("reponse-serveur").textContent = texte;
          });
  });
</script>
```

**Remarque :** cette dernière étape illustre concrètement le principe des applications Web modernes : une page HTML/JavaScript exécutée dans le navigateur (le **client**) communique, en arrière-plan et sans recharger la page, avec un programme qui tourne sur un **serveur**, via des requêtes HTTP.
