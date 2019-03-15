from game.player import Player


class Detective(Player):
    def __init__(self, game, idNumber):
        super().__init__(game, f"Detective{idNumber}", busCard=8, taxiCard=10, undergroundCard=4)
        self.id = idNumber
