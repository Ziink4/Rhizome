# -*- coding: latin-1 -*-
"""
Created on Mon Jun 30 16:11:39 2014

@author: Florian, Hippolyte
"""

from numpy import linspace, mean
from modules.clusters import Clusters
from modules.graph import Graph
from time import perf_counter
from ast import literal_eval
from modules.util import Decoupage

import matplotlib.pyplot as plt
import matplotlib.markers as mrk


def qualiteConnection(cluster):
    """
    Retournes la qualité de la connexion globale,
    un float entre 0. et 1.
    """
    resultat = 0
    for bloc in cluster.clusters:
        resultat += len(bloc) ** 2.
    return resultat / (cluster.graph.n ** 2)


def simulationsClusters(tailleX, tailleY, decoupageN, decoupageP,
                        nbSimulations=1):
    """
    Répète nbSimulation fois une simulation donnée

    Arguments facultatifs:
    nbSimulation -- (int) Précise si le nombre de fois que la simulation doit
    etre répétée (défaut = 1)
    """
    tsim = []
    for simulation in range(nbSimulations):
        tsim.append(simulationClusters(tailleX, tailleY,
                                       decoupageN, decoupageP))

        print('Simulation n : ' + str(simulation + 1) + ', durée : ' +
              str(tsim) + ' s')

    return tsim


def simulationClusters(tailleX, tailleY, decoupageN, decoupageP):
    """
    Simule une zone de tailleX * tailleY
    Et regardes l'état des clusters et de la qualité de connection
    en fonction de n et de p
    """
    t0sim = perf_counter()

    for n in decoupageN:
        print(n)
        for portee in decoupageP:
            clusters = Clusters(Graph(tailleX, tailleY, n, portee))
            data = [qualiteConnection(clusters)]
            tailleClusterPrecedent = 0
            i = 0
            for cluster in clusters.clusters:
                tailleCluster = len(cluster)
                if tailleCluster == tailleClusterPrecedent:
                    data[i][1] += 1
                else:
                    data.append([tailleCluster, 1])
                    i += 1
                tailleClusterPrecedent = tailleCluster

            fichier = open("./simulations/clusters/" +
                           str((tailleX, tailleY, n, portee)) + '.txt', "a")

            fichier.write(str(data) + '\n')
            fichier.close()
    return perf_counter() - t0sim


def statsClusters(tailleX, tailleY, decoupageN, decoupageP, dispersion=False):
    """
    Ouvre les fichiers correspondant a une série de simulations
    afin d'afficher les graphiques

    Arguments facultatifs:
    dispersion -- (bool) Précise si le programme doit afficher la totalité des
    points du graphique pour avoir une idée de la dispersion (défaut = False)
    """
    plt.close("Qualité de connection")
    plt.close("Plus grand cluster")
    colorMap = plt.cm.Spectral(linspace(0, 1, len(decoupageP)))
    marqueurs = mrk.MarkerStyle.filled_markers
    indiceCouleur = 0
    for p in decoupageP:
        qualiteConnexion = []
        plusGrosCluster = []
        qualiteConnexionMoyenne = []
        plusGrosClusterMoyenne = []
        abscisse = []
        for n in decoupageN:
            qualiteConnexionN = []
            plusGrosClusterN = []

            fichier = open("./simulations/clusters/" +
                           str((tailleX, tailleY, n, p)) + '.txt', "r")

            data = fichier.readlines()
            for ligne in data:
                ligne = literal_eval(ligne)

                qualiteConnexionN.append(ligne[0])
                plusGrosClusterN.append(ligne[1][0])

                abscisse.append(n)

            fichier.close()

            qualiteConnexionMoyenne.append(mean(qualiteConnexionN))
            plusGrosClusterMoyenne.append(mean(plusGrosClusterN))

            qualiteConnexion += qualiteConnexionN
            plusGrosCluster += plusGrosClusterN

        plt.figure("Qualité de connection")

        if dispersion:
            plt.scatter(abscisse, qualiteConnexion,
                        marker=marqueurs[indiceCouleur % 13],
                        c=colorMap[indiceCouleur])

        plt.plot(decoupageN, qualiteConnexionMoyenne,
                 marqueurs[indiceCouleur % 13] + '-',
                 c=colorMap[indiceCouleur], label=str(p))

        plt.figure("Plus grand cluster")

        if dispersion:
            plt.scatter(abscisse, plusGrosCluster,
                        marker=marqueurs[indiceCouleur % 13],
                        c=colorMap[indiceCouleur])

        plt.plot(decoupageN, plusGrosClusterMoyenne,
                 marqueurs[indiceCouleur % 13] + '-',
                 c=colorMap[indiceCouleur], label=str(p))

        indiceCouleur += 1

    plt.figure("Qualité de connection")
    plt.legend(loc=0)
    plt.figure("Plus grand cluster")
    plt.legend(loc=0)
    plt.show()


def simulationsComplexiteClusters(tailleX, tailleY, decoupageN, decoupageP,
                                  nbSimulations=1):
    """
    Répète nbSimulation fois une simulation donnée

    Arguments facultatifs:
    nbSimulation -- (int) Précise si le nombre de fois que la simulation doit
    etre répétée (défaut = 1)
    """
    tsim = []
    for simulation in range(nbSimulations):
        tsim.append(simulationComplexiteClusters(tailleX, tailleY,
                                                 decoupageN, decoupageP))

        print('Simulation n : ' + str(simulation + 1) + ', durée : ' +
              str(tsim) + ' s')

    return tsim


def simulationComplexiteClusters(tailleX, tailleY, decoupageN, decoupageP):
    """
    Simule une zone de tailleX * tailleY
    Et regardes la complexité de l'algorithme de séparation des clusters
    en fonction de n et de p
    """
    t0sim = perf_counter()

    for n in decoupageN:
        print(n)
        for portee in decoupageP:
            clusters = Clusters(Graph(tailleX, tailleY, n, portee))
            fichier = open("./simulations/clustersComplex/" +
                           str((tailleX, tailleY, n, portee)) +
                           '.txt', "a")

            fichier.write(str(clusters.compteur) + '\n')
            fichier.close()
    return perf_counter() - t0sim


def statsComplexiteClusters(tailleX, tailleY, decoupageN, decoupageP,
                            dispersion=False):
    """
    Ouvre les fichiers correspondant a une série de simulations
    afin d'afficher les graphiques

    Arguments facultatifs:
    dispersion -- (bool) Précise si le programme doit afficher la totalité des
    points du graphique pour avoir une idée de la dispersion (défaut = False)
    """
    plt.close("Compteur")
    plt.figure("Compteur")
    colorMap = plt.cm.Spectral(linspace(0, 1, len(decoupageP)))
    marqueurs = mrk.MarkerStyle.filled_markers
    indiceCouleur = 0

    out = {}

    for p in decoupageP:
        L1 = []
        L1m = []
        abscisse = []
        for n in decoupageN:
            L1N = []

            fichier = open("./simulations/clustersComplex/" +
                           str((tailleX, tailleY, n, p)) + '.txt', "r")

            data = fichier.readlines()
            for ligne in data:
                ligne = literal_eval(ligne)

                L1N.append(ligne)

                abscisse.append(n)

            fichier.close()

            L1m.append(mean(L1N))

            L1 += L1N

        if dispersion:
            plt.scatter(abscisse, L1,
                        marker=marqueurs[indiceCouleur % 13],
                        c=colorMap[indiceCouleur])

        plt.plot(decoupageN, L1m,
                 marqueurs[indiceCouleur % 13] + '-',
                 c=colorMap[indiceCouleur], label=str(p))

        indiceCouleur += 1

        out[p] = L1m

    plt.legend(loc=0)
    plt.show()
    return out


if __name__ == "__main__":
    # Anciennes statistiques sur les tailles
    # des groupes connexes
    # dP0 = Decoupage(10, 25, 1)
    # dN0 = Decoupage(5000, 25000, 1000)
    # t0 = simulationsClusters(2000, 2000, dN0, dP0, 42)
    # statsClusters(2000, 2000, dN0, dP0)

    # Statistiques globales sur la complexité de l'algorithme cluster
    # Par pas de 1000, sur les portées 10-25
    # 5400 scondes pour 1 calcul
    # dP1 = Decoupage(10, 25, 1)
    # dN1 = Decoupage(5000, 25000, 1000)
    # t1 = simulationsComplexiteClusters(2000, 2000, dN1, dP1, 5)
    # out1 = statsComplexiteClusters(2000, 2000, dN1, dP1)

    # Statistiques plus précises pour les portées 16, 20 et 24
    # par pas de 100
    # 8600 secondes pour 1 calcul
    # dP2 = Decoupage(16, 24, 4)
    # dN2 = Decoupage(5000, 25000, 100)
    # t2 = simulationsComplexiteClusters(2000, 2000, dN2, dP2)
    # out2 = statsComplexiteClusters(2000, 2000, dN2, dP2)

    # Statistiques plus précises pour les portées 16, 20, et 24
    # par pas de 10000 pour le comportement asymptotique
    # 1400 secondes pour 1 calcul
    # dP3 = Decoupage(16, 24, 4)
    # dN3 = Decoupage(5000, 105000, 10000)
    # t3 = simulationsComplexiteClusters(2000, 2000, dN3, dP3)
    # out3 = statsComplexiteClusters(2000, 2000, dN3, dP3)

    # Statistiques RAPIDES sur la complexité de l'algorithme cluster
    # N = 20000, P = 16
    dP4 = Decoupage(16, 16, 1)
    dN4 = Decoupage(20000, 20000, 1)
    t4 = simulationsComplexiteClusters(2000, 2000, dN4, dP4)
    out4 = statsComplexiteClusters(2000, 2000, dN4, dP4)
