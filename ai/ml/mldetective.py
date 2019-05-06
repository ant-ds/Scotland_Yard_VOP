from game.detective import Detective
from game.misterx import MisterX
from ai.ml.mlutils import chooseAction, chooseActionMrX
from detectivestate import DetectiveState, MrXState
import tensorflow as tf       


class AIModelDetective(Detective):
    def __init__(self, modelname=None, longest_path=10, coordinates=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.longest_path = longest_path
        self.coordinates = coordinates
        self.nextaction = []
        self.model = None
        if modelname is not None:
            self.model = tf.keras.models.load_model(modelname)

    def decide(self):
        # look up other detectives
        # choose actions for all detectives
        # assign actions to other detectives
        # return own chosen action
        idxFirstAlive = min([i for i, det in enumerate(self.game.detectives) if not det.defeated])
        if self.game.detectives[idxFirstAlive] != self:
            if self.nextaction[1] is None:
                return None, None
            else:
                return self.nextaction
        else:
            for i, det in enumerate(self.game.detectives):
                det.nextaction, _ = chooseAction(self.model, self.game.board.getOptions(det, doubleAllowed=False), DetectiveState().extractDetState(self.game, i), 0, self.longest_path, self.coordinates)
            if self.nextaction[1] is None:
                return None, None
            else:
                return self.nextaction


class AIModelMisterX(MisterX):
    def __init__(self, modelname=None, longest_path=10, coordinates=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.longest_path = longest_path
        self.coordinates = coordinates
        self.model = None
        if modelname is not None:
            self.model = tf.keras.models.load_model(modelname)

    def decide(self):
        nextaction, _ = chooseActionMrX(self.model, self.game.board.getOptions(self, doubleAllowed=False), MrXState().extractMrXState(self.game), 0, self.longest_path, self.coordinates)
        return nextaction
