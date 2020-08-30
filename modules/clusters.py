# -*- coding: latin-1 -*-
"""
Created on Sun Jun 29 15:40:33 2014

@author: Florian, Hippolyte
"""

from copy import deepcopy
from time import perf_counter
from numpy import sort, linspace, array, flipud
from modules.graph import GraphCarte
from matplotlib.markers import MarkerStyle

from scipy.spatial import ConvexHull
import matplotlib.pyplot as plt


class Clusters(object):
    """
    Classe regroupant tout le n�cessaire pour calculer et afficher
    les clusters de connections dans une situation donn�e (un graph donn�)

    Arguments facultatifs:
    debug -- (bool) Pr�cise si le programme doit afficher les informations de
    d�bogage durant les calculs (d�faut = False)
    """

    def __init__(self, graph, debug=False):
        tempsDepart = perf_counter()

        compteur = 0

        connexions = deepcopy(graph.connexions)
        nonConnectes = list(range(len(connexions)))
        clusters = []
        while nonConnectes:
            # Tant que la liste grandit, on on ajoute tout les amis des amis
            nouveauCluster = list(connexions[nonConnectes[0]])
            n1, n2 = 0, 1
            while n2 > n1:
                L2 = []
                for gsm in nouveauCluster:
                    L2 += connexions[gsm]
                    # Compteur pour la complexit�
                    compteur += 1
                nouveauCluster = set(list(nouveauCluster) + L2)
                n1, n2 = n2, len(nouveauCluster)
            # On enl�ve des non connect�s les conn�ct�s
            # O(n)
            for gsm in nouveauCluster:
                nonConnectes.remove(gsm)

            # On augmente la liste finale
            clusters.append(nouveauCluster)

        # On ordonne ltot par taille d�croissante des paquets
        clusters.sort(key=len, reverse=True)

        t = perf_counter() - tempsDepart
        if debug:
            print("S�paration des clusters : ", t)

        self.temps = (t,)

        self.compteur = compteur

        self.clusters = clusters

        self.nclusters = len(clusters)

        self.graph = graph

        self.debug = debug

    def afficherPlotAvecClusters(self, modeZones=None, taillePoints=None):
        """
        Affiche le graphique comportant les points du Graphe, ansi
        que les clusters diff�renci�s par des couleurs et des symboles
        diff�rents

        Arguments facultatifs:
        modeZones -- (True/False/None) Si False, la fonction affiche en plus
        le contour des clusters, si True, la fonction affiche les contours
        et le remplissage, sur None, la fonction se contente d'afficher les
        points (d�faut = None)

        taillePoints -- (int) Pour for�er la taille des points affich�s
        Si rien n'est fourni, la taille des points est automatiquement calcul�e
        pour etre le mieux visible en fonction de la taille en X et en Y
        """
        tempsDepart = perf_counter()
        L = sort(self.graph.coord, kind='heapsort', order=['indice'])
        clusters = self.clusters
        tailleX = self.graph.tailleX
        tailleY = self.graph.tailleY

        plt.close('Graphe')
        plt.figure('Graphe')

        if self.graph.__class__ == GraphCarte:
            plt.imshow(flipud(self.graph.carte), origin='lower')

        plt.grid(True)
        plt.ylim([-1, tailleY])
        plt.xlim([-1, tailleX])

        # Dessin de la bordure de gauche
        plt.plot([0, 0], [0, tailleY - 1], 'r--', lw=2)

        # Dessin de la bordure de droite
        plt.plot([tailleX - 1, tailleX - 1],
                 [0, tailleY - 1], 'r--', lw=2)

        # Dessin de la bordure du haut
        plt.plot([0, tailleX - 1],
                 [tailleY - 1, tailleY - 1], 'r--', lw=2)

        # Dessin de la bordure du bas
        plt.plot([0, tailleX - 1], [0, 0], 'r--', lw=2)

        listeCouleur = plt.cm.Spectral(linspace(0, 1, len(clusters)))

        # La liste des 13 styles de points qui sont "pleins" c'est a dire qui
        # peuvent �tre remplis d'une couleur
        # 'o', 'v', '^', '<', '>', '8', 's', 'p', '*', 'h', 'H', 'D', 'd'
        listeMarkers = MarkerStyle.filled_markers

        # La taille "standard" des points varie entre 10 et 1000, en fonction
        # de la taille de la carte
        if taillePoints is None:
            taillePoints = min(1000, max(10, 2000 / min(tailleX, tailleY)))

        indiceCouleur = 0

        t0 = perf_counter() - tempsDepart
        if self.debug:
            print("Initialisation du graphique : ", t0)

        for bloc in clusters:
            LX = []
            LY = []
            couleur = listeCouleur[indiceCouleur][:3]

            for GSMID in bloc:
                _, x, y = L[GSMID]
                LX += [x]
                LY += [y]

            plt.scatter(LX, LY, marker=listeMarkers[indiceCouleur % len(listeMarkers)],
                        edgecolor=couleur, color=couleur, s=taillePoints)

            if modeZones is not None:
                if len(bloc) == 2:
                    plt.plot([LX[0], LX[1]], [LY[0], LY[1]],
                             color=couleur, ls='--')

                elif len(bloc) >= 3:
                    coord, enveloppe = self.contoursCluster(bloc, ConvexHull)

                    for bord in enveloppe.simplices:
                        plt.plot(coord['x'][bord], coord['y'][bord],
                                 color=couleur, ls='--')

                    if modeZones:
                        plt.fill(coord[enveloppe.vertices]['x'],
                                 coord[enveloppe.vertices]['y'],
                                 color=couleur,
                                 alpha=0.2)

            indiceCouleur += 1
        plt.show()

        t1 = perf_counter() - tempsDepart - t0
        if self.debug:
            print("Remplissage du graphique et affichage : " +
                  str(perf_counter() - tempsDepart) + " (" + str(t1) + ")")

        return t0, t1

    def contoursCluster(self, bloc, fonctionConvexHull):
        """
        Pour un cluster donn�, calcule l'envelloppe convexe autour de ce
        cluster afin de pouvoir afficher le contour
        dans afficherPlotAvecClusters
        """
        coordBloc = [(gsm['x'], gsm['y']) for gsm in self.graph.coord
                     if gsm['indice'] in bloc]

        enveloppe = fonctionConvexHull(coordBloc, qhull_options="QJ Pp")

        return array(coordBloc,
                     dtype=[('x', 'int'), ('y', 'int')]), enveloppe
