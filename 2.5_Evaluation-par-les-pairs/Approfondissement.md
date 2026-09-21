# Approfondissement — Recherche et tri : au-delà de la dichotomie

## Contexte et nature de l'activité :
Il s'agit d'une activité d'approfondissement individuelle, destinée aux élèves ayant terminé rapidement et correctement la fiche d'activité « Parcours séquentiel et recherche dichotomique », en particulier l'exercice 4 sur la comparaison des coûts. Elle prolonge cette réflexion vers le tri d'un tableau, notion connexe du programme de première NSI, sans introduire de nouvel outil technique.

## Objectifs :
Étendre la réflexion amorcée sur le coût des algorithmes de recherche à un algorithme de tri simple, et faire percevoir l'intérêt d'amortir le coût d'un tri lorsqu'il permet ensuite des recherches dichotomiques répétées.

## Pré-requis à cette activité :
Avoir terminé la fiche d'exercices initiale, en particulier l'exercice 4 sur le comptage des comparaisons en recherche dichotomique.

## Durée de l'activité :
45 minutes à 1 heure, en autonomie.

## Description du déroulement de l'activité :
Les élèves écrivent une fonction `tri_selection(tableau)` réalisant un tri par sélection. Ils dénombrent ensuite, pour plusieurs petites tailles de tableau (4, 5, 6 éléments), le nombre de comparaisons effectuées, afin de repérer un motif et d'en déduire une formule générale en fonction de n (aboutissant à une complexité en O(n²)). Ils comparent enfin ce coût à celui de la recherche dichotomique vu dans l'activité initiale, et discutent pourquoi trier une seule fois un tableau puis y effectuer plusieurs recherches dichotomiques reste avantageux malgré le coût plus élevé du tri. Une question optionnelle invite les élèves les plus à l'aise à rechercher et présenter le principe du tri fusion et sa complexité en O(n log n).

## Anticipation des difficultés des élèves :
Le passage du dénombrement concret des comparaisons à une formule générale en fonction de n peut être difficile : on peut guider les élèves en leur demandant de d'abord compter pour plusieurs petites valeurs de n avant de généraliser.

## Gestion de l'hétérogénéité :
Cette activité s'adresse déjà aux élèves les plus avancés sur l'activité initiale ; la question optionnelle sur le tri fusion permet de moduler encore la difficulté pour les élèves les plus à l'aise, sans pénaliser ceux qui s'arrêtent à la question précédente.
