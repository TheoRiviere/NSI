# Analyse d'intention — Parcours séquentiel et recherche dichotomique

## Objectifs :
Consolider la manipulation des tableaux vue en cours (parcours, recherche), faire acquérir la méthode de preuve d'un algorithme par invariant de boucle, et faire percevoir concrètement, par le calcul, l'intérêt de la recherche dichotomique par rapport à la recherche séquentielle.

## Pré-requis à cette activité :
Notion de tableau (types construits), boucle `for`, algorithmes de recherche séquentielle et de recherche dichotomique déjà présentés en cours — cette fiche est une consolidation, pas une découverte.

## Durée de l'activité :
Environ 1h30, à réaliser en autonomie (en classe ou à la maison), avec rendu individuel sous forme d'archive.

## Exercices cibles :
Cette activité prépare les exercices ultérieurs sur la complexité algorithmique et sur des structures de données plus riches (listes chaînées, arbres) abordées plus tard dans l'année.

## Description du déroulement de l'activité :
L'exercice 1 réinvestit directement le cours par deux fonctions de parcours simple (minimum, comptage d'occurrences).

L'exercice 2 fait construire un invariant de boucle sur une fonction de somme donnée, en suivant les trois étapes classiques (initialisation, conservation, terminaison). 

L'exercice 3 fait dérouler à la main la recherche dichotomique sur un exemple concret, à la fois pour une valeur présente et pour une valeur absente. 

L'exercice 4 fait modifier le code pour compter les comparaisons effectuées, puis comparer quantitativement les deux cas, ouvrant sur la notion de complexité en O(log n).

Les corrigés fournis en fin de fiche permettent au professeur d'aider les élèves, ou permettent une auto-correction en autonomie.

## Anticipation des difficultés des élèves :
La construction de l'invariant de boucle (exercice 2) est probablement le point le plus délicat, car elle demande une capacité d'abstraction nouvelle pour des élèves de première : il peut être utile de rappeler collectivement, avant l'activité, la démarche générale (formuler ce qui est vrai à un instant donné de la boucle). Le déroulé à la main de la dichotomie (exercice 3) peut aussi donner lieu à des erreurs sur le calcul des indices (milieu, bornes gauche/droite).

## Gestion de l'hétérogénéité :
Pour les élèves en difficulté, une reprise collective peut être prévue sur l'exercice 2 avant de les laisser poursuivre seuls.
