# -*- coding: latin-1 -*-
"""
Created on Thu Oct 16 18:25:49 2014

@author: Florian, Hippolyte
"""

from modules.rhizome import etapeRhizome
from modules.graph import Graph
from modules.gsm import GSM
from numpy import linspace, mean, median
from ast import literal_eval
from time import perf_counter
from modules.util import Decoupage

import matplotlib.pyplot as plt
import matplotlib.markers as mrk


def simulationsRhizome(tailleX, tailleY, decoupageN, portee, proba, ticks,
                       nbSimulations=1):
    """
    R�p�te nbSimulation fois une simulation donn�e

    Arguments facultatifs:
    nbSimulation -- (int) Pr�cise si le nombre de fois que la simulation doit
    etre r�p�t�e (d�faut = 1)
    """
    tsim = []
    for simulation in range(nbSimulations):
        tsim.append(simulationRhizome(tailleX, tailleY, decoupageN, portee,
                                      proba, ticks)[0])

        print('\n Simulation n : ' + str(simulation + 1) + ', dur�e : ' + \
            str(tsim) + ' s' + '\n')

    return tsim


def simulationRhizome(tailleX, tailleY, decoupageN, portee, proba, ticks):
    """
    Simule une zone de tailleX * tailleY
    Et regardes l'�tat des clusters et de la qualit� de connection
    en fonction de n et de p
    """
    t0sim = perf_counter()
    for n in decoupageN:
        g = Graph(tailleX, tailleY, n, portee, False)
        l = [GSM(k) for k in range(g.n)]
        messagesEnCours = {}
        messagesCrees = 0
        messagesRecus = []
        for i in range(ticks):
            envoyes, recus, messagesCrees, _, _ = etapeRhizome(g, l,
                                                               messagesEnCours,
                                                               messagesRecus,
                                                               messagesCrees,
                                                               proba, i)
            chaine = str((tailleX, tailleY, n, portee, proba, i))
            fichier = open("./simulations/donnees/" + chaine + '.txt', "a")
            fichier.write(str((envoyes, recus)) + '\n')
            fichier.close()
            fichier = open("./simulations/perdus/" + chaine + '.txt', "a")
            fichier.write(str(messagesCrees - len(messagesEnCours) - len(messagesRecus)) + '\n')
            fichier.close()

    return perf_counter() - t0sim, g, l


def statsRhizome(tailleX, tailleY, decoupageN, portee, proba, ticks):
    """
    Ouvre les fichiers correspondant a une s�rie de simulations
    afin d'afficher le graphique
    """
    plt.close(u"Donn�es re�ues moyennes")
    plt.close(u"Donn�es envoy�es moyennes")
    plt.close(u"Donn�es re�ues medianes")
    plt.close(u"Donn�es envoy�es medianes")
    colorMap = plt.cm.Spectral(linspace(0, 1, len(decoupageN)))
    marqueurs = mrk.MarkerStyle.filled_markers
    indiceCouleur = 0
    for n in decoupageN:
        envoye = []
        envoyeMediane = []
        recu = []
        recuMediane = []
        envoyeMax = []
        recuMax = []
        for t in range(ticks):
            envoyeT = []
            recuT = []
            chaine = str((tailleX, tailleY, n, portee, proba, t))
            fichier = open("./simulations/donnees/" + chaine + '.txt', "r")

            data = fichier.readlines()
            for ligne in data:
                envoyeTL, recuTL = literal_eval(ligne)
                envoyeT += envoyeTL
                recuT += recuTL

            envoye.append(mean(envoyeT))
            recu.append(mean(recuT))
            envoyeMediane.append(median(envoyeT))
            recuMediane.append(median(recuT))
            envoyeMax.append(max(envoyeT))
            recuMax.append(max(recuT))

        plt.figure(u"Donn�es envoy�es moyennes")
        plt.plot(range(ticks), envoye, marqueurs[indiceCouleur % 13] + '-',
                 c=colorMap[indiceCouleur], label=str(n))

        plt.figure(u"Donn�es re�ues moyennes")
        plt.plot(range(ticks), recu, marqueurs[indiceCouleur % 13] + '-',
                 c=colorMap[indiceCouleur], label=str(n))

        plt.figure(u"Donn�es envoy�es medianes")
        plt.plot(range(ticks), envoyeMediane,
                 marqueurs[indiceCouleur % 13] + '-',
                 c=colorMap[indiceCouleur], label=str(n))

        plt.figure(u"Donn�es re�ues medianes")
        plt.plot(range(ticks), recuMediane,
                 marqueurs[indiceCouleur % 13] + '-',
                 c=colorMap[indiceCouleur], label=str(n))

        plt.figure(u"Donn�es envoy�es maximum")
        plt.plot(range(ticks), envoyeMax, marqueurs[indiceCouleur % 13] + '-',
                 c=colorMap[indiceCouleur], label=str(n))

        plt.figure(u"Donn�es re�ues maximum")
        plt.plot(range(ticks), recuMax, marqueurs[indiceCouleur % 13] + '-',
                 c=colorMap[indiceCouleur], label=str(n))

        indiceCouleur += 1

    plt.figure(u"Donn�es re�ues moyennes")
    plt.legend(loc=0)
    plt.figure(u"Donn�es envoy�es moyennes")
    plt.legend(loc=0)
    plt.figure(u"Donn�es re�ues medianes")
    plt.legend(loc=0)
    plt.figure(u"Donn�es envoy�es medianes")
    plt.legend(loc=0)
    plt.figure(u"Donn�es re�ues maximum")
    plt.legend(loc=0)
    plt.figure(u"Donn�es envoy�es maximum")
    plt.legend(loc=0)
    plt.show()


if __name__ == "__main__":
    # dN = Decoupage(100, 6600, 100)
    # t0 = simulationRhizome(2000, 2000, dN, 25, 0.3, 300)
    # r = statsRhizome(2000, 2000, dN, 25, 0.0001, 8500)

    # Simulation (tr�s ?) longue
    # dN = Decoupage(20000, 20000, 1)
    # t0, g, l = simulationRhizome(1000, 1000, dN, 25, 0.0001, 50000)
    # r = statsRhizome(1000, 1000, dN, 25, 0.0001, 50000)

    # Simulation rapide (< 3sec)
    dN = Decoupage(40, 40, 1)
    t0, g, l = simulationRhizome(20, 20, dN, 4, 0.0001, 1000)
    r = statsRhizome(20, 20, dN, 4, 0.0001, 1000)

    # Afficher les clusters g�n�r�s par la simulation
    from clusters import Clusters
    c = Clusters(g)
    c.afficherPlotAvecClusters(True)
