from game.detective import Detective
from game.misterx import MisterX


class AIReinforcementDetective(Detective):
    # performs gives action

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nextaction = []

    # return node:int, transportation:string
    def decide(self):
        if self.nextaction[1] is None:
            return None, None
        return self.nextaction


class AITrainingMisterX(MisterX):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nextaction = []

    def decide(self):
        if self.nextaction[1] is None:
            return None, None
        return self.nextaction
