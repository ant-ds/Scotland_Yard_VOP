import numpy as np
import datetime

from game.misterx import MisterX
from game.detective import Detective
from game.board import Board

import game.constants as const
import display.util as util


class ScotlandYard():
    """
    Class with implementation of the strategic boardgame Scotland Yard.
    """
    def __init__(self, size=199, numDetectives=4, cfg=None, proj=''):
        self.board = Board(size, game=self)
        self.detectives = [Detective(name=f"Detective{i+1}", game=self) for i in range(numDetectives)]
        self.misterx = MisterX(game=self, name="Mister X", blackCards=numDetectives)
        self.turn = 0  # Keep track of turns

        self.gui = None  # Gui can be added later if a one is available
        self.config = cfg
        self.proj = proj

    def update(self):
        self.turn += 1

        if self.visualize:
            util.drawGame(self)

        if not self.misterx.update():
            # misterx has been eliminated
            return self.hasEnded()
        
        for detective in self.detectives:
            if not detective.defeated:
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
            if not d.defeated:
                allDetectivesDefeated = False
            
        if allDetectivesDefeated:
            status = -1
            return True, status
        
        if self.misterx.defeated:
            status = 1
            return True, status

        return False, None

    def print_(self, msg):
        if self.verbose:
            print(msg)

    def getDrawData(self):
        return util.drawData(self)
    
    def addGui(self, gui):
        self.gui = gui

    def loop(self):
        stop = False
        while not stop:
            stop, status = self.update()
            pass  # Visualization function calls could be added here
        
        self.statuscode = status
        print(f"Game ended with status {status}::  {const.GAME_END_MESSAGES[status]}")

        self.print_("Saving game data...")

        data = [self.statuscode]
        data.append([self.misterx.history, self.misterx.doubleMoves])
        data.append([det.history for det in self.detectives])
        data = np.array(data)

        curDateTime = datetime.datetime.now()
        filepath = f"history/{self.proj}scly-replay-{curDateTime}"
        for char in [" ", ".", ":", "-"]:
            filepath = filepath.replace(char, "_")
        
        np.save(filepath, data)

        self.print_("Done saving game data.")
    
    @property
    def verbose(self):
        return self.config['OUTPUT'].getboolean('verbose')

    @property
    def visualize(self):
        return self.config['OUTPUT'].getboolean('visualization')
