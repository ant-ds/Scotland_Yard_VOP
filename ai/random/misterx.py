from game.misterx import MisterX
import random


class ExampleAIImplementationRandomMisterX(MisterX):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # Should return a tuple (destination:int, transportation:string)
    def decide(self):

        # get options
        options = self.game.board.getOptions(self)

        if len(options) == 0:
            return None, None

        # choose random option from options
        decision = random.choice(options)

        if decision[0] == 'double':
            return "double", [decision[1][0], decision[1][1], decision[2][0], decision[2][1]]
        return decision[0], decision[1]
