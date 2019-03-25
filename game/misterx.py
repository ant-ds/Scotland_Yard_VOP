from game.player import Player
import game.constants as const


class MisterX(Player):
    def __init__(self, game, name, blackCards=2, doubleMoveCards=2):
        super().__init__(game, name, busCard=3, taxiCard=4, undergroundCard=3)

        # Black cards hide used transportation method from the detectives
        # 2x cards can be used to move twice in one turn
        self.cards.update({
            'black': blackCards,
            'double': doubleMoveCards,
        })

        self.doubleMoves = []
    
    @property
    def lastKnownPosition(self):
        try:
            idx = max([i - 1 for i in const.MRX_OPEN_TURNS if i - 1 < len(self.history)])
        except ValueError:
            # max from an empty sequence
            return None
        return self.history[idx][-1]

    def __str__(self):
        "Overwite the string method of base class Player for consistency"
        return "Mr. X"

    def cloneFrom(self, old):
        super().cloneFrom(old)
        self.doubleMoves = [m for m in old.doubleMoves]

    def clone(self):
        new = MisterX(self.game, self.name)
        new.cloneFrom(self)
        return new
