import game.constants as const

import numpy as np


class DetectiveState():
    """
    Class to hold detectives' state
    """

    def __init__(self):
        self.detectivepos = []  # position of the acting detective
        self.otherpos = []  # positions of other detectives
        self.detectivecards = []    # resources of acting detective
        self.revealcountdown = 0
        self.gamecountdown = 0
        self.possiblemrx = []
        self.defeated = False

    def extractDetState(self, game, idnumber):

        det = game.detectives[idnumber]
        self.detectivepos = det.position
        self.otherpos = [d.position for d in game.detectives if not d.id == idnumber]

        self.detectivecards = [det.cards['underground'] / 4, det.cards['bus'] / 8, det.cards['taxi'] / 11]

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
        self.defeated = det.defeated
        return self

    def display(self):
        print(f'Detective position: {self.detectivepos}\nDetective cards: {self.detectivecards}\nOther detectives: {self.otherpos}\nReveal countdown: {self.revealcountdown}\nGame countdown: {self.gamecountdown}\nOne hot possible Mr X: {self.possiblemrx}')
