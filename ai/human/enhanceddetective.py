from game.detective import Detective
from game.board import Board
from game.game import ScotlandYard
import game.constants as const
import networkx as nx

from operator import itemgetter
import random


class ExampleAIImplementationDetective(Detective):
    
    # static variables
    futureNodes = []  # List of lists of future nodes for every detective
    futureTransports = []  # List of lists of used transports for these nodes
    options = []  # List of lists of options for every detective
    living = []  # Gives first alive detective, needed in decide to make all choices when that detective plays
    varInit = False  # Set to true when all static variables are initisalised in decide. 
    
    def __init__(self, *args, **kwargs):
        self.trn = 1
        super().__init__(*args, **kwargs)

    def decide(self):
        # self.testMetroStartDists(3)
        
        # Determine turn
        self.trn = len(self.game.misterx.history)
        print(f"Current Turn: {self.trn}")

        # Initialize static variables correctly
        if not self.varInit:
            for detective in self.game.detectives:
                self.futureNodes.append([])
                self.futureTransports.append([])
                self.living.append(1)
            self.varInit = True

        disperseTurns = [1, 2]
        closeinTurns = [3, 4, 8, 13, 18, 24]  # TOCHECK: when is mrx revealed
        encircleTurns = [5, 6, 7, 9, 10, 11, 14, 15, 16, 19, 20, 21, 22, 23]
        broadenTurns = [12, 17]
        
        if self.id == self.living.index(1):
            # Generate all options for this turn
            for detective in self.game.detectives:
                # print(f"Options for detective {detective.id}: {self.game.board.getOptions(detective, doubleAllowed=False)}")
                self.options.append(self.game.board.getOptions(detective, doubleAllowed=False))

            if self.trn in disperseTurns:
                self.disperse()
            elif self.trn in closeinTurns:
                self.closein()
            elif self.trn in encircleTurns:
                self.encircle()
            elif self.trn in broadenTurns:
                self.broaden()

        decision = (self.futureNodes[self.id][0], self.futureTransports[self.id][0])
        del self.futureTransports[self.id][0]
        del self.futureNodes[self.id][0]
        if decision == (None, None):
            self.living[self.id] = 0

        print(f"Going to play {decision[1]} from {self.position} to {decision[0]}")
        # input("Press Enter to continue...")
        return decision[0], decision[1]

    def disperse(self):
        print("---Disperse algo---")
        self.metroMove()
        # for i in range(0, len(self.game.detectives)):
        #     decision = self.randomMove(self.game.detectives[i])
        #     self.futureNodes[i].append(decision[0])
        #     self.futureTransports[i].append(decision[1])

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
        # print("~Making random move~")
        options = self.game.board.getOptions(det)
        # print(f"Detective: {det.id} at {det.position}, Possible moves: {options}")
        if len(options) == 0:
            return None, None
        decision = random.choice(options)
        # print(f"Chosen move: {decision}")
        return decision[0], decision[1]
        
##########_TESTS_##########

    def testMetroStartDists(self, dist):
        metrodists = []
        # pospos = possible position
        for pospos in const.START_POSITIONS['detectives']:
            metrodist = []
            for metro in const.METRO_STATIONS:
                if nx.shortest_path_length(self.game.board.graph, metro, pospos) <= dist:
                    metrodist.append([metro, nx.shortest_path_length(self.game.board.graph, metro, pospos)])
            if(len(metrodist) == 0):
                print(f"PROBLEM: No less than {dist} metro for node {pospos}")
            metrodists.append(metrodist)
        print(metrodists)

##########__Metro__##########
    def getMetroDistances(self):
        "Returns list of distance of a player to all metros that are within reach in 3 turns"  # TODO: exclude metros from shortest path (max 1 metro?)
        metrodists = []
        for detective in self.game.detectives:
            # print(detective.position)
            metrodist = []
            for metro in const.METRO_STATIONS:
                pl = nx.shortest_path_length(self.game.board.graph, metro, detective.position)
                if pl <= 3 and pl > 0:
                    metrodist.append([metro, pl])
                    # print(nx.shortest_path(self.game.board.graph, metro, detective.position))
            metrodists.append(metrodist)
            # print(metrodist)
        print(f"Metro's for the detectives: {metrodists}")
        return metrodists

    def assignMetro(self):
        "Assign metro to every detective"  # TODO: don't just take first min, but consider other equal values
        dist = self.getMetroDistances()
        targetMetro = []
        for possibilities in dist:
            targetMetro.append(min(possibilities, key=itemgetter(1)))
        print(f"Target metros for detectives: {targetMetro}")
        return targetMetro

    def metroMove(self):
        "Decides which moves to make for every detective"
        targetMetro = self.assignMetro()

        for i in range(0, len(targetMetro)):
            path = nx.shortest_path(self.game.board.graph, self.game.detectives[i].position, targetMetro[i][0])
            if len(path) > 1: 
                transp = [transport[1] for transport in ExampleAIImplementationDetective.options[i] if transport[0] == path[1]]
            # print(f"transport to test {transp[0]}")
            
            # detective one turn away from a metro station
            if len(path) == 2: 
                # TODO: check if enough transport to do two upcoming moves
                neighbours = self.game.board.getOptions(self.game.detectives[i], customStartPosition=path[1])
                transportToUse = "taxi"
                # print(backforth)
                # print(f"viable taxi positions: {[viable for viable in backforth if viable[1] is transportToUse]} ")
                path.append(random.choice([viable for viable in neighbours if viable[1] is transportToUse])[0])
                transp.append(transportToUse)
                path.append(path[0])
                transp.append(transportToUse)
            
            if len(path) == 4:
                del path[3]

            print(f"Future moves for detective {i}:  {path}")
            self.futureNodes[i] = path[1:]
            self.futureTransports[i] = transp
            print(f"Shortened: {self.futureNodes[i]}")
        return 0
