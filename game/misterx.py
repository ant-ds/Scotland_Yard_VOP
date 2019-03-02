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
    
    def getTransportName(self, transport):
        """Some cards can be used for multiple purposes, but are only kept track of once,
        returns correct internal naming for this player instance"""
        if transport == 'ferry':
            return 'black'
        return transport
    
    @property
    def lastKnownPosition(self):
        lastKnown = None
        for i in const.MRX_OPEN_TURNS:
            try:
                lastKnown = self.history[i][2]  # history has format (start, transport, dest)
            except IndexError:  # once index too high, return last confirmed value
                return lastKnown
        return lastKnown

    def __str__(self):
        "Overwite the string method of base class Player for consistency"
        return "Mr. X"
