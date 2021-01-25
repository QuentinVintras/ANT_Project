# -*- coding: utf-8 -*-

import numpy as np
from numpy.random import randint
import sys
from abc import ABC, abstractmethod

def sign(x):
    if x<0:
        return -1
    elif x==0:
        return 0
    else:
        return 1


# Keep the capacity to add another animal
class Animal(ABC):
    """
    Classe décrivant les comportement par défaut des animaux. Peut-être 
    utilisée en l'état ou sous classée pour définir des comportements de
    déplacement différents.
    """
    def __init__(self, abscisse, ordonnee, eco, capacity=30):
        """
        Crée un animal aux coordonnées désirées.
        
        Paramètres
        ----------
        abscisse, ordonnée: int
            Les coordonnées auxquelles l'animal sera créé.
            
        capacité: int
            niveau de santé maximal de l'animal. Vaut 10 par défaut.
        """
        L = ['Fourmi0.png', 'Fourmi1.png', 'Fourmi2.png', 'Fourmi3.png']
        np.random.shuffle(L)
        self.image_name = L
        self.index_img = 0

        self.__health = randint(capacity//2, capacity)
        self._max = capacity
        self._eco = eco
        self.coords = abscisse, ordonnee

        self.dead = False

        a, b, c, d = np.random.randint(1, 4, 4)
        self.vect = [((-1) ** a) * b / np.sqrt(b ** 2 + d ** 2), ((-1) ** c) * d / np.sqrt(b ** 2 + d ** 2)] # direction de son mvt


    def __str__(self):
        """
        Affiche l'état courant de l'animal.
        
        Paramètres
        ----------
        Aucun
        
        Renvoie
        -------
        s: str
            La chaîne de caractères qui sera affichée via ''print''
        """

        # return "%c : position (%i, %i) etat %i/%i"%(
        #     self.car(), self.x, self.y,
        #     self.health, self._max
        #     )
    
    def car(self):
        """
        Renvoie l'identifiant de l'espèce de l'animal.
        
        Paramètres
        ----------
        Aucun
        
        Renvoie
        -------
        c: str
            Le caractère représentant l'animal.
        """
        return 'A'    

    def eat(self):
        """
        L'animal perd un niveau de health, puis se foodrit s'il se trouve
        sur une case de foodriture. Il affiche "Je meurs de faim" si sa
        health est à 0.
        """
        # print("on est la")
        self.health -= 1

        L = self._eco.list_food
        L1 = self._eco.list_food_name
        l = []
        l1 = []
        dist = 20
        for k in range(len(L)):
            val = L[k]
            if (abs(self.x - val[0]) < dist) and (abs(self.y - val[1]) < dist):
                self.health = self._max

            else:
                l.append(val)
                l1.append(L1[k])
        self._eco.list_food_name = l1
        self._eco.list_food = l

        if self.health<0:
            self.dead = True
        #     print(str(self)+". Je meurs de faim")

    def bouger(self):
        """
        Effectue un mouvement aléatoire (défini dans la superclasse) si 
        health>=3. Essaye de se rapprocher d'une case vers une réserve de
        foodriture sinon.
        """
        if self.dead != True:

            if self.health>=15:
                self.mouvAlea()
            else:
                self.mouvfood()


    def chgt_direction(self):
        """
        On simule l'évolution de sa trajectoire
        """
        a = self.vect[0] + np.random.randint(1,2,1)/10
        b = self.vect[1] + np.random.randint(1,2,1)/10
        self.vect = [a/np.sqrt(a**2 + b**2),b/np.sqrt(a**2 + b**2)]



    def mouvAlea(self): # avec un step de 2
        # self.coords = (self.x+randint(-3,4),
        #                self.y+randint(-3,4))


        self.chgt_direction()
        step = 4
        self.coords = (int(self.x + self.vect[0]*step)
                       ,int(self.y + self.vect[1]*step))


    def mouvfood(self):
        v, xmin, ymin = self._eco.vue(self.x, self.y, 20)
        liste_food = []
        for i in range(len(v)):
            for j in range(len(v[0])):
                if v[i][j] == 1:
                    cx = i+xmin
                    cy = j+ymin
                    d = max(abs(cx-self.x), abs(cy-self.y))
                    liste_food.append((d, cx, cy))
        if liste_food == []:
            self.mouvAlea()
        else:
            np.random.shuffle(liste_food)
            liste_food.sort()
            objx, objy = liste_food[0][1:]
            self.coords = (self.x + sign(objx-self.x),
                           self.y + sign(objy-self.y))

    @property
    def coords(self):
        """
        coords: tuple
            Les coordonnées de l'animal sur le plateau de jeu
        """
        return self.__coords

    @property
    def x(self):
        """
        x: nombre entier
            Abscisse de l'animal
        """
        return self.coords[0]

    @property
    def y(self):
        """
        y: nombre entier
            Abscisse de l'animal
        """
        return self.coords[1]

    @coords.setter
    def coords(self, nouv_coords):
        """
        Met à jour les coordonnées de l'insecte.
        Garantit qu'elles arrivent dans la zone définie par
        l'écosystème self._eco.
    
        Paramètres
        ----------
        Aucun
        """
        x, y = nouv_coords
        x = min(x, self._eco.dims[0]-1)
        x = max(x, 0)
        y = min(y, self._eco.dims[1]-1)
        y = max(y, 0)
        self.__coords = (x, y)

    @property
    def health(self):
        """
        health: float
            Le niveau de santé de l'animal. Si ce niveau arrive à 0 l'animal
            est marqué comme dead et sera retiré du plateau
        """
        return self.__health
    
    @health.setter
    def health(self, value):
        if value <= self._max:
            self.__health = value
        if value <= 0:  # <= car certaines cases enlèvent plus de 1 en santé
            value = 0   # ce qui gèrera les décès plus tard


class Ant(Animal):
    def car(self):
        return 'F'

