# -*- coding: latin-1 -*-
"""
Created on Mon Jun 30 11:04:45 2014

@author: Florian, Hippolyte
"""
from time import clock
from numpy import array, searchsorted, linspace, sum
from numpy.random import randint, choice
from heapq import heappush, heappop
from math import sqrt
from copy import deepcopy

import matplotlib.pyplot as plt


class Graph(object):
    """
    La classe sur quoi tout repose, qui génère la position des téléphones
    aléatoirements, et qui établit les connexions entre eux

    Arguments facultatifs :
    debug -- (bool) Précise si le programme doit afficher les informations de
    débogage durant les calculs (défaut = False)
    """
    def __init__(self, tailleX, tailleY, n, p, debug=False):
        # On vérifie qu'il y ait bien au moins un téléphone, que la portee
        # ne soit pas nulle et qu'il y ait assez de positions différentes
        if n < 1:
            raise ValueError("Pas de GSM.")
        if p < 1:
            raise ValueError("Portée nulle.")
        if tailleX * tailleY < n:
            raise ValueError("Trop de GSM ou grille trop petite.")

        # Liste des GSM interconnectés
        connexions = [[] for i in range(n)]

        tempsDepart = clock()

        # On créee la liste des coordonnées des GSM (X,Y) avec une bijection
        # de [0, tailleX*tailleY - 1] dans [0, tailleX - 1] x [0, tailleY - 1]
        listeId = enumerate(choice(range(tailleX * tailleY), n, False))
        coord = array(([(k, v % tailleX, v // tailleX) for k, v in listeId]),
                      dtype=[('indice', 'int'), ('x', 'int'), ('y', 'int')])

        t0 = clock() - tempsDepart
        if debug:
            print("Génération : ", t0)

        # On reclasse par x puis par y
        coord.sort(-1, 'heapsort', ['x', 'y'])

        # La liste des coordonnées est classée d'abord selon x, on créer la
        # liste triParX, qui à un indice x, associe le tuple composé de
        # l'indice du premier gsm qui a sa première coordonée supérieur ou
        # égale à x-p, et de l'indice du premier gsm qui a sa première
        # coordonnée strictement supérieure à x+p.
        triParX = []

        for x in range(tailleX):
            triParX.append((searchsorted(coord['x'], x - p),
                            searchsorted(coord['x'], x + p + 1)))

        t1 = clock() - tempsDepart - t0
        if debug:
            print("Tri par X : " + str(clock() - tempsDepart) + \
                  " (" + str(t1) + ")")

        # Création de la listes des GSM interconnectés:
        # on élimine d'abord tout les gsm qui sont trop éloignés sur x à l'aide
        # de triParX, on a alors une bande de gsm possiblement connectés, on
        # fait en suite de même pour y, on obtient un carré. On vérifie ensuite
        # pour chacun des gsm dans le carré, si ils sont dans le cercle de
        # rayon p et de centre (x,y).
        # pp : carré de la portée, utilisé pour les cercles
        pp = p**2

        for gsm in coord:
            i, x, y = gsm
            carre = coord[triParX[x][0]:triParX[x][1] + 1]

            carre = carre[(carre['y'] >= y - p)]

            carre = carre[(carre['y'] <= y + p)]

            for gsm2 in carre:
                # Si on est dans le cercle
                if (gsm2[1] - x)**2 + (gsm2[2] - y)**2 <= pp:
                    connexions[i].append(gsm2[0])

        # t3 Dépends de p et de n
        # La courbe est assez particulière
        # Cf. http://i.imgur.com/Lo7m3xH.png ou courbe_t3.png
        t2 = clock() - tempsDepart - t1
        if debug:
            print("Tri par Y & Cercle : " + str(clock() - tempsDepart) + \
                  " (" + str(t2) + ")")

        # Surface totale de la zone étudiée en m²
        self.surface = float(tailleX * tailleY)

        # tailleX : longueur de l'abscisse de la carte
        self.tailleX = tailleX

        # tailleY : idem pour l'ordonnée
        self.tailleY = tailleY

        # n : nombre de GSM
        self.n = n

        # p : portée d'un GSM
        self.p = p

        # Mode débogage (True / False)
        self.debug = debug

        self.connexions = connexions

        self.coordXY = deepcopy(coord)

        coord.sort(-1, 'heapsort', ['indice'])
        self.coord = deepcopy(coord)

        self.distancesVoisins = [[(sqrt((coord[gsm][1] - coord[gsm2][1])**2 +
                                        (coord[gsm][2] - coord[gsm2][2])**2),
                                   gsm2) for gsm2 in connexions[gsm]]
                                 for gsm in range(n)]

        # La courbe a la même forme que celle de t3
        t3 = clock() - tempsDepart - t2
        self.temps = (t0, t1, t2, t3)
        if debug:
            print("Fin du __init__ : " + str(clock() - tempsDepart) + \
                  " (" + str(t3) + ")")

    def afficherPlot(self, taillePoints=None):
        """
        Affiche les points de l'objet Graph avec des couleurs "aléatoires"

        Arguments facultatifs :
        taillePoints -- (int) Pour forçer la taille des points affichés
        Si rien n'est fourni, la taille des points est automatiquement calculée
        pour etre le mieux visible en fonction de la taille en X et en Y
        """
        tempsDepart = clock()
        tailleX = self.tailleX
        tailleY = self.tailleY
        coord = self.coord

        plt.close('Graphe')
        plt.figure('Graphe')
        plt.grid(True)
        plt.ylim([-1, tailleY])
        plt.xlim([-1, tailleX])

        # Dessin de la bordure de gauche
        plt.plot([0, 0], [0, tailleY - 1], 'r--', lw=2)

        # Dessin de la bordure de droite
        plt.plot([tailleX - 1, tailleX - 1], [0, tailleY - 1], 'r--', lw=2)

        # Dessin de la bordure du haut
        plt.plot([0, tailleX - 1], [tailleY - 1, tailleY - 1], 'r--', lw=2)

        # Dessin de la bordure de droite
        plt.plot([0, tailleX - 1], [0, 0], 'r--', lw=2)

        # La taille "standard" des points varie entre 10 et 1000, en fonction
        # de la taille de la carte
        if taillePoints is None:
            taillePoints = min(1000, max(10, 2000 / min(tailleX, tailleY)))

        listeCouleur = plt.cm.spectral(linspace(0, 1, self.n))
        LX = []
        LY = []

        t0 = clock() - tempsDepart
        if self.debug:
            print("Initialisation du graphique : ", t0)

        for GSM in coord:
            _, x, y = GSM
            LX += [x]
            LY += [y]

        plt.scatter(LX, LY, c=listeCouleur, edgecolor=listeCouleur,
                    s=taillePoints)

        plt.show()

        t1 = clock() - tempsDepart - t0
        if self.debug:
            print("Remplissage du graphique et affichage : " + \
                  str(clock() - tempsDepart) + " (" + str(t1) + ")")

        return (t0, t1)

    def pathFindingDijkstra(self, gsmDepart, gsmArrivee,
                            courbePuissance=lambda x: 1):
        """
        Implémentation de l'algorithme de Dijkstra pour trouver le chemin le
        le plus court entre deux téléphones donnés

        Arguments facultatifs:

        courbePuissance -- (fonction) Pour spécifier la distinction entre
        plusieurs téléphones A et B dans le même cercle que le téléphone C
        on applique courbePuissance à la distance entre C et A, et entre C et B
        On peut ainsi modéliser une perte de débit par exemple en fonction de
        la distance. Par défaut, la fonction est contante et égale à 1, c'est à
        dire que l'algorithme ne fera aucune différence entre A et B même si B
        est à 1mm de vous et B à 1m. (défaut = lambda x: 1)
        """
        tempsDepart = clock()
        M = set()
        d = {gsmDepart: 0}
        p = {}
        suivants = [(0, gsmDepart)]

        while suivants != []:

            dx, x = heappop(suivants)
            if x in M:
                continue

            M.add(x)

            for w, y in self.distancesVoisins[x]:
                if y in M:
                    continue
                dy = dx + courbePuissance(w)
                if y not in d or d[y] > dy:
                    d[y] = dy
                    heappush(suivants, (dy, y))
                    p[y] = x

        path = [gsmArrivee]
        x = gsmArrivee

        if x not in p.keys():
            raise Exception("Non reliés !")

        t0 = clock() - tempsDepart
        if self.debug:
            print("Génération de l'arbre : ", t0)

        while x != gsmDepart:
            x = p[x]
            path.insert(0, x)

        t1 = clock() - tempsDepart - t0
        if self.debug:
            print("Parcours de l'arbre : " + str(clock() - tempsDepart) + \
                  " (" + str(t1) + ")")

        return d[gsmArrivee], path, (t0, t1)


# GraphCarte hérite de la classe Graph
# Meme si l'__init__ est différent
# Les autres fonctions (plot, dijkstra) ne changent pas
class GraphCarte(Graph):
    """
    On lit une image, pour la considérer comme une carte,
    et de génerer les points en accord avec les densités de population des
    différents zones de la carte, répresentés par des couleurs.

    Pour ce faire, on lit une image bmp 24bits, moins lourde que en png car
    c'est codé sur des uint8 au lieux de float32. Chaque pixel correspond à
    un carré de longueur unité, et possède une certaine probabilité d'avoir
    un gsm, caractérisée par la luminance de sa couleur.

    ATTENTION : le [0][0] est en haut à gauche sur la carte, et en bas à gauche
    sur le graphe il faut changer les axes:
    (ce qui est lu/ce qui doit être compris)
        -X ---> -Y
        -Y ---> X

    Le paramètre n permet de spécifier le nombre théorique de GSM :
    on fait la somme de toute les probabilités de présences des GSM, puis on
    corrige chaqune par un coeff multiplicatif k tel que : sum*k == n

    Arguments facultatifs :
    debug -- (bool) Précise si le programme doit afficher les informations de
    débogage durant les calculs (défaut = False)

    n -- (int) Forcer l'espérance du nombre de téléphone présents en modifiant
    légèrement la carte
    """

    def __init__(self, p, nomCarte, n=None, debug=False):
        # On vérifie que la portée ne soit pas nulle
        if p < 1:
            raise ValueError("Portée nulle.")

        tempsDepart = clock()

        tcarte = -1

        # On déduit de la carte les paramètres:
        carte = plt.imread(nomCarte)

        # carte.shape = (largeur, hauteur, 3)
        tailleX, tailleY, _ = carte.shape

        surface = tailleX * tailleY

        # Conversion Couleur -> Noir et Blanc
        # N = 0.21 R + 0.72 G + 0.07 B (Formule usuelle de la luminance)
        for X in range(tailleX):
            for Y in range(tailleY):
                r, g, b = carte[X][Y][:3]
                g = round(0.21*r + 0.72*g + 0.07*b)
                carte[X][Y][:3] = [g, g, g]

        sommeDensite = surface - (sum(carte) / 765.)

        if n is not None:
            assert surface >= n

            if sommeDensite == 0:
                raise Exception("Cette carte est vierge.")

            nombreBlancs = 0
            sommeAutres = 0
            for X in range(tailleX):
                for Y in range(tailleY):
                    if carte[X][Y][0] == 255:
                        nombreBlancs += 1
                    else:
                        sommeAutres += carte[X][Y][0]

            coeff = -255. * (n + nombreBlancs - surface) / sommeAutres

            for X in range(tailleX):
                for Y in range(tailleY):
                    if carte[X][Y][0] <= 254:
                        carte[X][Y] *= coeff

            self.coeff = coeff

            tcarte = clock() - tempsDepart
            if debug:
                print("Dilatation des couleurs : ", tcarte)

        # On crée la liste des coordonnées des GSM (X,Y),
        # en fonction de la carte
        coord = []
        i = 0

        # Pour tous les points de la carte, on fait un jet de dés à 256 faces
        # pour déterminer si il y a un GSM
        # en tenant compte de la densité de population de la zone
        for X in range(tailleX):
            for Y in range(tailleY):
                if randint(255) >= carte[X][Y][0]:
                    # On fait faire une rotation de pi/2 aux coordonées pour
                    # respecter l'orientation de la carte
                    coord.append((i, Y, tailleX - X - 1))
                    i += 1

        coord = array((coord),
                      dtype=[('indice', 'int'), ('x', 'int'), ('y', 'int')])

        # On a inversé les coordonées pour respecter l'orientation de la carte,
        # il faut aussi échanger les tailles
        tailleX, tailleY = tailleY, tailleX

        # Le nombre de GSM n'est plus déterminé du fait de l'approche
        # probabiliste de la répartition des GSM
        n = len(coord)

        # Liste des GSM interconnectés
        connexions = [[] for __ in range(n)]

        t0 = clock() - tempsDepart
        if debug:
            print("Génération : ", t0)

        # plus besoin d'enlever les doublons, un simple tri suffit
        coord.sort(-1, 'heapsort', ['x', 'y'])

        triParX = []

        for x in range(tailleX):
            triParX.append((searchsorted(coord['x'], x - p),
                            searchsorted(coord['x'], x + p + 1)))

        t1 = clock() - tempsDepart - t0
        if debug:
            print("Tri par X : " + str(clock() - tempsDepart) + \
                  " (" + str(t1) + ")")

        # Création de la listes des GSM interconnectés
        # pp : carré de la portée, utilisé pour les cercles
        pp = p**2.

        for gsm in coord:
            i, x, y = gsm
            carre = coord[triParX[x][0]:triParX[x][1] + 1]

            carre = carre[(carre['y'] >= y - p)]

            carre = carre[(carre['y'] <= y + p)]

            for gsm2 in carre:
                # Si on est dans le cercle
                if (gsm2[1] - x)**2 + (gsm2[2] - y)**2 <= pp:
                    connexions[i].append(gsm2[0])

        t2 = clock() - tempsDepart - t1
        if debug:
            print("Tri par Y & Cercle : " + str(clock() - tempsDepart) + \
                  " (" + str(t2) + ")")

        # Surface totale de la zone étudiée en m²
        self.surface = float(surface)

        # tailleX : longueur de l'abscisse de la carte
        self.tailleX = tailleX

        # tailleY : idem pour l'ordonnée
        self.tailleY = tailleY

        # n : nombre de GSM
        self.n = n

        # p : portée d'un GSM
        self.p = p

        # Mode débogage (True / False)
        self.debug = debug

        self.carte = carte

        self.sommeDensite = sommeDensite

        self.connexions = connexions

        self.coordXY = deepcopy(coord)

        coord.sort(-1, 'heapsort', ['indice'])
        self.coord = deepcopy(coord)

        self.distancesVoisins = [[(sqrt((coord[gsm][1] - coord[gsm2][1])**2 +
                                        (coord[gsm][2] - coord[gsm2][2])**2),
                                   gsm2) for gsm2 in connexions[gsm]]
                                 for gsm in range(n)]

        t3 = clock() - tempsDepart - t2
        self.temps = (tcarte, t0, t1, t2, t3)
        if debug:
            print("Fin du __init__ : " + str(clock() - tempsDepart) + \
                  " (" + str(t3) + ")")
