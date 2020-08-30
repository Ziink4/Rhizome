# -*- coding: latin-1 -*-
"""
Created on Fri Oct 10 13:49:54 2014

@author: Florian, Hippolyte
"""
from numpy import searchsorted
from numpy.random import rand, randint, normal
from gsm import GSM, Message
from copy import deepcopy
from graph import Graph
from clusters import Clusters
from time import clock

# Taille de la m�moire interne d'un t�l�phone :
# Capacit� 1,000,000 messages de fa�on a ce que
# la liste des hash se transf�rerapidement
#
# Densit� de population : 20,000 hab./km�
# Soit 80000 t�l�phones pour une zone 2000m x 2000m
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
        print('Tick n : ' + str(i + 1) + ', dur�e : ' + str(temps))
        listeTemps.append(temps)

    return tick, listeTemps, messagesEnCours, messagesRecus, messagesCrees


def etapeRhizome(graph, listeGsm, messagesEnCours, messagesRecus,
                 messagesCrees, proba=0.5, tick=0, capacite=1000000):
    t0 = clock()
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
    return envoyes, recus, messagesCrees, tick + 1, clock() - t0


def nouveauxMessages(ancienGsm, nouveauGsm, messagesEnCours,
                     messagesRecus, capacite, tick):
    # Suppression des doublons
    anciens = ancienGsm.messages
    nouveaux = nouveauGsm.messages

    # Donn�es envoy�es & re�ues pour la liste des hash
    l = 40 * len(nouveaux)
    nouveauGsm.envoyes += l
    ancienGsm.recus += l
    hashAnciens = set([msg.hash for k, msg in enumerate(anciens)])
    hashDoublons = set([msg.hash for k, msg in enumerate(nouveaux)])
    hashDoublons.intersection_update(hashAnciens)
    listeSansDouble = [msg for msg in nouveaux if msg.hash not in hashDoublons]

    # Ajout des nouveaux messages, en commencant par les plus r�cents
    surplus = len(listeSansDouble) + len(anciens) - capacite
    surplus *= (surplus >= 0)

    for messageASuppr in anciens[:surplus]:
        if messageASuppr.hash in messagesEnCours:
            messagesEnCours[messageASuppr.hash] -= 1

    anciens = anciens[:-surplus]
    for nouveauMsg in listeSansDouble:
        position = searchsorted([msg.tick for msg in anciens], nouveauMsg.tick)
        anciens.insert(position, nouveauMsg)
        # Donn�es envoy�es & re�ues pour la liste des nouveaux messages
        l = nouveauMsg.contenu
        if nouveauMsg.hash in messagesEnCours:
            messagesEnCours[nouveauMsg.hash] += 1

        nouveauGsm.envoyes += l
        ancienGsm.recus += l

    for message in anciens:
        if message.destinataire == ancienGsm.imei:
            anciens.remove(message)
            if message.hash in messagesEnCours.keys():
                messagesEnCours.pop(message.hash)
                messagesRecus.append((message, tick - message.tick))

    ancienGsm.messages = anciens

if __name__ == '__main__':
    g = Graph(1000, 1000, 20000, 25, True)
    c = Clusters(g, True)
    l = [GSM(k) for k in range(g.n)]
    l2 = deepcopy(l)
    t0 = clock()
    t2 = rhizome(g, l, 0.0001, 100)
    t1 = clock() - t0
