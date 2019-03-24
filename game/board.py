import random

from game.misterx import MisterX

import game.util as util
import game.constants as const


class Board():
    def __init__(self, size, game=None):
        self.size = size
        self.game = game
        self.graph = util.createGraph(size)

        self._usedStartingPositions = []  # Makes sure no two players start on the same spot

    def giveStartPosition(self, playertype):
        """
        Assigns a starting position to a new player.
        """
        if 'detective' in playertype.__name__.lower():
            playertype = 'detectives'
        elif 'misterx' in playertype.__name__.lower():
            playertype = 'mrx'
        else:  # temporary
            raise ValueError("Jonas lets you know that your Player class was maybe not correctly recognized. Please send him a message or fix it yourself :)")
        
        pos = random.choice(const.START_POSITIONS[playertype])

        while pos in self._usedStartingPositions:
            pos = random.choice(const.START_POSITIONS[playertype])
        self._usedStartingPositions.append(pos)
        return pos
    
    # def draw(self):
    #     util.drawGraph(self.graph)
    
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
        "Returns currently occupied positions"
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
    
    def possiblePositions(self, start, moves=[], occupied=None, refuseCurrent=False, returnProbabilities=False, startprob=1):
        """
        Returns a list of possible locations a player could have moved to with the given
        list containing means of transport used.
        """
        options = [start]
        probs = {start: startprob}
        for i, move in enumerate(moves):
            newOptions = []  # new list of possible locations
            newProbs = {}
            
            for position in options:
                if position in occupied[i]:
                    # "Rejected {position} as a position of further exploration"
                    if i > 0:
                        occupied[i - 1].append(position)
                        return self.possiblePositions(
                            start, 
                            moves=moves, 
                            occupied=occupied, 
                            refuseCurrent=refuseCurrent, 
                            returnProbabilities=returnProbabilities, 
                            startprob=startprob
                        )
                    continue
                
                nbrs = []
                for nbr in self.graph[position]:
                    for k, transportDict in self.graph.get_edge_data(position, nbr).items():  # edge data is a dict of dicts
                        transport = transportDict['transport']
                        if move == transport or move == 'black':  # black move could be any move
                            if occupied is None or nbr not in occupied[i]:
                                if refuseCurrent is False or not (i == len(moves) - 1 and nbr in [d.position for d in self.game.detectives]):
                                    nbrs.append(nbr)
                newOptions += nbrs
                for nbr in nbrs:
                    if nbr not in newProbs.keys():
                        newProbs[nbr] = 0
                    newProbs[nbr] += probs[position] * 1.0 / float(len(nbrs))
            
            options = list(set(newOptions))  # eliminate doubles each iteration
            probs = util.dictMergeAdd(newProbs, {})
        
        if returnProbabilities:
            return sorted(options), probs
        return sorted(options)  # sort in ascending order

    def possibleMisterXPositions(self, returnProbabilities=False):
        """
        Returns a list of possible locations Mister X could be hiding.
        The parameter returnProbabilities enables the return of a dict
        mapping each option to its probability of being occupied.
        """
        # TODO: handle deaths and look into weird behaviour after a few reveals
        def getprohibited(start):
            print(f"Getting prohibited from {start} out:")
            prohibited = []
            for d in self.game.detectives:
                print(f"{d}'s history: {d.history}")
                if len(d.history) == start:
                    if start == 0:
                        dpositions = [d.position]
                    else:
                        dpositions = [d.history[-1][-1]]
                    """<<-- elif len(d.history) == start - 1:
                        print("elif case!")
                        dpositions = [d.history[-1][-1]]"""
                else:
                    dpositions = [d.history[start][0]]
                    dpositions += [h[-1] for h in d.history[start:]]
                for i, p in enumerate(dpositions):
                    if len(prohibited) == i:
                        prohibited.append([])
                    prohibited[i].append(p)
                print(f"Currently prohibited: {prohibited}")
            # Account for double moves, where the prohibited positions should be duplicated
            for double in mrx.doubleMoves:
                i = double - start - len(mrx.doubleMoves)
                if i >= 0:
                    prohibited.insert(i, prohibited[i])
            return prohibited

        mrx = self.game.misterx
        turn = len(mrx.history)  # current turn
        start = mrx.lastKnownPosition
        options = []
        probabilities = {}

        if start is None:
            # No reveal has yet happened
            moves = [hist[1] for hist in mrx.history]
            prohibited = getprohibited(0)
            for s in const.START_POSITIONS['mrx']:
                newops, probs = self.possiblePositions(
                    s, 
                    moves=moves, 
                    occupied=prohibited,
                    refuseCurrent=True,
                    returnProbabilities=True, 
                    startprob=1.0 / float(len(const.START_POSITIONS['mrx']))
                )
                options += newops
                probabilities = util.dictMergeAdd(probabilities, probs)
            options = sorted(list(set(options)))  # make unique and sort in ascending order
        else:
            # Look up the most recent reveal and slice the history accordingly
            sliceStart = max([i for i in const.MRX_OPEN_TURNS if i <= turn])
            moves = [hist[1] for hist in mrx.history[sliceStart:]]
            prohibited = getprohibited(sliceStart - len(mrx.doubleMoves))  # Account for double moves disrupting the indices
            options, probabilities = self.possiblePositions(
                start, 
                moves=moves, 
                occupied=prohibited,
                refuseCurrent=True,
                returnProbabilities=True
            )
        if returnProbabilities:
            return options, probabilities
        return options
