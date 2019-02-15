from game.misterx import MisterX
from game.detective import Detective


class Game():
    def __init__(self, board=None, numDetectives=4):
        self.board = board
        self.misterx = MisterX(game=self, name="Mister X", blackCards=numDetectives)
        self.detectives = [Detective(name=f"Detective{i+1}", game=self) for i in range(numDetectives)]

    def update(self):
        self.misterx.update()
        for detective in self.detectives:
            detective.update()

            if self.hasEnded:  # Regularly check if game has ended
                return False

    @property
    def hasEnded(self):
        """
        Checks all parameters that indicate that the game should end
        1) Detectives reached Mr. X's position
        2) TODO: others?
        """
        for d in self.detectives:
            if d.position == self.misterx.position:
                return True
        return False
