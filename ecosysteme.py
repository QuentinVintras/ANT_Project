# -*- coding: utf-8 -*-

import numpy as np
from numpy.random import randint
import time
import matplotlib.pyplot as plt
from animal import Fourmi

"""
Ce module contient la définition de la classe principale servant à gérer le jeu
"""
        
class Ecosysteme(list):
    """
    Classe gérant le déroulement du jeu. 
    """
    def __init__(self, nb_ins, nbt, nbNour, xmax, ymax):
        self.__xmax = xmax
        self.__ymax = ymax
        self.__plateau = []
        self.list_nour = []
        for i in range(xmax):
            self.__plateau.append([0]*ymax)
        self.nbtour =  nbt
        for i in range(nb_ins):
            self.append(Fourmi(randint(0, xmax), randint(0, ymax), self))
        if nbNour>xmax*ymax:
            raise(ValueError("Trop de nourriture"))
        else:
            x = randint(xmax)
            y = randint(ymax)
            for i in range(nbNour):
                while self.case(x,y) == 1:
                    x = randint(xmax)
                    y = randint(ymax)
                self.__plateau[x][y] = 1
                self.list_nour.append((x,y))

    @property
    def dims(self):
        """
        Renvoie les dimensions du plateau de jeu
        """
        return (self.__xmax, self.__ymax)

    def case(self, x, y):
        return self.__plateau[x][y]

    def vue(self, x, y, r):
        xmin = max(0, x-r)
        xmax = min(self.__xmax, x+r+1)
        ymin = max(0, y-r)
        ymax = min(self.__ymax, y+r+1)
        v = []
        for i in range(xmin, xmax):
            v.append(self.__plateau[i][ymin:ymax])
        return v, xmin, ymin


    def nbs(self):
        nbc = 0
        nbf = 0
        for ins in self:
            if ins.car()=='C':
                nbc += 1
            elif ins.car()=='F':
                nbf += 1
        return nbc, nbf
    
    def unTour(self):
        """
        Effectue toutes les actions liées à un tour de jeu.
        
        Paramètres
        ----------
        Aucun
        
        Renvoie
        -------
        Rien
        """
        for ins in self:  # fonctionne car Ecosysteme descend de list
            ins.bouger()
            ins.manger()
        self.enterrer()

    def enterrer(self):
        morts = []
        for ins in self:
            if ins.sante==0:
                morts.append(ins)
        for ins in morts:
            self.remove(ins)
            
    def simuler (self):
        """
        Contrôle l'évolution du jeu, affiche le résultat de chaque tour dans
        un terminal.
        
        Paramètres
        ----------
        Aucun

        Renvoie
        -------
        Rien  
        """
        liste_cig = []
        liste_fou = []
        for t in range(self.nbtour):
            print("### Tour %i ###"%(t))
            self.unTour()
            #print(self)
            nbc, nbf = self.nbs()
            print("Cigales {}\tFourmis {}\t".format(nbc, nbf))



if __name__ == "__main__":
    nbins = 300
    nbtour = 150
    ecosys = Ecosysteme(nbins,nbtour,80,30,40)
    print(ecosys)
    ecosys.simuler()
