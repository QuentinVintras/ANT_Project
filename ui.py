# -*- coding: utf-8 -*-
import sys
from ecosysteme import *
from random import shuffle
from PyQt5 import  QtGui, QtCore, QtWidgets, uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *



class InsectesUI(QtWidgets.QMainWindow):
    def __init__(self, nb_ins, nb_tour, nb_food, *args):
        self.nb_tours = nb_tour
        self.nb_ins = nb_ins
        self.nb_food = nb_food
        QtWidgets.QMainWindow.__init__(self, *args)
        self.ui = uic.loadUi('interface.ui', self)
        self.ui.bouton_gen.clicked.connect(self.generer)


        
        self.ecosys = None

        pixmap = QtGui.QPixmap("arrierPlan1.png")
        pal = QtGui.QPalette()
        pal.setBrush(QtGui.QPalette.Background, QtGui.QBrush(pixmap))
        self.ui.conteneur.lower()
        self.ui.conteneur.stackUnder(self)
        self.ui.conteneur.setAutoFillBackground(True)
        self.ui.conteneur.setPalette(pal)

        # objet "peintre" pour les insectes
        self.painter = QtGui.QPainter()
        # dico pour stocker les images
        self.img_dict={}
        
        # on connecte les signaux de mise à jour du terrain de jeu à la
        # fonction draw_ecosys
        self.ui.conteneur.paintEvent = self.draw_ecosys
        self.ui.bouton_pas.clicked.connect(self.un_pas) 
        self.ui.bouton_sim.clicked.connect(self.simulate_timer)

        
        #timer pour le bouton simuler
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.un_pas)
        self.generer()

        #affichage du nombre de fourmi mortes et vivante
        self.en_vie = self.nb_ins - self.ecosys.dead
        self.morte = self.ecosys.dead

    def ant_num_change(self):
        self.nb_ins = self.ui.ant_num.value()
        
    def un_pas(self):
        if self.ecosys.nbtour > 0:
            self.ecosys.unTour()
            self.conteneur.update()
            self.ecosys.nbtour -= 1
        else:
            if self.timer.isActive:
                self.timer.stop()
            QtWidgets.QMessageBox.question(self, 'Attention !',
                            'Le nombre de tours est épuisé',
                            QtWidgets.QMessageBox.Ok)
    def simulate(self):
        """
            Approche bourrin, mieux vaut eviter sinon on peut
            bloquer l'interface graphique
        """
        while self.ecosys.nbtour > 0:
            self.un_pas()
    
    def simulate_timer(self):
        """
            On laisse l'interface faire pour nous les appels
            a un_pas()
        """
        self.timer.start(100) # un tick toutes les 100 ms

    def generer(self):
        self.nb_tours = self.ui.nb_turns.value()
        self.nb_ins = self.ui.ant_num.value()
        self.nb_food = self.ui.food_num.value()


        if self.timer.isActive:
            self.timer.stop()
        self.ecosys = Ecosysteme(self.nb_ins, self.nb_tours,
                                    self.nb_food,
                                    self.ui.conteneur.width(),
                                    self.ui.conteneur.height()
                                    )
        self.ui.conteneur.update()

#    def draw_ecosys(self, *args):
#        self.painter.begin(self.conteneur)
#        qp = self.painter
#        shuffle(self.ecosys)
#        for ins in self.ecosys:
#            if ins.car() == 'F' :
#               qp.setPen(QtCore.Qt.green)
#               qp.drawRect(ins.x,ins.y, 10,5)
#            else:
#               qp.setPen(QtCore.Qt.red)
#               qp.drawRect(ins.x,ins.y, 10,5)
#       self.painter.end()

    def draw_ecosys(self, *args):
        # on informe le peintre qu'on veut dessiner dans le widget conteneur
        self.painter.begin(self.ui.conteneur)
        # variable intermédiraire pour alléger le code
        qp = self.painter

        # boucle pour parcourir les insectes et gérer les images (vu ci-dessus) 
        for ins in self.ecosys:
            cls_name = ins.__class__.__name__
            if cls_name == "Ant":
                img = QtGui.QImage(ins.image_name[ins.index_img])
                ins.index_img += 1
                if ins.index_img == 3:  # on remet a zéro l'index
                    ins.index_img = 0
                # on demande au peintre d'afficher l'image aux coordonnées de l'insecte
            elif cls_name == "BigAnt":
                img = QtGui.QImage("BigFourmi.png")
            if ins.dead == True:
                img = QtGui.QImage("tombeu.png")

            qp.drawImage(ins.x - 20, ins.y - 20,img)
            qp.drawText(ins.x - 20, ins.y - 20,str(max(ins.health,0)))
            self.en_vie = self.nb_ins - self.ecosys.dead
            self.morte = self.ecosys.dead

            self.ui.vie.display(self.en_vie)
            self.ui.morte_ui.display(self.morte)

            # qp.drawImage(ins.x - 20, ins.y - 20, QtGui.QImage(ins.image[ins.index_img]))


        for k in range(len(self.ecosys.list_food)):
            x,y = self.ecosys.list_food[k]
            # print(self.ecosys.list_food_name[k])
            image = QtGui.QImage(self.ecosys.list_food_name[k])
            qp.drawImage(x, y, image)
            
        # on informe le peintre qu'on a fini
        self.painter.end()




if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = InsectesUI(30, 20, 60) # nb_ins, nb_tour, nb_food,
    window.show()
    sys.exit(app.exec_())
