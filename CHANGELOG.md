## 12-10-2014

Features:
  - Implémentation du protocole Rhizome
  - Implémentation d'une régression des temps de calculs de rhizome

Miscellaneous:
  - Suppression de fichiers en doubles dans autres
  - Optimisations diverses de Rhizome
  - Changement de nom dans la license du MIT

  
## 05-10-2014

Bugfixes:
  - Correction du problème des 3 points bleus et du point rouge dans la situation (2, 2, 4)

Miscellaneous:
  - Commentaire du paramètre tempo dans la fonction test de main
  - Correction de commentaires dans analyse

## 03-10-2014

Miscellaneous:
  - Ajout de dessins explicatifs de la fonction cluster
  - Analyses de complexité pour la fonction cluster avec de grandes valeurs

  ## 30-09-2014

Miscellaneous:
  - Correction d'une faute d'orthographe
  
## 29-09-2014

Miscellaneous:
  - Renommage de certains fichiers dans "autres" pour une meilleure compréhension
  - Analyses de complexité de la fonction cluster
  - Ajout de commentaires dans analyse.py

## 28-09-2014 :

Features:
  - Ajout d'un paramètre dans statsComplexiteClusters et statsClusters pour choisir ou non d'afficher uniquement la moyenne des points
 
Bugfixes:
  - Suppression d'un import inutilisé
  - Correction d'un bug qui affichait la légende d'un mauvais graphique dans statsComplexiteClusters
  
Miscellaneous:
  - Renommage des anciens fichiers de simulation a la nouvelle norme
  - La légende des graphiques se place maintenant a la meilleure position possible
  - Ajout d'une image représentant la complexité de la classe Cluster

## 26-09-2014 :

Features:
  - Création d'un compteur dans la classe Clusters pour calculer la complexité
  - Création des fonctions simulationsComplexiteClusters, simulationComplexiteClusters et statsComplexiteClusters dans analyse pour réaliser des statistiques sur le compteur

Miscellaneous:
  - Ajout de la docstring a la fonction jingle

## 12-09-2014 :

Features:
  - Création du module "jingle" pour signaler la fin d'une simulation
  - Ajout d'une symphonie simple pour le jingle
  - Ajout d'un mode "off" au jingle
Bugfixes:
  - Réécriture de la méthode de création des points dans la classe Graph
  - Dans le cas ou scipy est en version < 0.13.0, on désactive une des fonctionnalités de afficherPlotAvecClusters
  - Suppression d'un bug dans afficherPlotAvecClusters qui tentais d'afficher la carte d'un Graph normal
  
## 02-09-2014 :

Miscellaneous:
  - Création du repository GitHub
  - Formatage du CHANGELOG en .md
  - Création de la branche "develop" pour les commits "temporaires"
  - Renommage du fichier de la license MIT de LICENSE en LICENSE.md
  - Modification de certains commentaires
  - Suppression du script "Clear pyc.bat" devenu inutile grace au .gitignore
  - Verification pylint + pep8, RAS
  
## 26-07-2014 :

Features:
  - Support partiel des cartes en couleur (conversion RGB vers Greyscale)
  - Nouvelle carte en couleurs
  - Ajout d'une liste de cartes dans la fonction testCarte (parceque les noms de fichiers c'est long a taper)
  - Ajout de la possibilité d'afficher la carte seule dans une figure a part dans testCarte
  - Ajout de fonctionnalités debug dans Clusters, pathFindingDijkstra, afficherPlot, afficherPlotAvecClusters
  - Ajout de l'affichage des temps totaux dans test et testCarte
  - Les fonctions test et testCarte retournent désormais les temps de calcul des différentes fonctions.
  - simulationsClusters retournes également la liste des temps de calcul de chaque simulation
  
Bugfixes:
  - Changement de la transparence du remplissage afficherPlotAvecClusters (alpha passe de 0.5 a 0.2)
  - le "for cotes in enveloppe.simplices" de contoursCluster est délocalisé directement dans afficherPlotAvecClusters pour éviter de faire deux boucles qui parcourent le même élément
  
Miscellaneous:
  - Renommage et améliorations de lisibilité dans contoursCluster
  - Réorganisation du code pour ne pas dépasser la "limite" des 79 caractères sur une ligne
  - Vérification de conformité a la PEP8, 557 erreurs de mise en forme corrigées
  - Check up complet avec pylint (Analyse syntaxique), note de départ 1.44/10, 282 Erreurs corrigées, note finale 9.58/10
  - Ajout de toutes les docstrings
  - Ajout du fichier de configuration de pylint (pylint.rc)
  - Inversement du sens du CHANGELOG (plus récent en haut)

## 25-07-2014 :

Features:
  - Héritage de la classe GraphCarte
  - Image de la carte en background du afficherPlotAvecClusters

Miscellaneous:
  - Début du suivi de version
  - Backup des screenshots
  - Création du dossier sur MEGA