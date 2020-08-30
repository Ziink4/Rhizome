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
    La classe sur quoi tout repose, qui g�n�re la position des t�l�phones
    al�atoirements, et qui �tablit les connexions entre eux

    Arguments facultatifs :
    debug -- (bool) Pr�cise si le programme doit afficher les informations de
    d�bogage durant les calculs (d�faut = False)
    """
    def __init__(self, tailleX, tailleY, n, p, debug=False):
        # On v�rifie qu'il y ait bien au moins un t�l�phone, que la portee
        # ne soit pas nulle et qu'il y ait assez de positions diff�rentes
        if n < 1:
            raise ValueError("Pas de GSM.")
        if p < 1:
            raise ValueError("Port�e nulle.")
        if tailleX * tailleY < n:
            raise ValueError("Trop de GSM ou grille trop petite.")

        # Liste des GSM interconnect�s
        connexions = [[] for i in range(n)]

        tempsDepart = clock()

        # On cr�ee la liste des coordonn�es des GSM (X,Y) avec une bijection
        # de [0, tailleX*tailleY - 1] dans [0, tailleX - 1] x [0, tailleY - 1]
        listeId = enumerate(choice(range(tailleX * tailleY), n, False))
        coord = array(([(k, v % tailleX, v // tailleX) for k, v in listeId]),
                      dtype=[('indice', 'int'), ('x', 'int'), ('y', 'int')])

        t0 = clock() - tempsDepart
        if debug:
            print("G�n�ration : ", t0)

        # On reclasse par x puis par y
        coord.sort(-1, 'heapsort', ['x', 'y'])

        # La liste des coordonn�es est class�e d'abord selon x, on cr�er la
        # liste triParX, qui � un indice x, associe le tuple compos� de
        # l'indice du premier gsm qui a sa premi�re coordon�e sup�rieur ou
        # �gale � x-p, et de l'indice du premier gsm qui a sa premi�re
        # coordonn�e strictement sup�rieure � x+p.
        triParX = []

        for x in range(tailleX):
            triParX.append((searchsorted(coord['x'], x - p),
                            searchsorted(coord['x'], x + p + 1)))

        t1 = clock() - tempsDepart - t0
        if debug:
            print("Tri par X : " + str(clock() - tempsDepart) + \
                  " (" + str(t1) + ")")

        # Cr�ation de la listes des GSM interconnect�s:
        # on �limine d'abord tout les gsm qui sont trop �loign�s sur x � l'aide
        # de triParX, on a alors une bande de gsm possiblement connect�s, on
        # fait en suite de m�me pour y, on obtient un carr�. On v�rifie ensuite
        # pour chacun des gsm dans le carr�, si ils sont dans le cercle de
        # rayon p et de centre (x,y).
        # pp : carr� de la port�e, utilis� pour les cercles
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

        # t3 D�pends de p et de n
        # La courbe est assez particuli�re
        # Cf. http://i.imgur.com/Lo7m3xH.png ou courbe_t3.png
        t2 = clock() - tempsDepart - t1
        if debug:
            print("Tri par Y & Cercle : " + str(clock() - tempsDepart) + \
                  " (" + str(t2) + ")")

        # Surface totale de la zone �tudi�e en m�
        self.surface = float(tailleX * tailleY)

        # tailleX : longueur de l'abscisse de la carte
        self.tailleX = tailleX

        # tailleY : idem pour l'ordonn�e
        self.tailleY = tailleY

        # n : nombre de GSM
        self.n = n

        # p : port�e d'un GSM
        self.p = p

        # Mode d�bogage (True / False)
        self.debug = debug

        self.connexions = connexions

        self.coordXY = deepcopy(coord)

        coord.sort(-1, 'heapsort', ['indice'])
        self.coord = deepcopy(coord)

        self.distancesVoisins = [[(sqrt((coord[gsm][1] - coord[gsm2][1])**2 +
                                        (coord[gsm][2] - coord[gsm2][2])**2),
                                   gsm2) for gsm2 in connexions[gsm]]
                                 for gsm in range(n)]

        # La courbe a la m�me forme que celle de t3
        t3 = clock() - tempsDepart - t2
        self.temps = (t0, t1, t2, t3)
        if debug:
            print("Fin du __init__ : " + str(clock() - tempsDepart) + \
                  " (" + str(t3) + ")")

    def afficherPlot(self, taillePoints=None):
        """
        Affiche les points de l'objet Graph avec des couleurs "al�atoires"

        Arguments facultatifs :
        taillePoints -- (int) Pour for�er la taille des points affich�s
        Si rien n'est fourni, la taille des points est automatiquement calcul�e
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
        Impl�mentation de l'algorithme de Dijkstra pour trouver le chemin le
        le plus court entre deux t�l�phones donn�s

        Arguments facultatifs:

        courbePuissance -- (fonction) Pour sp�cifier la distinction entre
        plusieurs t�l�phones A et B dans le m�me cercle que le t�l�phone C
        on applique courbePuissance � la distance entre C et A, et entre C et B
        On peut ainsi mod�liser une perte de d�bit par exemple en fonction de
        la distance. Par d�faut, la fonction est contante et �gale � 1, c'est �
        dire que l'algorithme ne fera aucune diff�rence entre A et B m�me si B
        est � 1mm de vous et B � 1m. (d�faut = lambda x: 1)
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
            raise Exception("Non reli�s !")

        t0 = clock() - tempsDepart
        if self.debug:
            print("G�n�ration de l'arbre : ", t0)

        while x != gsmDepart:
            x = p[x]
            path.insert(0, x)

        t1 = clock() - tempsDepart - t0
        if self.debug:
            print("Parcours de l'arbre : " + str(clock() - tempsDepart) + \
                  " (" + str(t1) + ")")

        return d[gsmArrivee], path, (t0, t1)


# GraphCarte h�rite de la classe Graph
# Meme si l'__init__ est diff�rent
# Les autres fonctions (plot, dijkstra) ne changent pas
class GraphCarte(Graph):
    """
    On lit une image, pour la consid�rer comme une carte,
    et de g�nerer les points en accord avec les densit�s de population des
    diff�rents zones de la carte, r�present�s par des couleurs.

    Pour ce faire, on lit une image bmp 24bits, moins lourde que en png car
    c'est cod� sur des uint8 au lieux de float32. Chaque pixel correspond �
    un carr� de longueur unit�, et poss�de une certaine probabilit� d'avoir
    un gsm, caract�ris�e par la luminance de sa couleur.

    ATTENTION : le [0][0] est en haut � gauche sur la carte, et en bas � gauche
    sur le graphe il faut changer les axes:
    (ce qui est lu/ce qui doit �tre compris)
        -X ---> -Y
        -Y ---> X

    Le param�tre n permet de sp�cifier le nombre th�orique de GSM :
    on fait la somme de toute les probabilit�s de pr�sences des GSM, puis on
    corrige chaqune par un coeff multiplicatif k tel que : sum*k == n

    Arguments facultatifs :
    debug -- (bool) Pr�cise si le programme doit afficher les informations de
    d�bogage durant les calculs (d�faut = False)

    n -- (int) Forcer l'esp�rance du nombre de t�l�phone pr�sents en modifiant
    l�g�rement la carte
    """

    def __init__(self, p, nomCarte, n=None, debug=False):
        # On v�rifie que la port�e ne soit pas nulle
        if p < 1:
            raise ValueError("Port�e nulle.")

        tempsDepart = clock()

        tcarte = -1

        # On d�duit de la carte les param�tres:
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

        # On cr�e la liste des coordonn�es des GSM (X,Y),
        # en fonction de la carte
        coord = []
        i = 0

        # Pour tous les points de la carte, on fait un jet de d�s � 256 faces
        # pour d�terminer si il y a un GSM
        # en tenant compte de la densit� de population de la zone
        for X in range(tailleX):
            for Y in range(tailleY):
                if randint(255) >= carte[X][Y][0]:
                    # On fait faire une rotation de pi/2 aux coordon�es pour
                    # respecter l'orientation de la carte
                    coord.append((i, Y, tailleX - X - 1))
                    i += 1

        coord = array((coord),
                      dtype=[('indice', 'int'), ('x', 'int'), ('y', 'int')])

        # On a invers� les coordon�es pour respecter l'orientation de la carte,
        # il faut aussi �changer les tailles
        tailleX, tailleY = tailleY, tailleX

        # Le nombre de GSM n'est plus d�termin� du fait de l'approche
        # probabiliste de la r�partition des GSM
        n = len(coord)

        # Liste des GSM interconnect�s
        connexions = [[] for __ in range(n)]

        t0 = clock() - tempsDepart
        if debug:
            print("G�n�ration : ", t0)

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

        # Cr�ation de la listes des GSM interconnect�s
        # pp : carr� de la port�e, utilis� pour les cercles
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

        # Surface totale de la zone �tudi�e en m�
        self.surface = float(surface)

        # tailleX : longueur de l'abscisse de la carte
        self.tailleX = tailleX

        # tailleY : idem pour l'ordonn�e
        self.tailleY = tailleY

        # n : nombre de GSM
        self.n = n

        # p : port�e d'un GSM
        self.p = p

        # Mode d�bogage (True / False)
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
