import random


class Board():
    def __init__(self, size):
        self.size = size

        self.graph = None  # Init graph with given size  TODO

        self._usedStartingPositions = []  # Makes sure no two players start on the same spot

    def giveStartPosition(self):
        """
        Assigns a starting position to a new player.
        """
        pos = random.randint(1,150)  # temporary
        while pos in self._usedStartingPositions:
            pos = random.randint(1,150)  # temporary
        self._usedStartingPositions.append(pos)
        return pos