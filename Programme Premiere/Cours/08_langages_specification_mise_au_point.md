# Chapitre 8 — Langages, spécification et mise au point de programmes

## Objectifs

- Identifier les constructions élémentaires communes à la plupart des langages de programmation.
- Comprendre l'intérêt de la diversité des langages de programmation.
- Écrire une spécification de fonction (préconditions, postconditions).
- Construire un jeu de tests pertinent pour une fonction.
- Utiliser des techniques de mise au point (débogage) et des bibliothèques.

## Prérequis

- Définition de fonctions, structures conditionnelles et répétitives en Python.

---

## 1. Les constructions élémentaires d'un langage de programmation

Malgré leur grande diversité apparente, la quasi-totalité des langages de programmation reposent sur un petit nombre de **constructions élémentaires** communes :

- **l'affectation** (donner une valeur à une variable) ;
- **la séquence** (exécuter des instructions les unes après les autres) ;
- **le test conditionnel** (exécuter certaines instructions seulement si une condition est vérifiée : `if`/`else`) ;
- **la répétition** (boucles : `for`, `while`) ;
- **la définition et l'appel de fonctions** (regrouper des instructions réutilisables, avec des paramètres).

Ce sont ces mêmes briques de base que l'on retrouve, sous des syntaxes différentes, dans des langages aussi variés que Python, C, Java ou JavaScript.

```python
# Python
if x > 0:
    print("positif")
```
```c
// C
if (x > 0) {
    printf("positif\n");
}
```
```javascript
// JavaScript
if (x > 0) {
    console.log("positif");
}
```

---

## 2. La diversité des langages de programmation

Il existe des centaines de langages de programmation, et cela n'est pas un hasard : chacun a été conçu avec des objectifs différents, qui le rendent plus ou moins adapté selon le contexte.

| Langage | Domaine typique | Caractéristique notable |
|---|---|---|
| Python | Enseignement, science des données, scripts | Syntaxe simple, très lisible |
| C | Systèmes embarqués, systèmes d'exploitation | Proche du matériel, très performant |
| JavaScript | Pages Web interactives | Exécuté nativement par les navigateurs |
| SQL | Bases de données | Langage déclaratif dédié aux requêtes |
| HTML/CSS | Structure et mise en forme de pages Web | Langages de description, pas de programmation générale |

On distingue notamment les langages **compilés** (le code source est traduit intégralement en langage machine avant l'exécution, par exemple le C) des langages **interprétés** (le code est lu et exécuté instruction par instruction par un autre programme, l'interpréteur, par exemple Python) — un langage interprété est généralement plus simple à tester rapidement, mais un programme compilé s'exécute souvent plus vite.

---

## 3. Spécifier une fonction : préconditions et postconditions

### 3.1 Pourquoi spécifier ?

Avant même d'écrire le code d'une fonction, il est utile d'en définir précisément le **contrat** : ce qu'elle attend en entrée, et ce qu'elle garantit en sortie. C'est ce qu'on appelle sa **spécification**.

- La **précondition** décrit ce qui doit être vrai sur les paramètres pour que la fonction fonctionne correctement (elle est de la responsabilité de celui qui **appelle** la fonction).
- La **postcondition** décrit ce que la fonction garantit sur son résultat, à condition que la précondition ait été respectée (elle est de la responsabilité de celui qui **écrit** la fonction).

```python
def racine_carree_entiere(n):
    """
    Précondition : n est un entier positif ou nul.
    Postcondition : renvoie le plus grand entier r tel que r*r <= n.
    """
    assert n >= 0, "n doit être positif ou nul"
    r = 0
    while (r + 1) * (r + 1) <= n:
        r += 1
    assert r * r <= n and (r + 1) * (r + 1) > n
    return r
```

L'instruction `assert condition, message` vérifie que `condition` est vraie ; si ce n'est pas le cas, elle interrompt immédiatement le programme en levant une exception `AssertionError`, avec le message donné. On peut ainsi vérifier **explicitement**, dans le code, qu'une précondition ou une postcondition est bien respectée — un outil précieux pour détecter au plus tôt une utilisation incorrecte d'une fonction, ou une erreur dans son implémentation.

### 3.2 Documenter avec une chaîne de documentation (*docstring*)

La chaîne entre triples guillemets juste après la définition de la fonction (comme ci-dessus) s'appelle une **docstring** : c'est l'endroit conventionnel, en Python, pour décrire la spécification d'une fonction (son rôle, ses préconditions, ses postconditions), de façon à ce qu'une personne qui souhaite l'utiliser n'ait pas besoin de lire son implémentation pour savoir comment s'en servir.

---

## 4. Construire un jeu de tests

### 4.1 Pourquoi tester ?

Un programme, aussi simple soit-il, contient souvent des erreurs (des **bugs**) lors de sa première écriture. Tester consiste à exécuter le programme sur des cas d'entrée connus, dont on connaît par avance le résultat attendu, afin de vérifier qu'il se comporte correctement.

### 4.2 Un bon jeu de tests

Un jeu de tests pertinent doit couvrir :

- des **cas simples et typiques** (le fonctionnement « normal ») ;
- des **cas limites** (valeurs extrêmes : 0, une liste vide, le plus grand ou le plus petit élément...) ;
- si pertinent, des cas où la précondition n'est **pas** respectée, pour vérifier que la fonction réagit comme prévu (lève bien une erreur, par exemple).

```python
def tester_racine_carree_entiere():
    cas_de_test = [
        (0, 0), (1, 1), (2, 1), (3, 1), (4, 2),
        (10, 3), (15, 3), (16, 4), (99, 9), (100, 10),
    ]
    for entree, attendu in cas_de_test:
        resultat = racine_carree_entiere(entree)
        assert resultat == attendu, f"échec pour n={entree} : attendu {attendu}, obtenu {resultat}"
    print("Tous les tests ont réussi !")

tester_racine_carree_entiere()
```

Écrire une fonction de test comme celle-ci présente un double avantage : elle documente le comportement attendu de la fonction testée, et elle permet de **revérifier automatiquement** ce comportement après toute modification du code (une pratique essentielle dès qu'un programme grandit).

---

## 5. Mise au point (débogage)

### 5.1 Techniques de base

Lorsqu'un programme ne se comporte pas comme attendu, plusieurs techniques permettent d'en identifier la cause :

- **Relire attentivement le code** et le message d'erreur (une exception Python indique la ligne exacte où l'erreur s'est produite, et souvent une explication précise).
- **Ajouter des affichages temporaires** (`print(...)`) à des points stratégiques du programme, pour observer la valeur des variables à différents moments de l'exécution.
- **Isoler le problème** en testant séparément chaque petite partie du code (par exemple, tester une fonction seule, avec des valeurs simples, plutôt que le programme entier).
- **Utiliser un débogueur** (outil intégré à de nombreux environnements de développement), qui permet d'exécuter le programme pas à pas et d'inspecter l'état des variables à tout moment.

### 5.2 Exemple : traquer un bug avec des affichages

```python
def moyenne_buggee(notes):
    total = 0
    for note in notes:
        total = note          # BUG : devrait être total += note
    return total / len(notes)

moyenne_buggee([10, 12, 14])   # renvoie 4.67 au lieu de 12.0 !
```

En ajoutant un affichage à l'intérieur de la boucle, le bug devient évident :

```python
def moyenne_debug(notes):
    total = 0
    for note in notes:
        total = note
        print("total apres cette note :", total)   # affichage de debogage
    return total / len(notes)

moyenne_debug([10, 12, 14])
# total apres cette note : 10
# total apres cette note : 12
# total apres cette note : 14     <- on voit que "total" ne fait qu'être remplacé, pas cumulé !
```

Une fois le bug identifié (`total = note` au lieu de `total += note`, qui **remplace** la valeur précédente au lieu de l'**accumuler**), la correction est immédiate :

```python
def moyenne_correcte(notes):
    total = 0
    for note in notes:
        total += note
    return total / len(notes)
```

---

## 6. Utiliser des bibliothèques

Il est rarement nécessaire de tout réécrire soi-même : Python fournit de nombreuses **bibliothèques** (modules), regroupant des fonctions déjà écrites, testées et optimisées, pour des besoins courants.

```python
import math
math.sqrt(16)    # 4.0  (racine carrée exacte, en flottant)
math.floor(3.7)  # 3    (arrondi à l'entier inférieur)
math.ceil(3.2)   # 4    (arrondi à l'entier supérieur)

import random
random.randint(1, 6)   # entier aléatoire entre 1 et 6 (inclus) - simule un dé
```

**Bonnes pratiques :** avant d'écrire soi-même une fonction pour un besoin courant (racine carrée, tri, génération aléatoire...), il est utile de vérifier si une bibliothèque standard ne la propose pas déjà — cela évite de dupliquer du code déjà écrit, testé et généralement plus efficace que ce qu'on pourrait écrire rapidement soi-même.

---

## Synthèse

| Notion | Point clé à retenir |
|---|---|
| Constructions élémentaires | Affectation, séquence, test, répétition, fonction — communes à presque tous les langages |
| Compilé vs interprété | Traduit avant exécution (rapide) vs exécuté directement (souple, plus simple à tester) |
| Précondition / postcondition | Contrat d'une fonction : ce qu'elle exige / ce qu'elle garantit |
| `assert` | Vérifie une condition, interrompt le programme si elle est fausse |
| Jeu de tests | Cas typiques + cas limites, pour vérifier automatiquement le bon comportement |
| Débogage | Lecture du message d'erreur, affichages temporaires, isolement du problème, débogueur |
| Bibliothèque | Code déjà écrit et testé, à réutiliser plutôt qu'à réécrire |

*Prochaine étape suggérée : Chapitre 9 — Parcours séquentiel et recherche dichotomique.*
