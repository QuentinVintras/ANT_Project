# -*- coding: utf-8 -*-

import numpy as np
from numpy.random import randint
import time
import matplotlib.pyplot as plt
from animal import Ant

"""
Ce module contient la définition de la classe principale servant à gérer le jeu
"""
        
class Ecosysteme(list):
    """
    Classe gérant le déroulement du jeu. 
    """
    def __init__(self, nb_ins, nbt, nbfood, xmax, ymax):


        self.__xmax = xmax
        self.__ymax = ymax
        self.__plateau = []
        self.list_food = []
        self.list_food_name = []
        self.dead = 0
        for i in range(xmax):
            self.__plateau.append([0]*ymax)
        self.nbtour = nbt
        for i in range(nb_ins):
            self.append(Ant(randint(0, xmax), randint(0, ymax), self))
        if nbfood>xmax*ymax:
            raise(ValueError("Too much food"))
        else:
            x = randint(xmax)
            y = randint(ymax)
            liste_name = ["food0.png","food1.png","food2.png","food3.png"]
            for i in range(nbfood):
                r = int(np.random.randint(0, 4, 1))
                while self.case(x,y) == 1:
                    x = randint(xmax)
                    y = randint(ymax)
                self.__plateau[x][y] = 1
                self.list_food.append((x,y))
                self.list_food_name.append(liste_name[r])


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
            ins.eat()
        self.enterrer()

    def enterrer(self):
        deads = []
        for ins in self:
            if ins.health==0:
                deads.append(ins)
        for ins in deads:
            ins.dead = True
            self.dead += 1
            # self.remove(ins)
            



if __name__ == "__main__":
    nbins = 300
    nbtour = 550
    ecosys = Ecosysteme(nbins,nbtour,80,30,40) #(self, nb_ins, nbt, nbfood, xmax, ymax)
    print(ecosys)
    ecosys.simuler()
