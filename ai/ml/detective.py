from game.detective import Detective
import numpy as np
import tensorflow as tf

class AIReinforcementDetective(Detective):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.epsilon = 0
        self.model = None   # Policy network
        self.state = {}
        self.latestaction = []
        self.latestQ # ? wat als er een random gekozen werd door epsilon?

    # return node:int, transportation:string
    def decide(self):
        # get all valid moves
        # check epsilon and consider random move
        # get all actions
        # check all Q values through network
        # take action with highest Q

        chosen_move = []

        valid_moves = self.game.board.getOptions(self, doubleAllowed=False)
        if np.random.uniform() <= self.epsilon:
            chosen_move = valid_moves[np.random.randint(0, len(valid_moves) - 1)]
            self.latestaction = chosen_move
            self.latestQ = self.model.predict
            return chosen_move        
