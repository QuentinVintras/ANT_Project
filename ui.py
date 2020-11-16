# -*- coding: utf-8 -*-
import sys
from ecosysteme import *
from PyQt5 import  QtGui, QtCore, QtWidgets, uic

class InsectesUI(QtWidgets.QMainWindow):
    """
    Cette classe sert à faire le lien entre l'interface graphique créée
    dans QtDesigner et les mécanismes de jeu de l'écosystème.
    """
    def __init__(self, nb_ins, nb_tour, nb_nour, *args, **kwargs):
        # les paramètres nb_ins, nb_tour et nb_tour sont pour l'instant
        # inutilisés, nous nous en servirons pour créer l'écosystème
        # par la suite. Bien noter que le constructeur peut prendre
        # des paramètre additionnels (nommés ou non) qui sont passés
        # au constructeur de la fenêtre graphique s'ils sont fournis.
    
        # 1ere étape, on appelle le constucteur de la super classe au
        # cas où on aurait voulu lui passer des arguments spécifiques
        # depuis la section __main__. Ce n'est pas le cas ici mais
        # on ne sait jamais de quoi on risque d'avoir besoin dans la
        # suite du projet.
        QtWidgets.QMainWindow.__init__(self, *args)


        # puis on indique à la fenêtre Qt maintenant initialisée qu'elle
        # doit suivre les directives décrites dans QtDesigner et sauvegardées
        # dans le fichier .ui créé à l'étape 1 du sujet.  
        self.ui = uic.loadUi('interface.ui', self)
        self.ecosys = Ecosysteme(nb_ins, nb_tour, 40, 80)
        self.ui.bouton_sim.clicked.connect(self.simuler)


    def simuler(self):
        print("simulation running")
        self.ecosys.simuler()

if __name__ == "__main__":
    # on créé une nouvelle application Qt
    app = QtWidgets.QApplication(sys.argv)
    
    # ici nous passons au constructeur de notre interface de jeu les
    # paramètres nb_ins, nb_tour, nb_nour mais on pourrait aussi
    # faire en sorte de les faire renseigner par l'utilisateur
    # au lancement de l'interface graphique.
    window = InsectesUI(50, 20, 30)
    
    # la fenêtre a été initialisée, tous les callbacks ont éte mis
    # en place (ou plutôt le seront, c'est votre travail), on affiche
    # la fenêtre
    window.show()
    
    # et on lance l'application
    sys.exit(app.exec_())
