import re
import copy
import game.constants as const


class Player():
    def __init__(self, game, name, busCard, taxiCard, undergroundCard):
        self.name = name
        self.game = game

        if self.game.isclone:
            self.position = None
        else:
            self.position = self.game.board.giveStartPosition(type(self))
        
        self.cards = {
            'bus': busCard,
            'taxi': taxiCard,
            'underground': undergroundCard,
        }
        self.originalCards = copy.deepcopy(self.cards)

        self.history = []  # format: (startPosition, transport, destination)
        self.defeated = False

    def update(self):
        nextReveal = min([revturn for revturn in const.MRX_OPEN_TURNS if revturn >= self.turn])

        self.print_("-------------------------------------")
        self.print_(f"Currently playing turn {self.turn}; Next reveal on turn {nextReveal}")
        self.print_(f"{self}'s turn")
        self.print_(f"Current position: {self.position}")

        dest, transport = self.decide()
        status, issue = self.move(dest, transport)
        if status is None:
            return self._defeated()
        while not status:
            self.print_(f"That move was invalid: {issue}")
            dest, transport = self.decide()
            status, issue = self.move(dest, transport)
            if status is None:
                return self._defeated()

        self._printCards()
        self.print_(f"{self} ended his turn on position {self.position}")

        return True  # if everything in update went smooth, return True

    def decide(self):
        """
        Decide which position to move to next.
        Returns a tuple of (destination, transportation used to get there)
        Basic interactive implementation, should be overwritten by superclasses.
        """

        options = self.game.board.getOptions(self)
        options = sorted(options, key=lambda x: x[0] == 'double')  # display single moves first
        self.print_(f"Your options are:: {options}")

        dest, transport = self._getInput()

        if dest is None and transport is None:
            return None, None  # player will be defeated after this

        if dest == 'double' and len(transport) == 4:
            transport[0] = int(transport[0])
            transport[2] = int(transport[2])

        try:
            dest = int(dest)
        except ValueError:
            self.print_(f"Destination recieved was not a valid destination")

        self.print_(f"{self} chose to move from {self.position} to {dest} via {transport}")

        return dest, transport

    def move(self, destination, transport):
        """
        Very simple implementation, no checks on possibility of move.
        """
        status, issue = self.game.board.movePlayer(self, destination, transport)
        
        return status, issue

    def getTransportName(self, transport):
        """Some cards can be used for multiple purposes, but are only kept track of once,
        returns correct internal naming for this player instance"""
        if transport == 'ferry':
            return 'black'
        return transport
    
    def _defeated(self):
        self.defeated = True
        return False
    
    @property
    def turn(self):
        return len(self.history)
    
    def _getInput(self):
        while True:
            recieved = input("What is your destination and how do you plan to get there?  ")
            inputs = re.findall(r"[\w']+", recieved)  # can handle commas, spaces, ...
            
            if inputs == []:
                continue
        
            if inputs[0] == 'double':
                if len(inputs) == 5:
                    break
                else:
                    self.print_("Wat doink?")
            elif inputs[0] == 'suicide':
                return None, None
            else:
                if len(inputs) == 2:
                    break
                else:
                    self.print_("Your input was invalid. Please try again:")
                    continue
        return inputs[0], inputs[1:]

    def _printCards(self):
        "Displays the cards this player is currently in possession of."
        self.game.print_(self.cards)

    def __str__(self):
        return self.name

    def print_(self, msg):
        self.game.print_(msg)

    def overwriteCards(self, cards: dict):
        d = {}
        for k, v in cards.items():
            d[k] = v
        self.cards = d

    def cloneFrom(self, old):
        # Overwrite all fields
        self.game = old.game
        self.name = old.name
        self.position = old.position
        self.overwriteCards(old.cards)
        self.history = [tuple([h for h in move]) for move in old.history]

    def clone(self):
        new = Player(self.game, self.name, self.cards['bus'], self.cards['taxi'], self.cards['underground'])
        new.cloneFrom(self)
        return new

    def reset(self):
        self.cards = copy.deepcopy(self.originalCards)
        self.history = []
        self.position = self.game.board.giveStartPosition(type(self))
        self.defeated = False
