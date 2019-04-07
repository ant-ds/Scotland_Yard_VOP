import networkx as nx
import itertools

from operator import itemgetter
import random

from game.detective import Detective
from game.board import Board
from game.game import ScotlandYard
import game.constants as const

# TODO-list: 
#   Cleanup code: try to use less for loops and more python adapted stuff
#   Implement getAdvancedOptions
#   Collisions on uneven turns (one in previous turn)
#
#
printplez = True
def condpr(item):
    if printplez:
        print(item)

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
                condpr(f"Options for detective {detective.id}: {self.game.board.getOptions(detective, doubleAllowed=False)}")
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
        input("Press Enter to continue...")
        return decision[0], decision[1]

    def disperse(self):

        def getMetroDistances():
            """
            Compose list of distance of a player to all metros that are within a distance of 3 turns
            Returns list of tuples with (metropos, shortest path length to metro)
            """
            # TODO: exclude metros from shortest path (max 1 metro?) - need to test availability!
            possibleMetros = [] # list containing lists of tuples, every list corresponds to one detective
            for detective in self.game.detectives:
                metrodist = []
                for metro in const.METRO_STATIONS:
                    pl = nx.shortest_path_length(self.game.board.graph, metro, detective.position)
                    if pl <= 3 and pl > 0:
                        metrodist.append((metro, pl))
                possibleMetros.append(metrodist)
            condpr(f"Metro's for the detectives: {possibleMetros}")
            return possibleMetros
        
        def assignMetro():
            """
            Assign a specific metro station to every detective, based on distance. Distance 2 is preferred, followed by distance 1, then 3.
            Returns list of metrostations, the position inside defines to which detective that metro is assigned. 
            """
            possibleMetros = getMetroDistances()
            targetMetro = []
            for possibilities in possibleMetros:
                sizeTwo = [metroTup[0] for metroTup in possibilities if metroTup[1] == 2 and metroTup[0] not in targetMetro]
                if sizeTwo:
                    targetMetro.append(random.choice(sizeTwo))
                else:
                    sizeOne = [metroTup[0] for metroTup in possibilities if metroTup[1] == 1 and metroTup[0] not in targetMetro]
                    if sizeOne:
                        targetMetro.append(random.choice(sizeOne))
                    else:
                        sizeThree = [metroTup[0] for metroTup in possibilities if metroTup[1] == 3 and metroTup[0] not in targetMetro]
                        if sizeThree: 
                            targetMetro.append(random.choice(sizeThree))
                        else: 
                            # Assign random unassigned metro
                            remainingMetros = [metro for metro in const.METRO_STATIONS if metro not in targetMetro]
                            targetMetro.append(random.choice(remainingMetros))
            print(f"Target metros for detectives: {targetMetro}")
            return targetMetro

        print("---Disperse algo---")
        
        targetMetro = assignMetro()

        #Small error check:
        assert (len(targetMetro) == len(self.game.detectives)), "MetroList and detectiveList not of same length!"
        
        for i in range(0, len(self.game.detectives)):
            path = nx.shortest_path(self.game.board.graph, self.game.detectives[i].position, targetMetro[i][0])
            assert (len(path) != 0), "Path lenght is 0!"
            condpr(f"Path length: {len(path)}")
            # to test: are there conflicting shortest paths?
            taken = []
            for turnToEval in range(1,min([3,len(path)])):
                for j in range(0,i): 
                        taken.append(self.futureNodes[j][turnToEval])
                
                if path[turnToEval] in taken:
                    #collision: find node with shortest path
                    neighbours = [node[0] for node in self.game.board.getOptions(self.game.detectives[i], customStartPosition=path[turnToEval-1]) if node[0] not in taken]
                    lengths = [nx.shortest_path(self.game.board.graph, pos, targetMetro[i][0]) for pos in neighbours]
                    index, _ = max(enumerate(lengths), key=itemgetter(1))
                    newpath = nx.shortest_path(self.game.board.graph, neighbours[index], targetMetro[i][0])
                    path = [path[0:turnToEval-1], newpath]
            transp = [transport[1] for transport in self.options[i] if transport[0] == path[1]]
            
            # detective one turn away from a metro station
            if len(path) == 2: 
                # TODO: check if enough transport to do two upcoming moves
                neighbours = self.getFutureOptions(self.game.detectives[i], 1, path[1])
                transportToUse = "taxi"
                # print(backforth)
                # print(f"viable taxi positions: {[viable for viable in backforth if viable[1] is transportToUse]} ")
                path.append(random.choice([viable for viable in neighbours if viable[1] is transportToUse])[0])
                transp.append(transportToUse)
                path.append(path[0])
                transp.append(transportToUse)
            
            
            if len(path) >3 :
                # only look 2 moves ahead and remove other decisions
                path = path[0:2]

            #add missing transport
            if len(transp) < len(path)-1:
                i0 = len(transp)
                for j in range (i0,len(path)-1):
                    neighbours = self.game.board.getOptions(self.game.detectives[i], customStartPosition=path[j])
                    postrans = [transport[1] for transport in neighbours if transport[0] == path[j+1]]
                    transp.append(postrans[0])

                
            if len(transp) > 2:
                transp = transp[0:1]

            print(f"Future moves for detective {i}:  {path}")
            self.futureNodes[i] = path[1:]
            self.futureTransports[i] = transp
            print(f"Shortened: {self.futureNodes[i]}")
        return 0

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
        # startPos = possible position
        for startPos in const.START_POSITIONS['detectives']:
            metrodist = []
            for metro in const.METRO_STATIONS:
                if nx.shortest_path_length(self.game.board.graph, metro, startPos) <= dist:
                    metrodist.append([metro, nx.shortest_path_length(self.game.board.graph, metro, startPos)])
            if(len(metrodist) == 0):
                print(f"PROBLEM: No less than {dist} metro for node {startPos}")
            metrodists.append(metrodist)
        print(metrodists)

    # def testCollidingShortestPaths(self):
    #     paths = []
    #     for startPos in const.START_POSITIONS['detectives']:
    #         for metro in const.METRO_STATIONS:
    #             paths.append(nx.shortest_path(self.game.board.graph, startPos, metro))

    #     for startPos in const.START_POSITIONS['detectives']:
    #         for i in range (0, len(startPos)):
    #             for j in range (0, len(const.START_POSITIONS)):
    #                 if const.START_POSITIONS[j] != startPos and startPos(i) == 

###########################

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
            

        transportOptions = self.game.board.getSimulatedOptions(cards, startPosition)
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



