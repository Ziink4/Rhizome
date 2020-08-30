# -*- coding: latin-1 -*-
"""
Created on Fri Oct 10 13:33:17 2014

@author: Florian, Hippolyte
"""
from hashlib import sha1


class GSM(object):
    """
    Classe repr�sentant un t�l�phone, avec son IMEI (identifiant unique),
    la liste des messages qu'il a en m�moire, ainsi que des compteurs de
    donn�es entrantes et sortantes
    """
    def __init__(self, imei):
        self.imei = imei
        self.messages = []
        self.envoyes = 0
        self.recus = 0

    def __repr__(self):
        return repr((self.imei, len(self.messages)))


class Message(object):
    """
    Classe repr�sentant un message, caract�ris� par un identifiant unique
    (Hash SHA-1), un num�ro (IMEI) d'exp�diteur, de destinataire,
    la date (tick) a laquele le message a �t� cr��, ainsi que son contenu

    Arguments facultatifs :
    contenu -- (str) Pr�cise si le message doit avoir un contenu sp�cifique
    (d�faut = '')
    """
    def __init__(self, expediteur, destinataire, tick, contenu=''):
        self.expediteur = expediteur
        self.destinataire = destinataire
        self.contenu = contenu
        self.tick = tick
        # SHA-1 : Fonction de hashage con�ue par la NSA
        # On peut trouver une collision en 2 ** 80 op�rations
        # TL;DR : IT'S (more than 99.9999999%) SAFE
        self.hash = sha1(str(expediteur) + str(destinataire) + str(tick) +
                         str(contenu)).hexdigest()

    def __repr__(self):
        return repr((self.expediteur, self.destinataire, self.tick,
                     self.contenu))

class AR(object):
    """
    Classe repr�sentant un message, caract�ris� par un identifiant unique
    (Hash SHA-1), un num�ro (IMEI) d'exp�diteur, de destinataire,
    la date (tick) a laquele le message a �t� cr��, ainsi que son contenu

    Arguments facultatifs :
    contenu -- (str) Pr�cise si le message doit avoir un contenu sp�cifique
    (d�faut = '')
    """
    def __init__(self, expediteur, contenu, tick):
        self.expediteur = expediteur
        self.destinataire = 0
        self.contenu = contenu
        self.tick = tick
        # SHA-1 : Fonction de hashage con�ue par la NSA
        # On peut trouver une collision en 2 ** 80 op�rations
        # TL;DR : IT'S (more than 99.9999999%) SAFE
        self.hash = sha1(str(expediteur) + str(destinataire) + str(tick) +
                         str(contenu)).hexdigest()

    def __repr__(self):
        return repr((self.expediteur, self.destinataire, self.tick,
                     self.contenu))