from game.detective import Detective
import random


class ExampleAIImplementationRandomDetective(Detective):
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
        print(self.id)
        return decision[0], decision[1]
