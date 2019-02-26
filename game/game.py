from game.misterx import MisterX
from game.detective import Detective
from game.board import Board

from game.draw import drawGame


class ScotlandYard():
    def __init__(self, size=199, numDetectives=4, visualize=False):
        self.board = Board(size, game=self)
        self.detectives = [Detective(name=f"Detective{i+1}", game=self) for i in range(numDetectives)]
        self.misterx = MisterX(game=self, name="Mister X", blackCards=numDetectives)

        self.visualize = visualize

    def update(self):

        if self.visualize:
            drawGame(self)

        self.misterx.update()
        
        for detective in self.detectives:
            detective.update()
        
        return not self.hasEnded  # Regularly check if game has ended

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
        1) A detective has reached Mr. X's position
        2) Mr.x has no options left because he is surrounded  # TODO: wannneer checken, andere functie best? bord kan NoOptionsError custom throwen
        3) No detective is able to move

        Returns: bool
        """

        if self.misterx.isDefeated:
            return True

        allDetectivesDefeated = True
        for d in self.detectives:
            if d.position == self.misterx.position:
                return True
            if not d.isDefeated:
                allDetectivesDefeated = False

        return allDetectivesDefeated
    