# -*- coding: utf-8 -*-

import numpy as np
from numpy.random import randint
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
    def __init__(self, abscisse, ordonnee, eco, capacite=30):
        """
        Crée un animal aux coordonnées désirées.
        
        Paramètres
        ----------
        abscisse, ordonnée: int
            Les coordonnées auxquelles l'animal sera créé.
            
        capacité: int
            niveau de santé maximal de l'animal. Vaut 10 par défaut.
        """
        L = ['Fourmi0', 'Fourmi1', 'Fourmi2', 'Fourmi3']
        np.random.shuffle(L)
        self.image_name = L
        self.index_img = 0

        self.__sante = randint(capacite//2, capacite)
        self._max = capacite
        self._eco = eco
        self.coords = abscisse, ordonnee

        self.mort = False

        a, b, c, d = np.random.randint(1, 4, 4)
        self.vect = [((-1) ** a) * b / np.sqrt(b ** 2 + d ** 2), ((-1) ** c) * d / np.sqrt(b ** 2 + d ** 2)] # direction de son mvt
        self.angle = "d"


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
        #     self.sante, self._max
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

    def manger(self):
        """
        L'animal perd un niveau de sante, puis se nourrit s'il se trouve
        sur une case de nourriture. Il affiche "Je meurs de faim" si sa
        sante est à 0.
        """
        # print("on est la")
        self.sante -= 1

        L = self._eco.list_nour
        L1 = self._eco.list_nour_name
        l = []
        l1 = []
        dist = 20
        for k in range(len(L)):
            val = L[k]
            if (abs(self.x - val[0]) < dist) and (abs(self.y - val[1]) < dist):
                self.sante = self._max

            else:
                l.append(val)
                l1.append(L1[k])
        self._eco.list_nour_name = l1
        self._eco.list_nour = l

        if self.sante<0:
            self.mort = True
        #     print(str(self)+". Je meurs de faim")

    @abstractmethod
    def bouger(self):
        """
        À instancier dans les classes filles
        """
        ...
    def chgt_direction(self):
        """
        On simule l'évolution de sa trajectoire
        """
        a = self.vect[0] + np.random.randint(1,2,1)/10
        b = self.vect[1] + np.random.randint(1,2,1)/10
        self.vect = [a/np.sqrt(a**2 + b**2),b/np.sqrt(a**2 + b**2)]

        v1 = self.vect[0]
        v2 = self.vect[1]


        if (abs(v2) < 0.4) and (v1 > 0):
            self.angle = "d"

        if (abs(v2) > 0.4) and (v1 <= 0):
            self.angle = "g"

        if (abs(v1) < 0.4) and (v2 > 0):
            self.angle = "b"

        if (abs(v1) > 0.4) and (v2 <= 0):
            self.angle = "h"


        if (abs(v2) > 0.4) and (abs(v2) < 0.88) and (v1 > 0):
            if v2 > 0:
                self.angle = "db"
            else:
                self.angle = "dh"

        if (abs(v2) > 0.4) and (abs(v2) < 0.88) and (v1 < 0):
            if v2 > 0:
                self.angle = "gb"
            else:
                self.angle = "gh"


    def mouvAlea(self): # avec un pas de 2
        # self.coords = (self.x+randint(-3,4),
        #                self.y+randint(-3,4))


        self.chgt_direction()
        pas = 4
        self.coords = (int(self.x + self.vect[0]*pas)
                       ,int(self.y + self.vect[1]*pas))


    def mouvNour(self):
        v, xmin, ymin = self._eco.vue(self.x, self.y, 20)
        liste_nour = []
        for i in range(len(v)):
            for j in range(len(v[0])):
                if v[i][j] == 1:
                    cx = i+xmin
                    cy = j+ymin
                    d = max(abs(cx-self.x), abs(cy-self.y))
                    liste_nour.append((d, cx, cy))
        if liste_nour == []:
            self.mouvAlea()
        else:
            np.random.shuffle(liste_nour)
            liste_nour.sort()
            objx, objy = liste_nour[0][1:]
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
    def sante(self):
        """
        sante: float
            Le niveau de santé de l'animal. Si ce niveau arrive à 0 l'animal
            est marqué comme mort et sera retiré du plateau
        """
        return self.__sante
    
    @sante.setter
    def sante(self, value):
        if value <= self._max:
            self.__sante = value
        if value <= 0:  # <= car certaines cases enlèvent plus de 1 en santé
            value = 0   # ce qui gèrera les décès plus tard


class Fourmi(Animal):
    def car(self):
        return 'F'
        
    def bouger(self):
        """
        Effectue un mouvement aléatoire (défini dans la superclasse) si 
        sante>=3. Essaye de se rapprocher d'une case vers une réserve de
        nourriture sinon.
        """
        if self.mort != True:

            if self.sante>=4:
                self.mouvAlea()
            else:
                self.mouvNour()

