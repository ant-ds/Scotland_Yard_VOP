from game.detective import Detective
from game.board import Board
from game.game import ScotlandYard
import game.constants as const
import networkx as nx

from operator import itemgetter


class ExampleAIImplementationDetective(Detective):
    def __init__(self, *args, **kwargs):
        self.futureMoves = [] # List of lists of futuremoves for every detective
        super().__init__(*args, **kwargs)
    
    

    # Should return a tuple (destination:int, transportation:string)
    def decide(self):
        print("#####---DETECTIVE AI RUNNING---#####")
        
        #only calculate everything for first player, execute for all
        if self.id == 0:
            self.metroMove()
        
        # get transport option for chosen move
        options = self.game.board.getOptions(self, doubleAllowed=False)
        options = dict(options)
        
        # TODO: this options[...] will return first transport for a node, even if there are multiple options
        print(f"Going to play detective {self.id} to {self.futureMoves[self.id][0]} using {options[self.futureMoves[self.id][0]]}")
        input("Press Enter to continue...")
        
        return self.futureMoves[self.id][0],options[self.futureMoves[self.id][0]]

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
            # print(targetMetro[i][0])
            path = nx.shortest_path(self.game.board.graph, self.game.detectives[i].position, targetMetro[i][0])
            print(f"Future moves for detective {i}:  {path}")
            self.futureMoves.append(path[1:])
            print(f"Shortened: {self.futureMoves[i]}")
        
        return 0