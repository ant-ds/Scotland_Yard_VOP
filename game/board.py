import random

import game.graph as g


class Board():
    def __init__(self, size, game=None):
        self.size = size
        self.game = game
        self.graph = g.createGraph(size)

        self._usedStartingPositions = []  # Makes sure no two players start on the same spot

    def giveStartPosition(self):
        """
        Assigns a starting position to a new player.
        """
        pos = random.randint(1, self.size)  # temporary
        while pos in self._usedStartingPositions:
            pos = random.randint(1, self.size)  # temporary
        self._usedStartingPositions.append(pos)
        return pos
    
    def draw(self):
        g.drawGraph(self.graph)
    
    def getOptions(self, startPosition):
        """
        returns a list of nodes neighbouring the given position on the board
        accompanied by the mode of transportation needed to reach said neighbour.
        """
        listret = []
        # for nbr in G[n]: iterates through neighbors
        for nbr in self.graph[startPosition]:
            transport = self.graph.get_edge_data(startPosition, nbr)[0]['transport']
            listret.append((nbr, transport))
        return listret

    def getOccupiedPositions(self):
        positions = [self.game.misterx.position]
        positions += [d.position for d in self.game.detectives]
        return positions

    def movePlayer(self, player, destination, transport):
        """
        Checks if the proposed move is valid based on the current position on the board.
        Also hands over used cards to Mr. X
        """

        # Is the proposed destination an option?
        options = self.getOptions(player.position)
        tup = (destination, transport)
        if not tup in options:
            return False, f"{tup} was not an option in {options}"
        
        # Is a ticket available for the transportation needed?
        if not player.cards[transport] > 0:
            return False, f"You do not have enough tickets for the {transport}"

        # Is the destination not occupied by a detective?
        if destination in [d.position for d in self.game.detectives]:
            return False, "The destination chosen is already occupied"

        player.position = destination
        player.cards[transport] -= 1

        # Give the used card to Mr. X
        self.game.misterx.cards[transport] += 1

        return True, None