from game.misterx import MisterX
import random
import networkx as nx


class ExampleAIImplementationMisterX(MisterX):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # Should return a tuple (destination:int, transportation:string)
    def decide(self):
        # play double move to pass over reveal
        if len(self.history) in [2, 7, 12, 17] and self.cards['double'] > 0:
            mrxOptions = self.game.board.getOptions(self, doubleAllowed=True)
            mrxOptions = [option for option in mrxOptions if option[0] == 'double']
            if self.cards['black'] >= 2:  # we need a minimum of 2 black cards, since it is possible to take the ferry and then play a black card
                mrxOptions += [(option[0], option[1], (option[2][0], 'black')) for option in mrxOptions]
            self.print_(f"{self} his double move options are: {mrxOptions}")
            # give scores based on the resulting number of possible positions for a double move
            scores = [(option, len(self.game.board.possiblePositions(option[1][0], [option[2][1]]))) for option in mrxOptions]
            self.print_(f"Scores for each option are: {[score[1] for score in scores]}")
            bestOptions = [tuple[0] for tuple in scores if tuple[1] == max([score[1] for score in scores])]
            self.print_(f"Options with maximal score: {bestOptions}")
            if bestOptions:
                decision = random.choice(bestOptions)
                self.print_(f"{self} chose to move from {self.position} to {decision[1][0]} via {decision[1][1]} then to {decision[2][0]} via {decision[2][1]}")
                return 'double', [decision[1][0], decision[1][1], decision[2][0], decision[2][1]]
            if not bestOptions:
                return None, None

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
        self.print_(f"Options with maximal scores: {bestOptions}")

        # choose random option from options with maximal scores
        if bestOptions:
            decision = random.choice(bestOptions)
        if not bestOptions:
            return None, None

        if len(self.history) in [4, 9, 14, 19] and self.cards['black'] > 0 and any(el in [option[1] for option in mrxOptions] for el in ['bus', 'underground']):
            decision = (decision[0], 'black')

        if decision[1] in ['bus', 'underground'] and (decision[0], 'taxi') in mrxOptions:
            decision = (decision[0], 'taxi')
        self.print_(f"{self} chose to move from {self.position} to {decision[0]} via {decision[1]}")
        return decision[0], decision[1]
