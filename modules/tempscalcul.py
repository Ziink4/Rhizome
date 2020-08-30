# -*- coding: latin-1 -*-
"""
Created on Mon Jun 30 16:11:39 2014

@author: Florian, Hippolyte
"""

from modules.graph import Graph
from time import perf_counter


def simulationsTempsCalcul(tailleX, tailleY, decoupageN, decoupageP,
                           nbSimulations):
    """
    Répète nbSimulation fois une simulation donnée
    """
    tempsDepart = perf_counter()

    for numSimul in range(nbSimulations):
        tempsSimul = simulationTempsCalcul(tailleX, tailleY, decoupageN,
                                           decoupageP)

        print('Simulation n : ' + str(numSimul) + ', durée : ' + \
              str(tempsSimul) + ' s')

    print('Temps total : ' + str(perf_counter() - tempsDepart) + ' s')


def simulationTempsCalcul(tailleX, tailleY, decoupageN, decoupageP):
    """
    Simule une zone de tailleX * tailleY
    Et regardes le temps de génération de cette simulation
    en fonction de n et de p
    """
    tempsDepartSimul = perf_counter()

    f = open(str((tailleX, tailleY, decoupageN.start, decoupageN.stop,
                  decoupageN.step, decoupageP.start, decoupageP.stop,
                  decoupageP.step)) + '.csv', "a")

    for n in decoupageN:
        n = int(n)
        for p in decoupageP:
            p = int(p)
            t0, t1, t2, t3, t4 = Graph(tailleX, tailleY, n, p).temps

            f.write(str(p) + ";" + str(n) + ";" +
                    str(t0).replace(".", ",") + ";" +
                    str(t1).replace(".", ",") + ";" +
                    str(t2).replace(".", ",") + ";" +
                    str(t3).replace(".", ",") + ";" +
                    str(t4).replace(".", ",") + "\n")

        # Affichage de la progression en pourcentage
        print(str((n * 100) // decoupageN.stop) + "%")
    f.close()
    return perf_counter() - tempsDepartSimul
