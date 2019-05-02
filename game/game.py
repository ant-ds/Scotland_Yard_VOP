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
    def __init__(self, size=199, turns=24, numDetectives=4, cfg=None, proj='', defaultPlayers=False, clone=False):
        self.isclone = clone  # Used in detecting clones, to prevent unnecessary calculations while cloning
        self.board = Board(size, game=self)
        if defaultPlayers:
            self.detectives = [Detective(idNumber=i, game=self) for i in range(numDetectives)]
            self.misterx = MisterX(game=self, name="Mister X", blackCards=numDetectives)
        else:
            self.detectives = []
            self.misterx = None

        self.gui = None  # Gui can be added later if a one is available
        self.config = cfg

        if self.config is not None:
            self.verbose = self.config['OUTPUT'].getboolean('verbose')
            self.visualize = self.config['OUTPUT'].getboolean('visualization')
        else:
            self.verbose = False
            self.visualize = False

        self.timeAtStart = datetime.datetime.now()
        self.proj = proj

        self.run = 0
        self.turns = 24

    def update(self):
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
        if self.run != 0:
            raise RuntimeWarning("Attempting to change a player while the game is running!")
        assert(isinstance(misterx, MisterX))
        self.misterx = misterx

        misterx.game = self  # Guarantee good reverse referencing
    
    def addDetectives(self, detectives):
        "Overwrite the detective instances used for playing the game"
        if self.run != 0:
            raise RuntimeWarning("Attempting to change a player while the game is running!")
        assert(isinstance(detectives, list))
        for detective in detectives:
            assert(isinstance(detective, Detective))
        self.detectives = detectives

        for det in detectives:  # Guarantee good reverse referencing
            det.game = self
    
    def hasEnded(self):
        """
        Checks all parameters that indicate that the game should end
        1) A detective has reached Mr. X's position;            status=0
        2) Mr.x has no options left and cannot move;            status=1
        3) No detective is able to move;                        status=-1
        4) Mister X survived a full game;                       status=-2

        Returns: bool, statuscode

        A statuscode >= 0 is a win for the Detectives, < 0 is a Mister X victory.
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
        
        if len(self.misterx.history) >= self.turns:
            status = -2
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
        """
        Starts the game loop and saves game data when completed.
        """
        self.run += 1  # Increment the counter for each run through the looping sequence
        stop = False
        while not stop:
            stop, status = self.update()
            pass  # Visualization function calls could be added here
        
        self.statuscode = status
        self.print_(f"Game ended with status {status}::  {const.GAME_END_MESSAGES[status]}")

        self.print_("Saving game data...")

        data = [self.statuscode]
        data = np.append(np.array(data), np.array([self.misterx.history, self.misterx.doubleMoves]))
        data = np.append(np.array(data), np.array([det.history for det in self.detectives]))
        data = np.array(data)

        filepath = f"history/{self.proj}scly-replay-{self.timeAtStart}-{self.run}"
        for char in [" ", ".", ":", "-"]:
            filepath = filepath.replace(char, "_")
        
        np.save(filepath, data)

        self.print_("Done saving game data.")

    @property
    def turn(self):
        return len(self.misterx.history)

    def clone(self):
        new = ScotlandYard(size=self.board.size, numDetectives=len(self.detectives), cfg=self.config, clone=True)
        new.addMisterX(self.misterx.clone(game=new))
        new.addDetectives([d.clone(game=new) for d in self.detectives])
        return new

    def reset(self):
        self.board.reset()
        self.misterx.reset()
        # self.detectives[0].reset()
        for det in self.detectives:
            det.reset()
