import random

from game.misterx import MisterX

import game.util as util
import game.constants as const


class Board():
    def __init__(self, size, game=None):
        self.size = size
        self.game = game
        self.graph = util.createGraph(size)

    def assignStartPositions(self):
        """
        Assigns a starting position to all players currently linked to the game.
        """
        assignedPositions = []  # Makes sure no two players start on the same spot
        mrxOptions = [pos for pos in const.START_POSITIONS['mrx'] if pos <= self.size and pos not in assignedPositions]

        pos = random.choice(mrxOptions)
        self.game.misterx.position = pos

        indices = [i for i in range(len(self.game.detectives))]
        random.shuffle(indices)
        detOptions = [pos for pos in const.START_POSITIONS['detectives'] if pos <= self.size and pos not in assignedPositions]
        for i in indices:  # Randomly shuffled detectives (indices)
            pos = random.choice(detOptions)
            assignedPositions.append(pos)
            self.game.detectives[i].position = pos
            # recalculate options (avoids while loop and unnecessary trying which could occur for a small sized board)
            detOptions = [pos for pos in const.START_POSITIONS['detectives'] if pos <= self.size and pos not in assignedPositions]
        
        self.print_(f"Starting Positions: Mister X: {self.game.misterx.position}; Detectives: {[d.position for d in self.game.detectives]}")
    
    def getOptions(self, player, customStartPosition=None, doubleAllowed=True):
        """
        returns a list of nodes neighbouring the given position on the board
        accompanied by the mode of transportation needed to reach said neighbour.

        Parameter doubleAllowed prevents infinite recursion by setting it to False with a recursive call.
        """
        if customStartPosition is not None and isinstance(customStartPosition, int):
            startPosition = customStartPosition
        else:
            startPosition = player.position
        
        options = []
        
        # for nbr in G[n]: iterates through neighbors
        for nbr in self.graph[startPosition]:
            for k, transportDict in self.graph.get_edge_data(startPosition, nbr).items():  # edge data is a dict of dicts
                transport = transportDict['transport']
                try:  # Sometimes a black Card check can be performed on a Detective
                    hasCard = player.cards[player.getTransportName(transport)] > 0
                except KeyError:
                    hasCard = False
                if hasCard and nbr not in [d.position for d in self.game.detectives]:
                    options.append((nbr, transport))

        if doubleAllowed and isinstance(player, MisterX) and player.cards['double'] > 0:  # Double move
            optionsSet = set(options)
            for option in options:
                newStart = option[0]
                newOptions = self.getOptions(player, customStartPosition=newStart, doubleAllowed=False)  # recursive call for each option
                newOptionsSet = set()
                for newOption in newOptions:
                    newOptionsSet.add(('double', option, newOption))
                optionsSet = optionsSet.union(newOptionsSet)
            options = list(optionsSet)           
        
        return options

    def getOccupiedPositions(self):
        positions = [self.game.misterx.position]
        positions += [d.position for d in self.game.detectives]
        return positions

    def movePlayer(self, player, destination, transport):
        """
        Checks if the proposed move is valid based on the current position on the board.
        Also hands over used cards to Mr. X
        """

        if destination == 'double':
            return self._doubleMovePlayer(player, transport)
        elif isinstance(transport, list):
            transport = transport[0]
        
        if destination is None and transport is None:
            return None, None  # Suicide-move

        # Is the proposed destination an option?
        options = self.getOptions(player)
        tup = (destination, transport)
        if not util.isOption(options, tup):
            return False, f"{tup} was not an option in {options}"
        
        # Is the destination not occupied by a detective?
        if destination in [d.position for d in self.game.detectives]:
            return False, "The destination chosen is already occupied"
        
        transport = player.getTransportName(transport)  # Convert to correct naming convention inside player instance

        # Is a ticket available for the transportation needed?
        if not player.cards[transport] > 0:
            return False, f"You do not have enough tickets for the {transport}"
        
        startPosition = player.position
        player.position = destination
        player.cards[transport] -= 1

        # Record the move in player's history
        player.history.append((startPosition, transport, destination))

        # Give the used card to Mr. X, except for black and doubles
        if transport not in ['black', 'double']:
            self.game.misterx.cards[transport] += 1

        return True, None
    
    def _doubleMovePlayer(self, player, moves):
        tup = ('double', (moves[0], moves[1]), (moves[2], moves[3]))
        options = self.getOptions(player)
        if not util.isOption(options, tup):
            return False, f"{tup} was not an option in {options}"
        
        if not player.cards['double'] > 0:
            return False, f"You do not have any double move tickets left!"
        
        for i in [0, 2]:
            # for both moves
            dest, transport = moves[i], moves[i + 1]
            status, issue = self.movePlayer(player, dest, transport)
            if not status:
                self._resetCards(player, turns=i)
                return status, issue
        
        player.cards['double'] -= 1
        player.doubleMoves.append(len(player.history) - 2)  # index in history for first of the double move
        return True, None

    def _resetCards(self, player, turns=1):
        """
        Resets a given player's cards for x amount of turns based on the player's history.
        """
        if turns < 1:
            return
        else:
            # turns >= 1
            lastMoves = player.history[-turns:]  # last 'turns' moves
            for move in lastMoves:
                # move looks like: (start, transport, destination)
                transport = player.getTransportName(move[1])  # Convert to correct naming convention inside player instance
                player.position = move[0]
                player.cards[transport] += 1
    
    def possiblePositions(self, start, moves=[]):
        """
        Returns a list of possible locations a player could have moved to with the given
        list containing means of transport used.
        """
        options = [start]
        for move in moves:
            newOptions = []  # new list of possible locations
            for position in options:
                for nbr in self.graph[position]:
                    for k, transportDict in self.graph.get_edge_data(position, nbr).items():  # edge data is a dict of dicts
                        transport = transportDict['transport']
                        if move == transport or move == 'black':  # black move could be any move
                            newOptions.append(nbr)
            options = list(set(newOptions))  # eliminate doubles for performance
        
        return sorted(options)  # sort in ascending order

    def possibleMisterXPositions(self):
        mrx = self.game.misterx
        start = mrx.lastKnownPosition
        options = []

        if start is None:
            moves = [hist[1] for hist in mrx.history]
            for s in const.START_POSITIONS['mrx']:
                options += self.possiblePositions(s, moves=moves)
            return sorted(list(set(options)))  # sort in ascending order and make unique
        
        sliceStart = 0

        for i in const.MRX_OPEN_TURNS:
            try:
                _ = mrx.history[i - 1][2]  # history has format (start, transport, dest)
                sliceStart = i
            except IndexError:  # once index too high, return last confirmed value
                break
        moves = [hist[1] for hist in mrx.history[sliceStart:]]
        return self.possiblePositions(start, moves=moves)

    def print_(self, msg):
        self.game.print_(msg)
