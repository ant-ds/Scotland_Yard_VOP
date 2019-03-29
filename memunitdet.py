from game.game import ScotlandYard
from ai.human import misterx, detective

import ai.random.misterx as randomMrX
import ai.random.detective as randomDetective

import game.util as util
import game.constants as const

import numpy as np
import pickle

from detectivestate import DetectiveState

class MemUnitDet():
    """
    Class to hold information for 1 training unit
    """
    def __init__(self):
        # current state
        self.currDetState = DetectiveState()

        # action
        self.actionpos = []
        self.actioncards = []   # holds one hot vectors with transport

        # reward
        self.reward = 0

        # next state
        self.nextDetState = DetectiveState()

    def generateData(self, game, coordinates, longest_path):

        # set current state
        self.currDetState.extractDetState(game, coordinates, longest_path)

        ended, statuscode = game.update()

        # assign action





        

        # assign reward (if game didn't end: reward remains 0)
        if ended:
            if statuscode >= 0:
                self.reward = 100
            else:
                self.reward = -100

        # set following state
        self.nextDetState.extractDetState(game, coordinates, longest_path)
        return ended

    def toNNVector(self):
        """
        Returns numpy array with the current detective state and the action
        Can be used as input for the NN
        """
        vec = []

        # detective positions
        for d in self.currDetState.detectivepos:
            for co in d:
                vec.append(co)
        
        # detective cards
        for d in self.currDetState.detectivecards:
            vec.append(d[0])
            vec.append(d[1])
            vec.append(d[2])
        
        # detective reveal, gamecountdown
        vec.append(self.currDetState.revealcountdown)
        vec.append(self.currDetState.gamecountdown)

        # action
        for d in self.actionpos:
            for co in d:
                vec.append(co)
        for d in self.actioncards:
            vec.append(d[0])
            vec.append(d[1])
            vec.append(d[2])

        # convert to numpy array and append possible positions for mrx (= one hot np arr)
        vec = np.array(vec)
        np.append(vec, self.currDetState.possiblemrx)

        return vec