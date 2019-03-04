from game.detective import Detective
from game.board import Board
from game.game import ScotlandYard
import game.constants as const
import networkx as nx

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
        "Returns list of distance of a player to all metros"
        dist = []
        for detective in self.game.detectives:
            metrodist = []
            for metro in const.METRO_STATIONS:
                metrodist.append([metro, nx.shortest_path_length(self.game.board.graph, metro, detective.position)])
            dist.append(metrodist)
            print(metrodist)
        #print(dist)
        return dist

    def assignMetro(self):
        "Assign metro to every detective"
        dist = self.getMetroDistances()
        #continue here
        return 0


    # # TODO
    # def calcXPositions(self):
    #     posLastReveal = 0 #get last reveal
    #     playedMoves = 0 #get played moves since
    #     turn = ScotlandYard().turn

    #     # Get last known position of mr X
    #     # Calculate all possible positions based on used cards (black might be difficult)
    #     return 0

    # # TODO
    # def turnsTillReveal():
    #     #gives back turns till reveal
    #     return 0
    
    


    # def assignMetro():
    #     #assign a metro station to