import networkx as nx
import itertools

from operator import itemgetter
import random

from game.detective import Detective
from game.board import Board
from game.game import ScotlandYard
import game.constants as const


class ExampleAIImplementationDetective(Detective):
    
    # static variables
    futureNodes = []  # List of lists of future nodes for every detective
    futureTransports = []  # List of lists of used transports for these nodes
    options = []  # List of lists of options for every detective
    living = []  # Gives first alive detective, needed in decide to make all choices when that detective plays
    # varInit = False  # Set to true when all static variables are initisalised in decide. 
    
    def __init__(self, *args, **kwargs):
        self.trn = 1
        super().__init__(*args, **kwargs)

    def decide(self):
        # self.testMetroStartDists(3)
        
        # Determine turn
        self.trn = len(self.game.misterx.history)
        print(f"Current Turn: {self.trn}")

        # Initialize static variables correctly
        if len(self.futureNodes) != len(self.game.detectives):
            # TODO: use extend instead of forloop and append
            for detective in self.game.detectives:
                self.futureNodes.append([])
                self.futureTransports.append([])
                self.living.append(1)
            # self.varInit = True

        self.getFutureOptions(self, 2, 3)
        
        disperseTurns = [1] # makes decission for turn 1 and 2 at the same time
        closeinTurns = [3, 4, 8, 13, 18, 24]
        encircleTurns = [5, 6, 7, 9, 10, 11, 14, 15, 16, 19, 20, 21, 22, 23]
        broadenTurns = [12, 17]
        
        # Decide everything in first detective decide call of this turn
        if self.id == self.living.index(1):
            self.options = []
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
        print(f"getting decision for id::{self.id}\nFuture:{self.futureNodes, self.futureTransports}")
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

    def closein(self):
        targetpos = self.game.misterx.lastKnownPosition

        for i in range (0, len(self.game.detectives)):
            path = nx.shortest_path(self.game.board.graph, self.game.detectives[i].position, targetpos)
            self.futureNodes[i].append(path[1])
            oklist = [opts[1] for opts in self.options[i] if opts[0] == path[1]]
            self.futureTransports[i].append(oklist[0])


    def encircle(self, decisiondepth=1):
        def validateOptionSet(optionset: list) -> bool:
            """
            Validate a set of options for detectives:
            1) Check no end positions overlap
            """
            ends = [option[0] for option in optionset if option[0] is not None]
            for end in ends:
                if ends.count(end) > 1:
                    return False
            return True

        def search(game, moves=[], depth=0):
            if depth == 0:
                return [(game.board.mrxEntropy(), moves)]
            fullOptions = []  # create a list containing all lists of options per detecive
            for i, det in enumerate(game.detectives):
                ops = game.board.getOptions(det)
                if ops == []:
                    ops = [(None, None)]
                fullOptions.append(ops)
            crossproduct = list(itertools.product(*fullOptions))  # Giant crossproduct of all possible options
            self.print_(f"Added fan-out of {len(crossproduct)} on level {depth}")

            results = []
            clone = game.clone()
            origDets = [d for d in clone.detectives]
            origMrx = clone.misterx.clone()
            clone.verbose = False
            for options in crossproduct:
                if not validateOptionSet(options):
                    continue
                for j, det in enumerate(clone.detectives):  # Manually create new moves that change the entropy of the current state
                    clone.detectives[j] = origDets[j].clone()
                    clone.board.movePlayer(clone.detectives[j], options[j][0], options[j][1])
                    if depth == decisiondepth:
                        # Only save the first moves, rest is used to simulate the future
                        moves = options
                clone.misterx.update()    
                results += search(clone, moves, depth=depth - 1)
                clone.misterx = origMrx.clone()
            return results

        self.print_("---Encircle algo---")
        bestEntropy, bestMove = min(search(self.game, depth=decisiondepth), key=lambda x: x[0])
        # Assign best option's positions to futurenodes/transports
        self.print_(f"Best move for lowering the entropy: {bestMove}\nGives a resulting entropy of {bestEntropy}")
        for i, move in enumerate(bestMove):
            self.futureNodes[i].append(move[0])
            self.futureTransports[i].append(move[1])

    def broaden(self):
        print("---Broaden algo---")
        for i, det in enumerate(self.game.detectives):
            decision = self.randomMove(det)
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
        # TODO: collision prevention
        targetMetro = self.assignMetro()

        for i in range(0, len(targetMetro)):
            path = nx.shortest_path(self.game.board.graph, self.game.detectives[i].position, targetMetro[i][0])
            print(f"Path length: {len(path)}")
            # if len(path) > 1: 
            transp = [transport[1] for transport in self.options[i] if transport[0] == path[1]]
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
                # only look 2 moves ahead and remove other decisions
                del path[3]

            #add missing transport
            if len(transp) < len(path)-1:
                i0 = len(transp)
                for j in range (i0,len(path)-1):
                    neighbours = self.game.board.getOptions(self.game.detectives[i], customStartPosition=path[j])
                    postrans = [transport[1] for transport in neighbours if transport[0] == path[j+1]]
                    transp.append(postrans[0])

                
            if len(transp) == 3:
                del transp[2]

            print(f"Future moves for detective {i}:  {path}")
            self.futureNodes[i] = path[1:]
            self.futureTransports[i] = transp
            print(f"Shortened: {self.futureNodes[i]}")
        return 0

    def getFutureOptions(self, detective, turnsAhead, startPosition):
        cards = detective.cards 
        index = detective.id
        maxNodesAnticipated = max([len(x) for x in self.futureNodes])
        maxTransportsAnticipated = max([len(x) for x in self.futureTransports])
        
        # Check if the turn is more in the future than anticipated, if this is the case, there are no restrictions on the available positions
        if maxNodesAnticipated < turnsAhead or maxTransportsAnticipated < turnsAhead:
            return self.game.board.getOptions(detective, startPosition)

        currentlyAhead = 0
        for transp in self.futureTransports[index]:
            if currentlyAhead <= turnsAhead:
                # remove that transport in dictionary
                cards[transp] -= 1
                if(cards[transp] < 0): cards[transp] = 0
            currentlyAhead += 1
            

        transportOptions = self.game.board.getSimulatedOptions(self, cards, startPosition)
        for nodeList in self.futureNodes:
            if turnsAhead < len(nodeList):
                tup1 = (nodeList[turnsAhead], 'taxi')
                tup2 = (nodeList[turnsAhead], 'bus')
                tup3 = (nodeList[turnsAhead], 'underground')
                if  tup1 in transportOptions:
                    transportOptions.remove(tup1)
                if  tup2 in transportOptions:
                    transportOptions.remove(tup2)
                if tup3 in transportOptions:
                    transportOptions.remove(tup3)
            
        return transportOptions



