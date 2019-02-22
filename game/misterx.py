from game.player import Player


class MisterX(Player):
    def __init__(self, game, name, blackCards=2, doubleMoveCards=2):
        super().__init__(game, name, busCard=3, taxiCard=4, undergroundCard=3)

        # Black cards hide used transportation method from the detectives
        # 2x cards can be used to move twice in one turn
        self.cards.update({
            'black': blackCards,
            'double': doubleMoveCards,
        })
    
    def __str__(self):
        "Overwite the string method of base class Player for consistency"
        return "Mr. X"
