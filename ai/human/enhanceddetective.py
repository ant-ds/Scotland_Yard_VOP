import networkx as nx
import itertools
from math import log2
from operator import itemgetter
import random
import numpy as np

from game.detective import Detective
import game.constants as const

class ExampleAIImplementationDetective(Detective):
    
    # static variables
    futureNodes = []  # List of lists of future nodes for every detective
    futureTransports = []  # List of lists of used transports for these nodes
    options = []  # List of lists of options for every detective
    living = []  # Gives first alive detective, needed in decide to make all choices when that detective plays
    
    def __init__(self, *args, **kwargs):
        self.trn = 1
        super().__init__(*args, **kwargs)

    def reset(self):
        super().reset()
        self.trn = 1
        self.emptyFutureLists()
        if self.options:

            for i in range(len(self.game.detectives)):
                del self.options[i][:]
        del self.living[:] 
        self.living.extend([1 for _ in range(len(self.game.detectives))])
    
    def decide(self):
        # self.testMetroStartDists(3)
        
        # Determine turn
        self.trn = len(self.game.misterx.history)
        self.print_(f"Current Turn: {self.trn}")

        # Initialize static variables correctly
        if len(self.futureNodes) != len(self.game.detectives):
            self.futureNodes.extend([[] for _ in range(len(self.game.detectives))])
            self.futureTransports.extend([[] for _ in range(len(self.game.detectives))])
            self.living.extend([1 for _ in range(len(self.game.detectives))])

        disperseTurns = [1] # makes decission for turn 1 and 2 at the same time
        closeinTurns = [3, 4, 8, 13, 18, 24, 25]
        encircleTurns = [5, 6, 7, 9, 10, 11, 14, 15, 16, 19, 20, 21, 22, 23]
        broadenTurns = [12, 17]
        
        # Decide everything in first detective decide call of this turn
        if 1 in self.living and self.id == self.living.index(1):
            self.options = []
            # Generate all options for this turn

            for i, detective in enumerate(self.game.detectives):
                ops = self.game.board.getOptions(detective)
                if ops == []:
                   ops = [(None, None)]
                self.options.append(ops)
                self.print_(f"Options for detective {detective.id}: {self.options[i]}")
            
            optionsleft = False
            for i, det in enumerate(self.game.detectives):
                if self.options[i] != [(None, None)]:
                    optionsleft = True
            
            if not optionsleft:
                for i, det in enumerate(self.game.detectives):
                    det.defeated = True
                return None, None

            if self.trn in disperseTurns:
                self.disperse()
            elif self.trn in closeinTurns:
                self.closein()
            elif self.trn in encircleTurns:
                self.encircle(decisiondepth=2)
            elif self.trn in broadenTurns:
                self.broaden()

        self.print_(f"getting decision for id::{self.id}\nFuture:{self.futureNodes, self.futureTransports}")
        try:
            decision = (self.futureNodes[self.id][0], self.futureTransports[self.id][0])
        except Exception as e:
            # print(vars(self))
            # print(vars(ExampleAIImplementationDetective))
            # raise e
            print("Unexpected empty list, assuming detective is out of moves")
            return None, None
        del self.futureTransports[self.id][0]
        del self.futureNodes[self.id][0]
        if decision == (None, None):
            self.living[self.id] = 0

        self.print_(f"Going to play {decision[1]} from {self.position} to {decision[0]}")

        # input("Press Enter to continue...")
        return decision[0], decision[1]

    def disperse(self):

        def getMetroDistances():
            """
            Compose list of distance of a player to all metros that are within a distance of 3 turns
            Returns: list of tuples with (metropos, shortest path length to metro)
            """
            possibleMetros = [] # list containing lists of tuples, every list corresponds to one detective
            for detective in self.game.detectives:
                metrodist = []
                for metro in const.METRO_STATIONS:
                    pl = nx.shortest_path_length(self.game.board.graph, metro, detective.position)
                    if pl <= 3 and pl > 0:
                        metrodist.append((metro, pl))
                possibleMetros.append(metrodist)
            self.print_(f"Metro's for the detectives: {possibleMetros}")
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
            # print(f"Target metros for detectives: {targetMetro}")
            return targetMetro

        # print("---Disperse algo---")
        
        targetMetro = assignMetro()

        assert (len(targetMetro) == len(self.game.detectives)), "MetroList and detectiveList not of same length!"
        
        for i, det in enumerate(self.game.detectives):
            path = nx.shortest_path(self.game.board.graph, det.position, targetMetro[i])
            assert (len(path) != 0), "Path lenght is 0!"
            self.print_(f"Shortest path calculation for detective {i}, path length : {len(path)}")
            transp = []
            taken = []
            for turnToEval in range(1,min([3,len(path)])):
                for j in range(0,i): 
                        taken.append(self.futureNodes[j][turnToEval-1])
                        if len(self.futureNodes[j]) > turnToEval:
                            taken.append(self.futureNodes[j][turnToEval]) # prevent next detective from blocking earlier detective by being on needed position before moving
                
                if path[turnToEval] in taken:
                    self.print_(f"Collision detected for detective {i}, problematic node: {path[turnToEval]}.")
                    #collision: find node with shortest path
                    neighbours = [node[0] for node in self.game.board.getOptions(det, customStartPosition=path[turnToEval-1]) if node[0] not in taken]
                    lengths = [nx.shortest_path_length(self.game.board.graph, pos, targetMetro[i]) for pos in neighbours]
                    index, _ = min(enumerate(lengths), key=itemgetter(1))
                    newpath = nx.shortest_path(self.game.board.graph, neighbours[index], targetMetro[i])
                    path = path[0:turnToEval] + newpath
            transportPos = [transport[1] for transport in self.options[i] if transport[0] == path[1]]
            transp.append(transportPos[0])
            
            # detective one turn away from a metro station
            if len(path) == 2: 
                neighbours = self.getFutureOptions(det, 1, path[1])
                transportToUse = "taxi"
                # print(backforth)
                # print(f"viable taxi positions: {[viable for viable in backforth if viable[1] is transportToUse]} ")
                path.append(random.choice([viable for viable in neighbours if viable[1] is transportToUse])[0])
                transp.append(transportToUse)
                path.append(path[0])
                transp.append(transportToUse)
            
            
            if len(path) >3 :
                # only look 2 moves ahead and remove other decisions
                path = path[0:3]

            #add missing transport
            if len(transp) < len(path)-1:
                i0 = len(transp)
                for j in range (i0,len(path)-1):
                    neighbours = self.getFutureOptions(det, j, path[j])
                    postrans = [transport[1] for transport in neighbours if transport[0] == path[j+1]]
                    transp.append(postrans[0])

                
            if len(transp) > 2:
                transp = transp[:2]

            # print(f"Future moves for detective {i}:  {path}")
            self.futureNodes[i] = path[1:]
            self.futureTransports[i] = transp
            # print(f"Shortened: {self.futureNodes[i]}")
        return 0


    def closein(self):
        self.emptyFutureLists()
        for i in range(len(self.game.detectives)):
            #split list of tuples (postion, transport) into two separate lists [positions] and [transport]
            neighboursPos, neighboursTrans = map(list,zip(*self.getAvailableOptions(i))) 

            lengths = [nx.shortest_path_length(self.game.board.graph, pos, self.game.misterx.lastKnownPosition) for pos in neighboursPos]
            if lengths:    
                index, _ = min(enumerate(lengths), key=itemgetter(1))
                self.futureNodes[i].append(neighboursPos[index])
                self.futureTransports[i].append(neighboursTrans[index])
            # else:
            #     self.futureNodes[i].append([None])
            #     self.futureTransports[i].append([None])
                

    def encircle(self, decisiondepth = 1):
        def narrowXPosition():
            """
            Narrow all mrX positions down to a subset of most likely positions
            Returns: list of tuples (position, probability)
            """
            _, dictX = self.game.board.possibleMisterXPositions(returnProbabilities=True)
            possibleX = list(dictX.items())
            # print(f"Possible positions for mr X: {possibleX}")
            averageProb = sum(map(lambda x: x[1], possibleX)) / len(possibleX)
            probableX = [pos for pos in possibleX if pos[1] >= averageProb]
            # print(f"Average probability: {averageProb}\nNarrowed down positions for mr X: {probableX}")
            self.print_(f"Original amount of X positions: {len(possibleX)} now narrowed down to {len(probableX)}")
            return probableX
        
        def calcEntropy(tupleList):
            """
            Calculate the entropy of a given list of tuples (..., probability)
            Returns: a double
            """
            _, probabilities = map(list, zip(*tupleList))
            entropy = 0.0
            for p in probabilities:
                entropy -= p * log2(p)
            # condpr(f"Entropy: {entropy}")
            return entropy

        def multipleExpand(newDetectivePositions, depth = decisiondepth):
            """
            Expands a given list of mrXpositions with it's neighbours
            Returns: list of tuples (position, probability)
            """
            mrx = self.game.misterx 
            # Look up the most recent reveal and slice the history accordingly
            sliceStart = max([i for i in const.MRX_OPEN_TURNS if i <= self.trn])
            moves = [hist[1] for hist in mrx.history[sliceStart:]]
            # print(f"Moves: {moves}")
            for _ in range(0, depth):
                moves.append('black')
            prohibited = self.game.board.getprohibited(sliceStart - len(mrx.doubleMoves))  # Account for double moves disrupting the indices
            prohibited.append(newDetectivePositions)
            # print(f"{prohibited}")
            _, dictX = self.game.board.possiblePositions(
                            mrx.lastKnownPosition, 
                            moves=moves, 
                            occupied=prohibited, 
                            refuseCurrent=True, 
                            returnProbabilities=True, 
                        )
            possibleX = list(dictX.items())
            
            if possibleX == []:
                _, dictX = self.game.board.possibleMisterXPositions(returnProbabilities=True)
                possibleX = list(dictX.items())
                if not possibleX:
                    print("Da last buggggg")
                    possibleX = [(self.game.misterx.lastKnownPosition, 0.01)]
            return possibleX

        def optionGenerator(prevOptions = [], skip = []):
            """
            Generates a list of options for each detective
            """
            if prevOptions == [] and skip == []:
                fullOptions = []  # create a list containing all lists of options per detecive
                
                for i, det in enumerate(self.game.detectives):
                    if not det.defeated:
                        ops = self.game.board.getOptions(det)
                        if ops:
                            fullOptions.append(ops)
                        else:
                            skip.append(i)
                return fullOptions, skip
            
            if prevOptions: 
                oldOptions = prevOptions
                if len(oldOptions) != len(self.game.detectives):
                    print("Breakpoint")
                fullOptions = []
                j = 0
                for i, det in enumerate(self.game.detectives):
                    if (not det.defeated) and (i not in skip):
                        tempOptions = []
                        for nde, _ in oldOptions[j]:
                            ops = self.game.board.getOptions(det, customStartPosition = nde)
                            if ops:
                                tempOptions.extend(ops)
                        if tempOptions:
                            fullOptions.append(tempOptions)
                        else:
                            if oldOptions[j]:
                                fullOptions.append(oldOptions[j])
                            else:
                                assert(False), "Error in optionGenerator"
                        j += 1
                return fullOptions, skip
            assert(False), "Error in optionGenerator"

        def solutionCompute(currentDepth, fullOptions, skip = []):
            """
            Assign a score for every possibility and filter based on that score (entropy + transport)
            Returns list of sets (possibility, score), the average entropy and the list to skip
            """
            fullOptions, skip = optionGenerator(fullOptions, skip)
            crossproduct = list(itertools.product(*fullOptions))  # Giant crossproduct of all possible options      
            print(f"Added fan-out of {len(crossproduct)} on level {currentDepth}")
            summedEnt = 0
            solution = []
            scoreList = []
            for i, scenario in enumerate(crossproduct):
                detectivePos = [node[0] for node in scenario]
                expanded = multipleExpand(detectivePos, depth=currentDepth)
                # entropy for score
                ent = calcEntropy(expanded)
                # transport for score
                score = ent
                # OPTION: comment the 3 following lines to remove transport scoring
                for tup in scenario:
                    if tup[1] != "taxi":
                        score += 0.25
                summedEnt += ent
                scoreList.append(score)
                solution.append((crossproduct[i],score))
            averageEnt = summedEnt/len(crossproduct)
            averageScore = sum(scoreList)/len(crossproduct)
            self.print_(f"Average entropy: {averageEnt}, Average score: {averageScore}")

            npScores = np.array(scoreList)
            
            # k is the amount options chosen for next level
            # OPTION: change value of k to narrow/broaden branching
            k = (int) (60/len(self.game.detectives))
            
            kk = (int) (min(k,len(npScores)-1))
            indexes = np.argpartition(npScores, kk)[:kk]
            
            scenarios = []
            for ind in indexes:
                scenarios.append(solution[ind])
            
            print(f"Filter: reduced fanout of level {currentDepth} from {len(solution)} to {len(scenarios)}")

            #Change scenarios to options
            filteredSol = [] 
            solutions = [scenario[0] for scenario in scenarios]
            for i in range(len(solutions[0])):
                allsols = [scenario[i] for scenario in solutions]
                uniquesols = list(set(allsols))
                filteredSol.append(uniquesols)
            return filteredSol, scenarios, skip


        assert(decisiondepth != 0), "Decisiondepth must be greater than zero" 
        

        #sol is a list of tuples (scenario, entropy)
        sol, scenarios, skp = solutionCompute(1,[],[])

        for i in range(1, decisiondepth):    
            sol, scenarios, skp = solutionCompute(i+1, sol, skp)

        if len(scenarios) != 1:
            best = min(scenarios, key = lambda t: t[1])[0]
        else:
            print(scenarios)
            best = scenarios[0][0]
        
        
        decissions = []
        j=0
        for i, det in enumerate(self.game.detectives):
            if not det.defeated and i not in skp:
                neighboursPos, neighboursTrans = map(list,zip(*self.getAvailableOptions(i)))
                if neighboursPos and neighboursTrans:
                    lengths = [nx.shortest_path_length(self.game.board.graph, pos, best[j][0]) for pos in neighboursPos]
                    if lengths:    
                        index, _ = min(enumerate(lengths), key=itemgetter(1))
                        decissions.append((neighboursPos[index],neighboursTrans[index]))
                else:
                    decissions.append((None,None))
                j+=1
            else:
                decissions.append((None,None))
        for i, decission in enumerate(decissions):
            self.futureNodes[i].append(decission[0])
            self.futureTransports[i].append(decission[1])
    

    def broaden(self):

        self.emptyFutureLists()
        self.print_("---Broaden algo---")

        for i, det in enumerate(self.game.detectives):
            decision = self.randomMove(det)
            self.futureNodes[i].append(decision[0])
            self.futureTransports[i].append(decision[1])

    def randomMove(self, det):

        options = self.getAvailableOptions(det)
        decision = random.choice(options)

        return decision[0], decision[1]


    def getFutureOptions(self, detective, turnsAhead, startPosition):
        """
        Returns a list of tuples that will be available in the future, taking into accounts the future moves
        Arguments: a detective, amount of turns into the future, startposition
        Returns: list of tuples (position, transport)
        """
        cards = detective.cards 
        index = detective.id
        
        for i in range(min(len(self.futureTransports[index]), turnsAhead)):
            cards[self.futureTransports[i]] = min(0, cards[self.futureTransports[i]]-1)
        
        taken = []
        for nodeList in self.futureNodes:
            if turnsAhead < len(nodeList)-1 and i < index:
                taken.append(nodeList[turnsAhead+1]) #Those positions are where an earlier detective plans to go, so it may not be occupied.
            if turnsAhead < len(nodeList):
                taken.append(nodeList[turnsAhead]) #Those positions will still be occupied by other detectives

        transportOptions = self.game.board.getSimulatedOptions(cards, startPosition, taken)
        return transportOptions

    def emptyFutureLists(self):
        for i in range(len(self.game.detectives)):
            del self.futureNodes[i][:]
            del self.futureTransports[i][:]

    def getAvailableOptions(self, detOrId):
        """
        Returns a list of tuples that are available after taking the future decissions, made for earlier detectives, into account
        Arguments: a detective, or a detective id
        Returns: list of tuples (position, transport)
        """

        assert(isinstance(detOrId, int) or (detOrId, Detective))
        if isinstance(detOrId, int):
            i = detOrId
        elif isinstance(detOrId, Detective):
            i= detOrId.id
        
        # Generate list of unavailable positions for our detective
        taken = []
        for j in range(i):
            if self.futureNodes[j]:
                taken.append(self.futureNodes[j][0]) #Those positions will still be occupied by other detectives
            if len(self.futureNodes[j]) > 1:
                taken.append(self.futureNodes[j][1]) #Those positions are where an earlier detective plans to go, so it may not be occupied.
        
        options = [node for node in self.options[i] if node[0] not in taken]
        # Return None if options is empty
        if not options:
            return [(None, None)]
        return options

        
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

                self.print_(f"PROBLEM: No less than {dist} metro for node {startPos}")

            metrodists.append(metrodist)
        self.print_(metrodists)


###########################
