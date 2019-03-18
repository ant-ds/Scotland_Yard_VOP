from game.detective import Detective
from game.board import Board
from game.game import ScotlandYard
import game.constants as const
import networkx as nx

from operator import itemgetter
import random

class ExampleAIImplementationDetective(Detective):
    
    #static variables
    futureNodes = [] # List of lists of future nodes for every detective
    futureTransports = [] # List of lists of used transports for these nodes
    options = [] # List of lists of options for every detective
    
    def __init__(self, *args, **kwargs):
        self.trn = 1
        super().__init__(*args, **kwargs)

    def decide(self):
        print("#####---DETECTIVE AI RUNNING---#####")
        
        # Determine turn
        self.trn = len(self.game.misterx.history)-1
        print(f"Current Turn: {self.trn}")

        # Initialize static variables correctly
        if self.trn == 1 and self.id == 0:
            for detective in self.game.detectives:
                self.futureNodes.append([])
                self.futureTransports.append([])

        disperseTurns = [1,2,3]
        closeinTurns = [4,8,13,18,24] # TOCHECK: when is mrx revealed
        encircleTurns = [5,6,7,9,10,11,14,15,16,19,20,21,22,23]
        broadenTurns = [12, 17]
        
        if self.id == 0:
            if self.trn in disperseTurns:
                self.disperse()
            elif self.trn in closeinTurns:
                self.closein()
            elif self.trn in encircleTurns:
                self.encircle()
            elif self.trn in broadenTurns:
                self.broaden()
        
        decision = (self.futureNodes[self.id][0],self.futureTransports[self.id][0])
        del self.futureTransports[self.id][0]
        del self.futureNodes[self.id][0]

        print(f"Going to play {decision[1]} from {self.position} to {decision[0]}")
        # input("Press Enter to continue...")
        return decision[0], decision[1]


    def disperse(self):
        print("---Disperse algo---")
        for i in range(0, len(self.game.detectives)):
            decision = self.randomMove(self.game.detectives[i])
            self.futureNodes[i].append(decision[0])
            self.futureTransports[i].append(decision[1])

    def closein(self):
        print("---Close-in algo---")
        for i in range(0, len(self.game.detectives)):
            decision = self.randomMove(self.game.detectives[i])
            self.futureNodes[i].append(decision[0])
            self.futureTransports[i].append(decision[1])

    def encircle(self):
        print("---Encircle algo---")
        for i in range(0, len(self.game.detectives)):
            decision = self.randomMove(self.game.detectives[i])
            self.futureNodes[i].append(decision[0])
            self.futureTransports[i].append(decision[1])

    def broaden(self):
        print("---Broaden algo---")
        for i in range(0, len(self.game.detectives)):
            decision = self.randomMove(self.game.detectives[i])
            self.futureNodes[i].append(decision[0])
            self.futureTransports[i].append(decision[1])

    def randomMove(self, det):
        print("")
        print("~Making random move~")
        options = self.game.board.getOptions(det)
        print(f"Detective: {det.id} at {det.position}, Possible moves: {options}")
        if len(options) == 0:
            return None, None
        decision = random.choice(options)
        print(f"Chosen move: {decision}")
        return decision[0], decision[1]
        