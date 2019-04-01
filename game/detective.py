from game.player import Player


class Detective(Player):
    def __init__(self, game, idNumber):
        super().__init__(game, f"Detective{idNumber}", busCard=8, taxiCard=10, undergroundCard=4)
        self.id = idNumber
    
    def cloneFrom(self, old):
        super().cloneFrom(old)
        # No extra data to copy

    def clone(self, game=None):
        if game is None:
            game = self.game
        new = type(self)(game, self.id)
        new.cloneFrom(self)
        return new
