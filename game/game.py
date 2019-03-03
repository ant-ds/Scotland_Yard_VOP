from game.misterx import MisterX
from game.detective import Detective
from game.board import Board

import game.draw as draw


class ScotlandYard():
    """
    Class with implementation of the strategic boardgame Scotland Yard.
    """
    def __init__(self, size=199, numDetectives=4, visualize=False, verbose=False):
        self.board = Board(size, game=self)
        self.detectives = [Detective(name=f"Detective{i+1}", game=self) for i in range(numDetectives)]
        self.misterx = MisterX(game=self, name="Mister X", blackCards=numDetectives)
        self.turn = 0  # Keep track of turns

        self.visualize = visualize
        self.verbose = verbose

        self.gui = None  # Gui can be added later if a one is available

    def update(self):
        self.turn += 1

        if self.visualize:
            draw.drawGame(self)

        if not self.misterx.update():
            # misterx has been eliminated
            return self.hasEnded()
        
        for detective in self.detectives:
            if not detective.isDefeated:
                detective.update()
        
        return self.hasEnded()  # Regularly check if game has ended

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
    
    def hasEnded(self):
        """
        Checks all parameters that indicate that the game should end
        1) A detective has reached Mr. X's position
        2) Mr.x has no options left because he is surrounded
        3) No detective is able to move

        Returns: bool, statuscode
        """

        allDetectivesDefeated = True
        for d in self.detectives:
            if d.position == self.misterx.position:
                status = 0
                return True, status
            if not d.isDefeated:
                allDetectivesDefeated = False
            
        if allDetectivesDefeated:
            status = -1
            return True, status
        
        if self.misterx.isDefeated:
            status = 1
            return True, status

        return False, None

    def print_(self, msg):
        if self.verbose:
            print(msg)

    def getDrawData(self):
        return draw.drawData(self)
    
    def addGui(self, gui):
        self.gui = gui
