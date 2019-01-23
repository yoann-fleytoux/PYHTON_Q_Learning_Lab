# -*- coding: utf-8 -*-
"""Classe labytoet

Classe permettant d'initialiser notre probleme pour le QLearning.
Ici, le problème est un labyrinthe
"""


import csv
import os
from tkinter import Tk, Canvas
from random import choice



class Labyrinth(object):
    def __init__(self, labyrinthPath):
        """
        Le chemin passé en paramètre doit être celui d'un fichier csv qui contient:
        0 pour les murs
        -1 pour le chemin
        un nombre négatif pour la pénalité du piège
        1 pour les départs
        2 pour les sorties
        """
        if not os.path.isfile(labyrinthPath):
            raise Exception("Sample path does not exist: " + labyrinthPath)
        self._readLabyrinth(labyrinthPath)
        self._labyToEtat()


    def _readLabyrinth(self, labyrinthPath):
        '''
        fonction d'initialisation,
        lis le fichier csv passe en parametres et le stoque dans laby.
        le cfichier se forme de la maniere suivante:
        ligne 1: coordonnees de depart
        ligne 2: coordonnees d'arrivee
        n*n valeurs des cases du labyrinthe
        '''
        self.laby = list()
        with open(labyrinthPath, 'rt') as csvfile:
            fileReader = csv.reader(csvfile, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
            for row in fileReader: #lis tout le fichier
                self.laby.append(row)
            del fileReader


    def _labyToEtat(self):
        '''
        fonction d'initialisation
        transforme un labyrinthe 'bitmap' en etats pour le qlearning
        un 0 du labyrinthe correspond a un mur, une autre valeur au poid de la case
        les etats sont stoques dans le dictionaire 'etats', ils ont chacun une liste d'etats suivant associes a un poid
        '''
        self.etats=dict()
        self.debut = list()
        self.fin = list()

        #directions possibles a partir d'une case: haut droit bas gauche
        directions={(-1,0),(0,1),(1,0),(0,-1)}

        for i, v in enumerate(enumerate(self.laby)):
            for j, e in enumerate(v[1]):
                for d in directions:
                    self.etats[i+d[0],j+d[1]]=[]

        for i, v in enumerate(enumerate(self.laby)):
            for j, e in enumerate(v[1]):
                if e!=0: #chaque etat se rajoute en tant qu'etat suivant a ses voisins s'il n'est pas un mur
                    if e==2:
                        e=10
                        self.fin.append((i,j))

                    if e == 1:
                        e=-1
                        self.debut.append((i,j))

                    for d in directions:
                        self.etats[i+d[0],j+d[1]].append((e, (i,j)))

        self.current=self.debut[0]


    def setInitialState(self):
        """
        Renvoie un état de départ aléatoirement
        """
        self.current=choice(self.debut)
        return self.current

    def isGoal(self):
        '''
        Retourne True si le l'état courant est dans une position d'arrivée
        '''
        return (self.current in self.fin)

    def getAction(self, state):
        '''
        Renvoie toutes les actions possibles pour un état donné
        '''
        return range(len(self.etats[state]))

    def action(self, action):
        '''
        fais une action et retourne la récompense
        '''
        r=self.etats[self.current][action][0]
        self.current=self.etats[self.current][action][1]
        return r

    def getCurrentPosition(self):
        '''
        Retourne la position courante du robot
        '''
        return self.current
