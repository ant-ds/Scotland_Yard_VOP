from game.detective import Detective
from game.board import Board
from game.game import ScotlandYard
import game.constants as const
import networkx as nx

from operator import itemgetter

class ExampleAIImplementationDetective(Detective):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    # Should return a tuple (destination:int, transportation:string)
    def decide(self):
        print("#####---DETECTIVE AI RUNNING---#####")
        self.assignMetro()
        input("Press Enter to continue...")
        return 153, 'taxi'


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
        assignList = []
        for test in dist:
            assignList.append(min(test, key=itemgetter(1)))
        print(assignList)
        return assignList

    def metroMove(self):
        "Decides which moves to make for every detective"
        return 0