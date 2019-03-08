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
        self.print_(f"{self} his options are: {mrxOptions}")

        # give scores to each neighbour based on the shortest path of each neighbour to the detectives (higher score is better)
        scores = [(nbr, min(nx.shortest_path_length(self.game.board.graph, nbr, detective.position)
                  for detective in self.game.detectives) + self.game.board.graph.degree(nbr) % 4)
                  for nbr in self.game.board.graph[self.position]]
        self.print_(f"Scores for each neighbour of {self}: {scores}")
        scores = [tuple for tuple in scores if tuple[1] == max(score[1] for score in scores)]
        self.print_(f"Maximal scores for neighbours of {self}: {scores}")

        # determine options with maximal scores
        bestOptions = [option for option in mrxOptions if option[0] in [score[0] for score in scores]]
        self.print_(f"Choices with maximal scores: {bestOptions}")

        # choose random option from options with maximal scores
        decision = random.choice(bestOptions)

        if self.game.turn in [4, 9, 14, 19] and self.cards['black'] > 0 and ['underground', 'bus'] in [option[1] for option in mrxOptions]:
            decision = (decision[0], 'black')
        if decision[1] in ['bus', 'underground'] and (decision[0], 'taxi') in mrxOptions:
            decision = (decision[0], 'taxi')
        print(f"{self} chose to move from {self.position} to {decision[0]} via {decision[1]}")
        return decision[0], decision[1]
