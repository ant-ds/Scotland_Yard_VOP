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
        super().__init__(*args, **kwargs)
    
    
    

    # Should return a tuple (destination:int, transportation:string)
    def decide(self):
        print("#####---DETECTIVE AI RUNNING---#####")
        # print(f"ID is {self.id}")
        
        # Only calculate everything for first player, execute for all
        if self.id == 0:
            # Generate all options for this turn
            for detective in self.game.detectives:
                print(f"Options for detective {detective.id}: {self.game.board.getOptions(detective, doubleAllowed=False)}")
                ExampleAIImplementationDetective.options.append(self.game.board.getOptions(detective, doubleAllowed=False))
            
            # Calculate moves for first three moves
            self.metroMove()

        optionsdict = dict(ExampleAIImplementationDetective.options[self.id])
        
        # TODO: this ExampleAIImplementationDetective.options[...] will return first transport for a node, even if there are multiple options
        # TODO: remove moved from list and only metromove on turn 0
        print(f"Going to play detective {self.id} to {ExampleAIImplementationDetective.futureNodes[self.id][0]} using {optionsdict[ExampleAIImplementationDetective.futureNodes[self.id][0]]}")
        input("Press Enter to continue...")
        
        return ExampleAIImplementationDetective.futureNodes[self.id][0],optionsdict[ExampleAIImplementationDetective.futureNodes[self.id][0]]

    def getMetroDistances(self):
        "Returns list of distance of a player to all metros that are within reach in 3 turns" #TODO: exclude metros from shortest path (max 1 metro?)
        dist = []
        for detective in self.game.detectives:
            print(detective.position)
            metrodist = []
            for metro in const.METRO_STATIONS:
                if nx.shortest_path_length(self.game.board.graph, metro, detective.position)<=3:
                    metrodist.append([metro, nx.shortest_path_length(self.game.board.graph, metro, detective.position)])
                    # print(nx.shortest_path(self.game.board.graph, metro, detective.position))
            dist.append(metrodist)
            #print(metrodist)
        print(dist)
        return dist

    def assignMetro(self):
        "Assign metro to every detective" #TODO: don't just take first min, but consider other equal values
        dist = self.getMetroDistances()
        targetMetro = []
        for possibilities in dist:
            targetMetro.append(min(possibilities, key=itemgetter(1)))
        print(targetMetro)
        return targetMetro

    def metroMove(self):
        "Decides which moves to make for every detective"
        targetMetro = self.assignMetro()

        for i in range(0,len(targetMetro)):
            path = nx.shortest_path(self.game.board.graph, self.game.detectives[i].position, targetMetro[i][0])
            if len(path)>1: transp = [transport[1] for transport in ExampleAIImplementationDetective.options[i] if transport[0] == path[1]]
            # print(f"transport to test {transp[0]}")
            
            # detective already on a metro station
            if len(path) == 1: 
                # TODO: make a litle loop
                dummy = 0


            # detective one turn away from a metro station
            if len(path) == 2: #TODO: check if enough transport to do two upcoming moves
                backforth = self.game.board.getOptions(self.game.detectives[i], customStartPosition = path[1])
                transportToUse = "taxi"
                print(backforth)
                print(f"viable taxi positions: {[viable for viable in backforth if viable[1] is transportToUse]} ")
                path.append(random.choice([viable for viable in backforth if viable[1] is transportToUse]))
                transp.append(transportToUse)
                path.append(path[0])
                transp.append(transportToUse)

            # detective two turns away from metro stations
            if len(path) == 3:
                # TODO: try to make a little loop
                dummytwo = 0

            # detective three turns away from metro stations
            if len(path) == 4:
                # TODO: at feature transports
                dummythree = 0

            
                
            print(f"Future moves for detective {i}:  {path}")
            ExampleAIImplementationDetective.futureNodes.append(path[1:])
            ExampleAIImplementationDetective.futureTransports.append(transp)
            print(f"Shortened: {ExampleAIImplementationDetective.futureNodes[i]}")
        
        return 0