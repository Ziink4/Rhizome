# -*- coding: latin-1 -*-
"""
Created on Fri Oct 10 13:33:17 2014

@author: Florian, Hippolyte
"""
from hashlib import sha1


class GSM(object):
    """
    Classe représentant un téléphone, avec son IMEI (identifiant unique),
    la liste des messages qu'il a en mémoire, ainsi que des compteurs de
    données entrantes et sortantes
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
    Classe représentant un message, caractérisé par un identifiant unique
    (Hash SHA-1), un numéro (IMEI) d'expéditeur, de destinataire,
    la date (tick) a laquele le message a été créé, ainsi que son contenu

    Arguments facultatifs :
    contenu -- (str) Précise si le message doit avoir un contenu spécifique
    (défaut = '')
    """
    def __init__(self, expediteur, destinataire, tick, contenu=''):
        self.expediteur = expediteur
        self.destinataire = destinataire
        self.contenu = contenu
        self.tick = tick
        # SHA-1 : Fonction de hashage conçue par la NSA
        # On peut trouver une collision en 2 ** 80 opérations
        # TL;DR : IT'S (more than 99.9999999%) SAFE
        self.hash = sha1(str(expediteur) + str(destinataire) + str(tick) +
                         str(contenu)).hexdigest()

    def __repr__(self):
        return repr((self.expediteur, self.destinataire, self.tick,
                     self.contenu))

class AR(object):
    """
    Classe représentant un message, caractérisé par un identifiant unique
    (Hash SHA-1), un numéro (IMEI) d'expéditeur, de destinataire,
    la date (tick) a laquele le message a été créé, ainsi que son contenu

    Arguments facultatifs :
    contenu -- (str) Précise si le message doit avoir un contenu spécifique
    (défaut = '')
    """
    def __init__(self, expediteur, contenu, tick):
        self.expediteur = expediteur
        self.destinataire = 0
        self.contenu = contenu
        self.tick = tick
        # SHA-1 : Fonction de hashage conçue par la NSA
        # On peut trouver une collision en 2 ** 80 opérations
        # TL;DR : IT'S (more than 99.9999999%) SAFE
        self.hash = sha1(str(expediteur) + str(destinataire) + str(tick) +
                         str(contenu)).hexdigest()

    def __repr__(self):
        return repr((self.expediteur, self.destinataire, self.tick,
                     self.contenu))