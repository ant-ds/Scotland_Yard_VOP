from game.misterx import MisterX
import random
import networkx as nx


class ExampleAIImplementationMisterX(MisterX):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # Should return a tuple (destination:int, transportation:string)
    def decide(self):

        # get options for MrX
        mrxOptions = self.game.board.getOptions(self, doubleAllowed=False)
        print(f"Mr. X his options are:: {mrxOptions}")

        # give scores to each neighbour based on the shortest path of each neighbour to the detectives (higher score is better)
        scores = [(nbr, min(nx.shortest_path_length(self.game.board.graph, nbr, detective.position) for detective in self.game.detectives))
                  for nbr in self.game.board.graph[self.position]]
        print(f"Scores for each neighbour of Mr. X {scores}")
        scores = [tuple for tuple in scores if tuple[1] == max(score[1] for score in scores)]
        print(f"Maximal scores for neighbours of Mr. X {scores}")

        # determine options with maximal scores
        bestOptions = [option for option in mrxOptions if option[0] in [score[0] for score in scores]]
        print(f"Choices with maximal scores: {bestOptions}")

        # choose random option from options with maximal scores
        decision = random.choice(bestOptions)

        if self.game.turn in [4, 9, 14, 19] and self.cards['black'] > 0:
            decision = (decision[0], 'black')
        print(f"{self} chose to move from {self.position} to {decision[0]} via {decision[1]}")
        return decision[0], decision[1]
