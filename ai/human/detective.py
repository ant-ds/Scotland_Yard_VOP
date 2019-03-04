from game.detective import Detective
from game.board import Board
from game.game import ScotlandYard
import game.constants as const

class ExampleAIImplementationDetective(Detective):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    # def getMetroDistance(self):
    #     "Returns list of distance of a player to all metros"
    #     for metro in const.METRO_STATIONS:
    #         print(metro)
    #     return 0

    # Should return a tuple (destination:int, transportation:string)
    def decide(self):
        return 153, 'taxi'



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