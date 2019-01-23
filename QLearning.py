# -*- coding: utf-8 -*-
"""Classe QLearning

Classe permettant d'utiliser l'algorithme QLearning.
Cette classe est un thread qui tourne en arrière plan pour résoudre un problème donné
"""
from random import shuffle, randint
import labytoet
from threading import Thread
from time import sleep
from math import exp

class QLearning(Thread):
    def __init__(self, problem, iterations=3000, gamma=1, exploration=0.6):
        """
        Prend un problème en paramètre.
        """
        Thread.__init__(self)
        self.iterations = iterations
        self.exploration = exploration
        self.problem = problem
        self.gamma = gamma
        self.terminated = False

        # Initialisation du dictionnaire Q
        self.Q = self.problem.etats.fromkeys(self.problem.etats.keys(), dict())
        for i in self.Q:
            self.Q[i] = dict(zip(range(len(self.problem.etats[i])), [0] * len(self.problem.etats)))

        self.countAction = dict()
        self.countState = self.problem.etats.fromkeys(self.problem.etats.keys(), 0)
        #Thread(target=self.run).start()
        #self.problem.afficher(self.countState)

    def run(self):
        """
        Fonction pour lancer le thread
        """
        #for i in range(self.iterations):
        i = self.iterations
        while(i!=0 and not self.terminated):
            s=self.problem.setInitialState()

            self.countState[s] += 1

            while not self.problem.isGoal():
                if self.terminated:
                    break
                sleep(0.0001)
                a = self.getAction(s)
                self.countAction[(s, a)] = self.countAction.get((s, a), 0) + 1

                r = self.problem.action(a)
                new_s=self.problem.getCurrentPosition()

                self.Q[s][a] = r + self.gamma * max(self.Q[new_s].values())

                s = new_s
                self.countState[s] += 1
            i -= 1
        QLearning.__init__(self, self.problem)


    def getAction(self, s):
        """
        Choisit une action parmi ceux qui sont possibles suivant une startégie.
        Par défaut, la fonction opère plus d'exploration que d'exploitation avec une loi exponentielle :
        au départ, beaucoup d'exploration pour converger par la suite que sur de l'exploitation
        """
        somme = 0
        for i in self.problem.fin:
            somme += self.countState[i]
        return max(self.Q[s], key=lambda i:\
            (1-self.exploration)*self.Q[s][i] \
            - self.exploration*self.countAction.get((s, i), 0)*exp(-somme/(len(self.problem.fin)*10)))


    def stop(self):
        """
        Permet d'arrêter le thread en cours d'exécution
        """
        self.terminated = True

    def getIterationsValue(self):
        return self.iterations

    def setIterationsValue(self, iterations):
        self.iterations = iterations

    def getGammaValue(self):
        return self.gamma

    def setGammaValue(self, gamma):
        self.gamma = gamma

    def getExplorationValue(self):
        return self.exploration

    def setExplorationValue(self, exploration):
        self.exploration = exploration

    def getCountState(self):
        return self.countState
