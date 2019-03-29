from game.game import ScotlandYard

from ai.human import misterx, detective

import display.gui as gui
import ai.random.misterx as randomMrX
import ai.random.detective as randomDetective

import game.util as util
import game.constants as const

import numpy as np
import pickle


class DetectiveState():
    """
    Class to hold detectives' state
    """

    def __init__(self):
        self.detectivepos = []
        self.detectivecards = []
        self.revealcountdown = 0
        self.gamecountdown = 0
        self.possiblemrx = []

    def extractDetState(self, game, coordinates, longest_path):

        for det in game.detectives:
            # normalize coordinates
            self.detectivepos.append([x / longest_path for x in coordinates[det.position]])
            self.detectivecards.append([det.cards['underground'] / 4, det.cards['bus'] / 8, det.cards['taxi'] / 11])

        # Reveal countdown
        revealcountdown = -1
        for i in const.MRX_OPEN_TURNS[:-1]:
            revealcountdown = i - len(game.misterx.history)
            if revealcountdown >= 0:
                break

        # Wanneer de laatste reveal geweest is,
        # wordt de teller altijd op 4 (= maximale tellerwaarde) gezet
        # zodat de detectives altijd de indruk hebben dat de reveal nog ver weg is
        # en dat ze dus moeten blijven jagen op mister X.
        # 4 wordt als maximum genomen zodanig dat genormaliseerd kan worden.
        if revealcountdown < 0:
            revealcountdown = 4

        self.revealcountdown = revealcountdown / 4

        self.gamecountdown = (game.turns - len(game.misterx.history)) / game.turns

        possiblepos = game.board.possibleMisterXPositions()
        onehotvec = np.zeros(game.board.size)
        for i in possiblepos:
            onehotvec[i - 1] = 1
        self.possiblemrx = onehotvec

    def display(self):
        print(f'Detective positions: {self.detectivepos}\nDetective cards: {self.detectivecards}\nReveal countdown: {self.revealcountdown}\nGame countdown: {self.gamecountdown}\nOne hot possible Mr X: {self.possiblemrx}')



"""
Testing:
"""



def initTrainingConstants(coordinate_anchors, gamesize):
    config = util.readConfig('MLsettings.ini')

    SY = ScotlandYard(cfg=config, size=gamesize)

    # load coordinates
    coord = pickle.load(
        open(f"Distances_A{coordinate_anchors}_s{gamesize}.pickle", "rb"))

    # calculate longest path
    longest = 0
    for co in coord:
        if longest < max(co):
            longest = max(co)

    return longest, coord, SY


def main():
    longest_path, coordinates, game = initTrainingConstants(10, 199)

    game.addMisterX(misterx.ExampleAIImplementationMisterX(game=game, name="AI Mister X", blackCards=4))
    # game.addMisterX(randomMrX.ExampleAIImplementationRandomMisterX(name="Random Mr. X", game=game, blackCards=4))
    game.addDetectives([randomDetective.ExampleAIImplementationRandomDetective(idNumber=i, game=game) for i in range(4)])

    game.board.assignStartPositions()
    game.running = True
    game.update()

    detstate = DetectiveState()
    detstate.extractDetState(game, coordinates, longest_path)
    detstate.display()


if __name__ == '__main__':
    main()
