# -*- coding: utf-8 -*-
"""Classe GUI

Classe permettant de créer l'affichage utilisateur pour tuner les paramètres.
On ne peut pas ouvrir de fichiers dans cette version du programme. Il ouvre
automatiquement le fichier labyrinthe.csv.
Le fichier labyrinthe.csv représente juste un labyrinthe avec :
0 = mur
1 = départ
2 = arrivée
-1 = chemin
-r = la valeur du piège avec r>1
"""

from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *
import labytoet
from QLearning import *


class Controller():
    def __init__(self, root, problem):
        self.root = root
        root.protocol("WM_DELETE_WINDOW", self.quitButtonPressed)
        self.problem = problem
        self.q_learning = QLearning(self.problem)
        self.view = View(self)

    def quitButtonPressed(self):
        self.q_learning.stop()
        self.root.destroy()

    def getExplorationValue(self):
        return self.q_learning.getExplorationValue()

    def setExplorationValue(self, exploration):
        exploration = float(exploration)
        if exploration >= 0 and exploration <= 1:
            self.q_learning.setExplorationValue(exploration)
        else:
            showinfo(title="Error value", message="La valeur de l'importance de l'exploration doit être comprise entre 0 et 1\n \
                0 = Exploitation pure\n1 = Exploration pure")

    def getIterationsValue(self):
        return self.q_learning.getIterationsValue()

    def setIterationsValue(self, iterations):
        iterations = int(iterations)
        if iterations > 0:
            self.q_learning.setIterationsValue(iterations)
        else:
            showinfo(title="Error value", message="Le nombre d'itérations doit être positif")

    def getGammaValue(self):
        return self.q_learning.getGammaValue()

    def setGammaValue(self, gamma):
        gamma = float(gamma)
        if gamma >= 0 and gamma <= 1:
            self.q_learning.setGammaValue(gamma)
        else:
            showinfo(title="Error value", message="Gamma doit être compris entre 0 et 1")

    def getCountState(self):
        return self.q_learning.getCountState()

    def getProblem(self):
        return self.problem

    def getCurrentPosition(self):
        return self.problem.getCurrentPosition()

    def run(self):
        self.q_learning.start()
        self.view.setCellcount(self.getCountState())

    def stop(self):
        self.q_learning.stop()
        self.view.setCellcount(self.getCountState())



class View(Frame):
    def __init__(self, controller):
        self.controller = controller
        self.window = self.controller.root
        # Barre de menu
        self.menuBar = Menu(self.window)
        menu1 = Menu(self.menuBar, tearoff=0)
        menu1.add_command(label="Open...", command=None)
        menu1.add_separator()
        menu1.add_command(label="Quit", command=self.controller.quitButtonPressed)
        self.menuBar.add_cascade(label="File", menu=menu1)
        menu2 = Menu(self.menuBar, tearoff=0)
        menu2.add_command(label="About", command=self.about)
        self.menuBar.add_cascade(label="Help", menu=menu2)
        self.window.config(menu=self.menuBar)

        # Frame
        self.frame = Frame(bd=20)
        self.frame.pack(side=RIGHT, fill=X)

        # Nombre d'itérations
        self.iterationsLabel = Label(self.frame, text="Nombres\nd'itérations")
        self.iterationsLabel.grid(row=0, column=0)
        self.iterationsValue = StringVar()
        self.iterationsValue.set(self.controller.getIterationsValue())
        self.iterationsEntry = Entry(self.frame, textvariable=self.iterationsValue, width=5)
        self.iterationsEntry.grid(row=1, column=0)
        self.iterationsEntry.bind("<Return>", self.setIterationsValue)
        self.iterationsButton = Button(self.frame, text='OK', \
            command=self.setIterationsButton)
        self.iterationsButton.grid(row=1, column=1)

        # Paramètre gamma
        self.gammaLabel = Label(self.frame, text="Gamma")
        self.gammaLabel.grid(row=2, column=0)
        self.gammaValue = StringVar()
        self.gammaValue.set(self.controller.getGammaValue())
        self.gammaEntry = Entry(self.frame, textvariable=self.gammaValue, width=5)
        self.gammaEntry.grid(row=3, column=0)
        self.gammaEntry.bind("<Return>", self.setGammaValue)
        self.gammaButton = Button(self.frame, text='OK', \
            command=self.setGammaButton)
        self.gammaButton.grid(row=3, column=1)

        # Paramètre exploration
        self.explorationLabel = Label(self.frame, text="Importance de\nl'exploration")
        self.explorationLabel.grid(row=4, column=0)
        self.explorationValue = StringVar()
        self.explorationValue.set(self.controller.getExplorationValue())
        self.explorationEntry = Entry(self.frame, textvariable=self.explorationValue, width=5)
        self.explorationEntry.grid(row=5, column=0)
        self.explorationEntry.bind("<Return>", self.setExplorationValue)
        self.explorationButton = Button(self.frame, text='OK', \
            command=self.setExplorationButton)
        self.explorationButton.grid(row=5, column=1)

        # Bouton run
        self.runButton = Button(self.frame, text='Run', command=self.controller.run)
        self.runButton.grid(row=6, column=0)
        self.runButton = Button(self.frame, text='Stop', command=self.controller.stop)
        self.runButton.grid(row=6, column=1)

        # Deuxième Frame
        self.frame2 = Frame()
        self.frame2.pack(side=LEFT, fill=X)
        self.setCanvas()

    def setCanvas(self):
        '''
        fonction d'affichage, affiche chaque case du labyrinthe sour forme d'une grille
        cellcount est un dictionaire contenant les compteurs de parcours de chaque etats, pour afficher une trace
        '''
        # Canvas
        self.canv = dict()
        problem = self.controller.getProblem()
        self.laby = problem.laby
        # Taille des cellules du labyrinthe
        t_case = 15
        # Un canvas par case du labyrinthe
        for i, v in enumerate(enumerate(self.laby)):
            for j, e in enumerate(v[1]):
                self.canv[i,j]=Canvas(self.frame2, width=t_case, height=t_case, highlightthickness=0)
                self.canv[i,j].grid(row=i, column=j)
                if e<-1 and not (i,j) in problem.debut:
                    #marque les cases piégées par leur poid
                    self.canv[i,j].create_text(t_case/2,t_case/2,text=repr(int(abs(e))))

        #on note le debut et la fin
        for d in problem.debut:
            self.canv[d].create_text(t_case/2,t_case/2,text='D')
        for f in problem.fin:
            self.canv[f].create_text(t_case/2,t_case/2,text='A')


        self.cellcount = self.controller.getCountState()

        #lance le refraichissement de lu labyrinthe
        self.frame2.after(20, self.refresh)

    def setCellcount(self, cellcount):
        self.cellcount = cellcount


    def refresh(self):
        '''
        colore les cases du labyrinthe selon leur valeur et nombre de parcours
        rouge pour les pieges
        noir pour les murs
        blanc pour les cases normales
        trace des cases visitees verte
        '''
        m = max(1, max(self.cellcount.values()))
        for i, v in enumerate(enumerate(self.laby)):
            for j, e in enumerate(v[1]):
                g=255*(e!=0)#rend les murs noir et le reste vert
                b=g-self.cellcount[i,j]*255.0/m #rend les cases plus ou moins blanches selon leur nombre de parcours
                r=b
                if e<-1:#rend les pièges rouges
                    g-=180
                    b-=120

                #les canvas prennent un format type #RRGGBB pour la couleur
                self.canv[i,j]['bg']='#{:02X}{:02X}{:02X}'.format(*[max(int(r), 0), max(int(g), 0), max(int(b), 0)])

        self.canv[self.controller.getCurrentPosition()]['bg']='blue' #affiche la position courante en bleue
        self.frame2.after(20, self.refresh)

    def invalidFile(self):
        showerror("Error Opening File", "Cannot open the file: It is an incompatible type of labyrinth")

    def about(self):
        showinfo("About", "Projet QLearning\nVersion " + __version__ + "\n(C) " + __author__)

    def setGammaValue(self, event):
        self.controller.setGammaValue(event.widget.get())
        self.gammaValue.set(self.controller.getGammaValue())

    def setIterationsValue(self, event):
        self.controller.setIterationsValue(event.widget.get())
        self.iterationsValue.set(self.controller.getIterationsValue())

    def setExplorationValue(self, event):
        self.controller.setExplorationValue(event.widget.get())
        self.explorationValue.set(self.controller.getExplorationValue())


    def setIterationsButton(self):
        self.controller.setIterationsValue(self.iterationsEntry.get())

    def setGammaButton(self):
        self.controller.setGammaValue(self.gammaEntry.get())

    def setExplorationButton(self):
        self.controller.setExplorationValue(self.explorationEntry.get())


def main():
    # Fenêtre d'affichage
    root = Tk()
    root.title('Projet QLearning')
    root.resizable(width=False,height=False)

    # Problème donné
    lab = labytoet.Labyrinth("labyrinthe.csv")

    app = Controller(root, lab)
    root.mainloop()


if (__name__ == '__main__'):
    main()
