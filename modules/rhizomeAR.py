# -*- coding: latin-1 -*-
"""
Created on Fri Oct 10 13:49:54 2014

@author: Florian, Hippolyte
"""
from bisect import bisect_left
from numpy.random import rand, randint, normal
from modules.gsm import GSM, Message
from copy import deepcopy
from modules.graph import Graph
from modules.clusters import Clusters
from time import perf_counter


# Taille de la mémoire interne d'un téléphone :
# Capacité 1,000,000 messages de façon a ce que
# la liste des hash se transfèrerapidement
#
# Densité de population : 20,000 hab./km²
# Soit 80000 téléphones pour une zone 2000m x 2000m
# Soit 20000 pout du 1000m x 1000m
def rhizome(graph, listeGsm, proba, ticks=1, capacite=1000000):
    tick = 0
    listeTemps = []
    messagesEnCours = {}
    messagesRecus = []
    messagesCrees = 0
    for i in range(ticks):
        _, _, messagesCrees, tick, temps = etapeRhizome(graph, listeGsm,
                                                        messagesEnCours,
                                                        messagesRecus, proba,
                                                        tick, capacite)
        print('Tick n : ' + str(i + 1) + ', durée : ' + str(temps))
        listeTemps.append(temps)

    return tick, listeTemps, messagesEnCours, messagesRecus, messagesCrees


def etapeRhizome(graph, listeGsm, messagesEnCours, messagesRecus,
                 messagesCrees, proba=0.5, tick=0, capacite=1000000):
    t0 = perf_counter()
    listeProbabilites = rand(graph.n) <= proba
    for gsm in listeGsm:
        gsm.envoyes = 0
        gsm.recus = 0
        if listeProbabilites[gsm.imei]:
            contenu = min(int(normal(65, 16.4)), 0)
            gsm.envoyes += contenu
            nouveauMessage = Message(gsm.imei, randint(0, graph.n),
                                     tick, contenu)
            gsm.messages.append(nouveauMessage)
            messagesEnCours[nouveauMessage.hash] = 1
            messagesCrees += 1
    for gsm in listeGsm:
        for imeiVoisin in graph.connexions[gsm.imei]:
            nouveauxMessages(gsm, listeGsm[imeiVoisin],
                             messagesEnCours, messagesRecus,
                             capacite, tick)
    envoyes = []
    recus = []
    for gsm in listeGsm:
        envoyes.append(gsm.envoyes)
        recus.append(gsm.recus)
    return envoyes, recus, messagesCrees, tick + 1, perf_counter() - t0


def nouveauxMessages(ancienGsm, nouveauGsm, messagesEnCours,
                     messagesRecus, capacite, tick):
    # Suppression des doublons
    anciens = ancienGsm.messages
    nouveaux = nouveauGsm.messages

    # Données envoyées & reçues pour la liste des hash
    l = 40 * len(nouveaux)
    nouveauGsm.envoyes += l
    ancienGsm.recus += l
    hashAnciens = [msg.hash for msg in anciens]
    hashDoublons = [msg.hash for msg in nouveaux if msg.hash in hashAnciens]
    listeSansDouble = [msg for msg in nouveaux if msg.hash not in hashDoublons]

    # Ajout des nouveaux messages, en commencant par les plus récents
    surplus = len(listeSansDouble) + len(anciens) - capacite
    surplus *= (surplus >= 0)

    for messageASuppr in anciens[:surplus]:
        if messageASuppr.hash in messagesEnCours:
            messagesEnCours[messageASuppr.hash] -= 1

    anciens = anciens[:-surplus]
    for nouveauMsg in listeSansDouble:
        position = bisect_left([msg.tick for msg in anciens], nouveauMsg.tick)
        anciens.insert(position, nouveauMsg)
        # Données envoyées & reçues pour la liste des nouveaux messages
        l = nouveauMsg.contenu
        if nouveauMsg.hash in messagesEnCours:
            messagesEnCours[nouveauMsg.hash] += 1

        nouveauGsm.envoyes += l
        ancienGsm.recus += l

    for message in anciens:
        if message.destinataire == ancienGsm.imei:
            # Envoyer l'accusé de Réception
            anciens.remove(message)
            if message.hash in messagesEnCours.keys():
                messagesEnCours.pop(message.hash)
                messagesRecus.append((message, tick - message.tick))

    ancienGsm.messages = anciens


if __name__ == '__main__':
    # Setup (non-profilé) :
    # Test rhizome taille réelle
    # g = Graph(1000, 1000, 20000, 25, True)
    # Test rhizome rapide
    g = Graph(20, 20, 40, 4, True)

    c = Clusters(g, True)
    l = [GSM(k) for k in range(g.n)]
    l2 = deepcopy(l)

    # Profiling
    import cProfile
    import pstats

    # Start Profiler
    pr = cProfile.Profile()
    pr.enable()

    # Simulation
    t = rhizome(g, l, 0.0001, 100)

    # Stop profiler and print stats
    pr.disable()
    pr.dump_stats('rhizomeAR.prof')
    # To see results :
    # gprof2dot -f pstats rhizomeAR.prof > rhizomeAR.prof.dot
    # https://dreampuf.github.io/GraphvizOnline/

    ps = pstats.Stats(pr)
    ps.sort_stats('cumulative').print_stats()
