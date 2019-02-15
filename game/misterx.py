from game.player import Player


class MisterX(Player):
    def __init__(self, game, name, blackCards=0, doubleMoveCards=2):
        super().__init__(game, name, busCard=3, taxiCard=4, undergroundCard=3)
        self.blackCards = blackCards  # Black cards hide used transportation method from the detectives
        self.doubleMoveCards = doubleMoveCards  # Can be used to move twice in one turn

    def getOptions(self):
        pass

    def move(self, destination, transport):
        pass

    def decide(self):
        pass
