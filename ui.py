# -*- coding: utf-8 -*-
import sys
from ecosysteme import *
from random import shuffle
from PyQt5 import  QtGui, QtCore, QtWidgets, uic

class InsectesUI(QtWidgets.QMainWindow):
    def __init__(self, nb_ins, nb_tour, nb_nour, *args):
        self.nb_tours = nb_tour
        self.nb_ins = nb_ins
        self.nb_nour = nb_nour
        QtWidgets.QMainWindow.__init__(self, *args)
        self.ui = uic.loadUi('interface.ui', self)
        self.ui.bouton_gen.clicked.connect(self.generer) 
        
        self.ecosys = None

        pixmap = QtGui.QPixmap("arrierPlan.png")
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
        self.ui.bouton_sim.clicked.connect(self.simuler_timer)

        
        #timer pour le bouton simuler
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.un_pas)
        self.generer()
        
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
    def simuler(self):
        """
            Approche bourrin, mieux vaut eviter sinon on peut
            bloquer l'interface graphique
        """
        while self.ecosys.nbtour > 0:
            self.un_pas()
    
    def simuler_timer(self):
        """
            On laisse l'interface faire pour nous les appels
            a un_pas()
        """
        self.timer.start(500) # un tick toutes les 500 ms

    def generer(self):
        if self.timer.isActive:
            self.timer.stop()
        self.ecosys = Ecosysteme(self.nb_ins, self.nb_tours,
                                    self.nb_nour,
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
            if cls_name not in self.img_dict:
                # il faut avoir dans le répertoire les images qui portent le nom
                # de la classe
                self.img_dict[cls_name] = QtGui.QImage(cls_name+".png")
            img = self.img_dict[cls_name]

            # on demande au peintre d'afficher l'image aux coordonnées de l'insecte
            qp.drawImage(ins.x,ins.y, img)
        print(self.ecosys.list_nour)
        for food in self.ecosys.list_nour:
            d,x,y = food
            qp.drawImage(x,y,QtGui.QImage(Nourriture.png))
        # on informe le peintre qu'on a fini
        self.painter.end()




if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = InsectesUI(50, 20, 30)
    window.show()
    sys.exit(app.exec_())
