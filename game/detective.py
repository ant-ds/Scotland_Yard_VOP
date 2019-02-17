from game.player import Player


class Detective(Player):
    def __init__(self, game, name):
        super().__init__(game, name, busCard=8, taxiCard=10, undergroundCard=4)

    def getOptions(self):
        pass

    """def move(self, destination, transport):
        pass

    def decide(self):
        pass"""
