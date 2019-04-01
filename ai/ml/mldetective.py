from game.detective import Detective
from ai.ml.mlutils import chooseAction
from detectivestate import DetectiveState
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
        if self.game.detectives[0] != self:
            if self.nextaction[1] is None:
                return None, None
            else:
                return self.nextaction
        else:
            poss_det_action = [self.game.board.getOptions(detective, doubleAllowed=False) for detective in self.game.detectives]
            detstate = DetectiveState().extractDetState(self.game, self.coordinates, self.longest_path)
            actions, _ = chooseAction(self.model, poss_det_action, detstate, 0, self.longest_path, self.coordinates)
            for i in range(0, len(self.game.detectives)):
                self.game.detectives[i].nextaction = actions[i]
            return self.nextaction
