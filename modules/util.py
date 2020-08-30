# -*- coding: utf-8 -*-
"""
Created on Wed Sep 10 17:44:36 2014

@author: Florian, Hippolyte
"""
from winsound import Beep
from numpy import linspace, array


def jingle(tempo):
    """
    Joue une mélodie pour prévenir la fin des simulations
    """
    if tempo == 0:
        return

    l = [523, 587, 659]
    d = [(1, 1), (1, 1), (1, 1), (2, 1), (3, 2), (2, 2), (1, 1), (3, 1),
         (2, 1), (2, 1), (1, 2)]
    for note, temps in d:
        Beep(l[note-1], tempo*temps)


class Decoupage(list):
    """
    Une implémentation de la classe list qui permets de regrouper
    les arguments ndebut, nfin, npas en un seul objet.
    """
    def __init__(self, start, stop, step):
        list.__init__(self)
        self.start = start
        self.stop = stop
        self.step = step
        self += list(array(linspace(start, stop, 1 + (stop - start) / step),
                           dtype='int'))
