from game.detective import Detective

class AIReinforcementDetective(Detective):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.epsilon = 0
        self.model = None   # Policy network
        self.state = []
        self.latestaction = []
        self.latestQ # ? wat als er een random gekozen werd door epsilon?

    # return node:int, transportation:string
    def decide(self):
        # check epsilon and consider random move
        # get all actions
        # check all Q values through network
        # take action with highest Q