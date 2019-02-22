from game.misterx import MisterX
from game.detective import Detective
from game.board import Board

# from game.draw import drawGame


class ScotlandYard():
    def __init__(self, size, numDetectives=4):
        self.board = Board(size, game=self)
        self.detectives = [Detective(name=f"Detective{i+1}", game=self) for i in range(numDetectives)]
        self.misterx = MisterX(game=self, name="Mister X", blackCards=numDetectives)

    def update(self):

        # drawGame(self)

        self.misterx.update()
        for detective in self.detectives:
            detective.update()

            if self.hasEnded:  # Regularly check if game has ended
                return False
        return True  # If the game is not done, return True so game loop keeps running

    def addMisterX(self, misterx):
        "Overwrite the misterx instance used for playing the game"
        assert(isinstance(misterx, MisterX))
        self.misterx = misterx
    
    def addDetectives(self, detectives):
        "Overwrite the detective instances used for playing the game"
        assert(isinstance(detectives, list))
        for detective in detectives:
            assert(isinstance(detective, Detective))
        self.detectives = detectives
    
    @property
    def hasEnded(self):
        """
        Checks all parameters that indicate that the game should end
        1) Detectives reached Mr. X's position
        2) TODO: others?

        Returns: bool
        """
        for d in self.detectives:
            if d.position == self.misterx.position:
                return True
        return False
    