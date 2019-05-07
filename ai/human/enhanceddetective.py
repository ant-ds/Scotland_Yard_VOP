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
        # self.futureNodes = []
        # self.futureTransports = []
        if self.options:

            for i in range(len(self.game.detectives)):
                del self.options[i][:]
        del self.living[:] 
        self.living.extend([1 for _ in range(len(self.game.detectives))])   
        # self.options = []
        # self.living = []
    
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
                return None, None

            if self.trn in disperseTurns:
                self.disperse()
            elif self.trn in closeinTurns:
                self.closein()
            elif self.trn in encircleTurns:
                self.encircle(decisiondepth=1)
            elif self.trn in broadenTurns:
                self.broaden()

        self.print_(f"getting decision for id::{self.id}\nFuture:{self.futureNodes, self.futureTransports}")
        try:
            decision = (self.futureNodes[self.id][0], self.futureTransports[self.id][0])
        except Exception as e:
            print(vars(self))
            print(vars(ExampleAIImplementationDetective))
            raise e
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
            # TODO: exclude metros from shortest path (max 1 metro?) - need to test availability!
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
        # def narrowXPosition():
        #     """
        #     Narrow all mrX positions down to a subset of most likely positions
        #     Returns: list of tuples (position, probability)
        #     """
        #     _, dictX = self.game.board.possibleMisterXPositions(returnProbabilities=True)
        #     possibleX = list(dictX.items())
        #     # print(f"Possible positions for mr X: {possibleX}")
        #     averageProb = sum(map(lambda x: x[1], possibleX)) / len(possibleX)
        #     probableX = [pos for pos in possibleX if pos[1] >= averageProb]
        #     # print(f"Average probability: {averageProb}\nNarrowed down positions for mr X: {probableX}")
        #     condpr(f"Original amount of X positions: {len(possibleX)} now narrowed down to {len(probableX)}")
        #     # TODO: do something with amount of options for a node.
        #     return probableX
        
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

        # def expand(newDetectivePositions):
        #     """
        #     Expands a given list of mrXpositions with it's neighbours
        #     Returns: list of tuples (position, probability)
        #     """
        #     mrx = self.game.misterx 
        #     # Look up the most recent reveal and slice the history accordingly
        #     sliceStart = max([i for i in const.MRX_OPEN_TURNS if i <= self.trn])
        #     moves = [hist[1] for hist in mrx.history[sliceStart:]]
        #     # print(f"Moves: {moves}")
        #     moves.append('black')
        #     prohibited = self.game.board.getprohibited(sliceStart - len(mrx.doubleMoves))  # Account for double moves disrupting the indices
        #     prohibited.append(newDetectivePositions)
        #     # print(f"{prohibited}")
        #     _, dictX = self.game.board.possiblePositions(
        #                     mrx.lastKnownPosition, 
        #                     moves=moves, 
        #                     occupied=prohibited, 
        #                     refuseCurrent=True, 
        #                     returnProbabilities=True, 
        #                 )
        #     possibleX = list(dictX.items())
        #     if possibleX == []:
        #         print("BUG")
        #     return possibleX
        
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
                print("BUG")
            return possibleX

        def optionGenerator(prevOptions = [], skip = []):
            """
            Generates a list of options for each detective
            """
            if prevOptions == [] and skip == []:
                fullOptions = []  # create a list containing all lists of options per detecive
                # skip = []
                
                for i, det in enumerate(self.game.detectives):
                    if not det.defeated:
                        ops = self.game.board.getOptions(det)
                        if ops:
                            fullOptions.append(ops)
                        else:
                            skip.append(i)
                return fullOptions, skip
            
            if prevOptions: 
                # TODO: test
                oldOptions = prevOptions
                fullOptions = []
                for i, det in enumerate(self.game.detectives):
                    if (not det.defeated) and (i not in skip):
                        tempOptions = []
                        for nde, _ in oldOptions[i]:
                            ops = self.game.board.getOptions(det, customStartPosition = nde)
                            if ops:
                                tempOptions.extend(ops)
                        if tempOptions:
                            fullOptions.append(tempOptions)
                        else:
                            if oldOptions[i]:
                                fullOptions.append(oldOptions[i])
                            else:
                                assert(False), "Error in optionGenerator"
                return fullOptions, skip
            assert(False), "Error in optionGenerator"

        def solutionCompute(currentDepth, fullOptions, skip = []):
            """
            Calculate entropy for every possible option
            Returns list of sets (possibility, entropy), the average entropy and the list to skip
            """
            fullOptions, skip = optionGenerator(fullOptions, skip)
            crossproduct = list(itertools.product(*fullOptions))  # Giant crossproduct of all possible options      
            self.print_(f"Added fan-out of {len(crossproduct)} on level {currentDepth}")
            # print(f"Crossproduct: {crossproduct}")
            # entropy = -1
            # bestScenario = 0
            summedEnt = 0
            solution = []
            for i, scenario in enumerate(crossproduct):
                detectivePos = [node[0] for node in scenario]
                expanded = multipleExpand(detectivePos, depth=currentDepth)
                ent = calcEntropy(expanded)
                summedEnt = summedEnt + ent
                solution.append((crossproduct[i],ent))
                # if entropy > ent or entropy == -1:
                #     entropy = ent
                #     bestScenario = i
                #     # print(f"ENTROPY CHANGED TO {entropy} (scenario: {i})")
            averageEnt = summedEnt/len(crossproduct)
            return solution, averageEnt, skip

        def filterSolution(solution, averageEnt = None, skip = [], currentDepth = 0):
            """
            Filters all solutions to a subset to be examined in next depth based on a score given by entropy and transportmethods. The lower the score, the better.
            """

            optimalTransport = []
            for i, det in enumerate(self.game.detectives):
                if(i not in skip):
                    # TODO: filter transport here
                    optimalTransport.append("taxi")

            #Increment score (=entropy) 0.25 for every lesser transport
            
            scoresol = []
            scorearray = []
            penalty = 0
            for sol in solution:
                for i, tup in enumerate(sol[0]):
                    penalty = 0
                    if tup[1] != optimalTransport[i]:
                        penalty = penalty + 0.25
                score = sol[1] + penalty
                scorearray.append(score)
                scoresol.append((sol[0],score))
            scorearray = np.array(scorearray)
            scorefilter = np.percentile(scorearray, 1)
            #TODO: choose percentile in order to have x amount of scenarios left
            
            #Filter: only consider scenario's below average score
            scenarios = []
            if averageEnt:
                scenarios = [sol[0] for sol in scoresol if sol[1] < scorefilter]
                print(f"Filter: reduced fanout of level {currentDepth} to: {len(scenarios)}")
            else:
                scenarios = [sol[0] for sol in scoresol]
            
            if not scenarios:
                scenarios.append(min(scoresol, key = lambda t: t[1])[0])

            #Change scenarios to options
            filteredSol = [] 
            for i in range(len(scenarios[0])): #TODO: DEBUG HERE
                allsols = [scenario[i] for scenario in scenarios]
                uniquesols = list(set(allsols))
                filteredSol.append(uniquesols)


            return filteredSol, scenarios


        assert(decisiondepth != 0), "Decisiondepth must be greater than zero" 

        sol, ae, skp = solutionCompute(1,[],[])
        #sol is a list of tuples (scenario, entropy)


        for i in range(1, decisiondepth):    
            options, _ = filterSolution(sol, averageEnt = ae, skip = skp, currentDepth = i)
            sol, ae, skp = solutionCompute(i+1, options, skp)
        
        _, scenarios = filterSolution(sol, averageEnt = ae, skip = skp, currentDepth = decisiondepth)

        if len(scenarios) != 1:
            best = min(scenarios, key = lambda t: t[1])
        else:
            best = scenarios[0]    
        
        
        decissions = []
        j=0
        for i, det in enumerate(self.game.detectives):
            if not det.defeated and i not in skp:
                # print(f"Da moves are: {moves[j]}")
                neighboursPos, neighboursTrans = map(list,zip(*self.getAvailableOptions(i)))
                if neighboursPos and neighboursTrans:
                    lengths = [nx.shortest_path_length(self.game.board.graph, pos, best[j][0]) for pos in neighboursPos]
                    if lengths:    
                        index, _ = min(enumerate(lengths), key=itemgetter(1))
                        decissions.append((neighboursPos[index],neighboursTrans[index]))
                        # self.futureNodes[i].append(neighboursPos[index])
                        # self.futureTransports[i].append(neighboursTrans[index])
                else:
                    decissions.append((None,None))
                j+=1
            else:
                decissions.append((None,None))
        for i, decission in enumerate(decissions):
            self.futureNodes[i].append(decission[0])
            self.futureTransports[i].append(decission[1])
    
    
    
    # def encircle(self, decisiondepth=1):
    #     def validateOptionSet(optionset: list) -> bool:
    #         """
    #         Validate a set of options for detectives:
    #         1) Check no end positions overlap
    #         """
    #         ends = [option[0] for option in optionset if option[0] is not None]
    #         for end in ends:
    #             if ends.count(end) > 1:
    #                 return False
    #         return True

    #     def search(game, moves=[], depth=0):
    #         if depth == 0:
    #             return [(game.board.mrxEntropy(), moves)]
    #         fullOptions = []  # create a list containing all lists of options per detecive
    #         for i, det in enumerate(game.detectives):
    #             ops = self.getAvailableOptions(det)
    #             fullOptions.append(ops)
    #         crossproduct = list(itertools.product(*fullOptions))  # Giant crossproduct of all possible options
    #         self.print_(f"Added fan-out of {len(crossproduct)} on level {depth}")

    #         results = []
    #         clone = game.clone()
    #         origDets = [d for d in clone.detectives]
    #         origMrx = clone.misterx.clone()
    #         clone.verbose = False
    #         for options in crossproduct:
    #             if not validateOptionSet(options):
    #                 continue
    #             for j, det in enumerate(clone.detectives):  # Manually create new moves that change the entropy of the current state
    #                 clone.detectives[j] = origDets[j].clone()
    #                 clone.board.movePlayer(clone.detectives[j], options[j][0], options[j][1])
    #                 if depth == decisiondepth:
    #                     # Only save the first moves, rest is used to simulate the future
    #                     moves = options
    #             # TODO: elliminate this update
    #             clone.misterx.update()    
    #             results += search(clone, moves, depth=depth - 1)
    #             clone.misterx = origMrx.clone()
    #         return results

    #     self.print_("---Encircle algo---")
    #     bestEntropy, bestMove = min(search(self.game, depth=decisiondepth), key=lambda x: x[0])
    #     # Assign best option's positions to futurenodes/transports
    #     self.print_(f"Best move for lowering the entropy: {bestMove}\nGives a resulting entropy of {bestEntropy}")
    #     for i, move in enumerate(bestMove):
    #         self.futureNodes[i].append(move[0])
    #         self.futureTransports[i].append(move[1])

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
