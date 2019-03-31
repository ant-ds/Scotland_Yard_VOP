from game.detective import Detective

class AIReinforcementDetective(Detective):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nextaction = []

    # return node:int, transportation:string
    def decide(self):
        if self.nextaction[1] is None:
            return None, None
        return self.nextaction        
