# -*- coding: latin-1 -*-
"""
Created on Mon Jun 30 11:04:45 2014

@author: Florian, Handers
"""

from modules import graph, analyseClusters, util, clusters
from numpy import flipud
import matplotlib.pyplot as plt
from time import clock


def test(index=4, tempo=100):
    """
    Teste la classe Graph avec une configuration préenregistrée
    Affiche la taille du plus gros cluster, la qualité de la connection
    et affiche en dernier le graphique avec les clusters représentés

    Arguments facultatifs:
    index -- (int) Pour sélectionner une configuration spécifique parmi celles
    de la liste 'situations' (défaut = 4)

    tempo -- (int) Pour préciser la durée d'une note du jingle de fin
    (défaut = 100)
    """
    tempsDepart = clock()

    situations = [[20, 20, 40, 4], [2000, 2000, 100000, 25], [4, 4, 6, 2],
                  [100, 100, 10000, 2], [2, 2, 4, 2]]

    situationChoisie = situations[index]

    print("ETAPE 1 : ")
    g = graph.Graph(situationChoisie[0], situationChoisie[1],
                    situationChoisie[2], situationChoisie[3], True)

    print("ETAPE 2 : ")
    c = clusters.Clusters(g, True)
    taillePlusGrandCluster = len(c.clusters[0])
    n = g.n

    print(c.nclusters, " Clusters")

    print("Plus grand : " + str(taillePlusGrandCluster) + "/" + str(n) + \
        " Téléphones (" + str(taillePlusGrandCluster*100//n) + "%)")

    print("Qualité de la connexion : " + str(analyseClusters.qualiteConnection(c)))

    tgraph = c.afficherPlotAvecClusters(True)

    t0 = clock() - tempsDepart
    print("Temps total : ", t0)
    util.jingle(tempo)

    return g, c, tgraph, t0


def testCarte(p, n=None, carte=0, afficherCarte=False, tempo=100):
    """
    Teste la classe Graph avec une certaine portée, en suivant la répartition
    et la taille d'une carte (image BMP)
    Affiche la taille du plus gros cluster, la qualité de la connection
    et affiche en dernier le graphique avec les clusters représentés

    Arguments facultatifs:
    n -- (int) Forcer l'espérance du nombres de téléphone présents en modifiant
    légèrement la carte

    carte -- (int) Sélectionner une carte parmi la liste 'cartes' (défaut = 0)

    afficherCarte -- (bool) Afficher la carte seule dans un graphique à part
    (défaut = False)
    """
    tempsDepart = clock()
    cartes = ['picasso.bmp', 'hrm.bmp', 'ville.bmp', 'presque vide.bmp']
    print("ETAPE 1 : ")
    g = graph.GraphCarte(p, './modules/cartes/' + cartes[carte], n, True)
    n = g.n
    if afficherCarte:
        plt.figure('Image Originale')
        plt.imshow(flipud(g.carte), origin='lower')

    print("ETAPE 2 : ")
    c = clusters.Clusters(g, True)
    taillePlusGrandCluster = len(c.clusters[0])

    print(c.nclusters, " Clusters")

    print("Plus grand : " + str(taillePlusGrandCluster) + "/" + str(n) + \
        " Téléphones (" + str(taillePlusGrandCluster * 100 // n) + "%)")

    print("Qualité de la connexion : " + str(analyseClusters.qualiteConnection(c)))

    tgraph = c.afficherPlotAvecClusters(True)

    t0 = clock() - tempsDepart
    print("Temps total : ", t0)
    util.jingle(tempo)

    return g, c, tgraph, t0

if __name__ == "__main__":
    t = testCarte(2, 10, carte = 3, afficherCarte=True, tempo=0)
    # t = test(0, 0)