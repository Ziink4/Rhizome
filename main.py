# -*- coding: latin-1 -*-
"""
Created on Mon Jun 30 11:04:45 2014

@author: Florian, Handers
"""

from modules import graph, util, clusters, analyseClusters
from numpy import flipud
import matplotlib.pyplot as plt
from time import perf_counter


def test(index=4, tempo=100):
    """
    Teste la classe Graph avec une configuration pr�enregistr�e
    Affiche la taille du plus gros cluster, la qualit� de la connection
    et affiche en dernier le graphique avec les clusters repr�sent�s

    Arguments facultatifs:
    index -- (int) Pour s�lectionner une configuration sp�cifique parmi celles
    de la liste 'situations' (d�faut = 4)

    tempo -- (int) Pour pr�ciser la dur�e d'une note du jingle de fin
    (d�faut = 100)
    """
    tempsDepart = perf_counter()

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
          " T�l�phones (" + str(taillePlusGrandCluster * 100 // n) + "%)")

    print("Qualit� de la connexion : " + str(analyseClusters.qualiteConnection(c)))

    tgraph = c.afficherPlotAvecClusters(True)

    t0 = perf_counter() - tempsDepart
    print("Temps total : ", t0)
    util.jingle(tempo)

    return g, c, tgraph, t0


def testCarte(p, n=None, carte=0, afficherCarte=False, tempo=100):
    """
    Teste la classe Graph avec une certaine port�e, en suivant la r�partition
    et la taille d'une carte (image BMP)
    Affiche la taille du plus gros cluster, la qualit� de la connection
    et affiche en dernier le graphique avec les clusters repr�sent�s

    Arguments facultatifs:
    n -- (int) Forcer l'esp�rance du nombres de t�l�phone pr�sents en modifiant
    l�g�rement la carte

    carte -- (int) S�lectionner une carte parmi la liste 'cartes' (d�faut = 0)

    afficherCarte -- (bool) Afficher la carte seule dans un graphique � part
    (d�faut = False)
    """
    tempsDepart = perf_counter()
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
          " T�l�phones (" + str(taillePlusGrandCluster * 100 // n) + "%)")

    print("Qualit� de la connexion : " + str(analyseClusters.qualiteConnection(c)))

    tgraph = c.afficherPlotAvecClusters(True)

    t0 = perf_counter() - tempsDepart
    print("Temps total : ", t0)
    util.jingle(tempo)

    return g, c, tgraph, t0


if __name__ == "__main__":
    # Profiling
    import cProfile
    import pstats

    # Start Profiler
    pr = cProfile.Profile()
    pr.enable()

    # Test clusterisation sur une carte
    # t = testCarte(2, 10, carte=3, afficherCarte=True, tempo=0)

    # Test clusterisation sur une distribution random
    t = test(0, 0)

    # Stop profiler and print stats
    pr.disable()
    pr.dump_stats('main.prof')
    # To see results :
    # gprof2dot -f pstats main.prof > main.prof.dot
    # https://dreampuf.github.io/GraphvizOnline/

    ps = pstats.Stats(pr)
    ps.sort_stats('cumulative').print_stats()
