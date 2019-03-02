import re


class Player():
    def __init__(self, game, name, busCard, taxiCard, undergroundCard):
        self.name = name
        self.game = game

        self.position = self.game.board.giveStartPosition(type(self))
        
        self.cards = {
            'bus': busCard,
            'taxi': taxiCard,
            'underground': undergroundCard,
        }

        self.history = []  # format: (startPosition, transport, destination)
        self.defeated = False

    def update(self):
        self.print_("-------------------------------------")
        self.print_(f"{self}'s turn")
        self.print_(f"Current position: {self.position}")

        dest, transport = self.decide()
        status, issue = self.move(dest, transport)
        if status is None:
            self._defeated()
            return False
        while not status:
            self.print_(f"That move was invalid: {issue}")
            dest, transport = self.decide()
            status, issue = self.move(dest, transport)
            if status is None:
                self._defeated()
                return False

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
        options = sorted(options, key=lambda x: x[0] == 'double')  # display signgle moves first
        self.print_(f"Your options are:: {options}")

        dest, transport = self._getInput()

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
        startPosition = self.position
        status, issue = self.game.board.movePlayer(self, destination, transport)
        if status:
            self.history.append((startPosition, transport, destination))
        return status, issue

    def getTransportName(self, transport):
        """Some cards can be used for multiple purposes, but are only kept track of once,
        returns correct internal naming for this player instance"""
        return transport

    @property
    def isDefeated(self):
        if self.defeated:
            return True
        
        # TODO
    
    def _defeated(self):
        self.defeated = True
    
    @property
    def turn(self):
        return len(self.history)
    
    def _getInput(self):
        while True:
            recieved = input("What is your destination and how do you plan to get there?  ")
            inputs = re.findall(r"[\w']+", recieved)  # can handle commas, spaces, ...
        
            if inputs[0] == 'double':
                if len(inputs) == 5:
                    break
                else:
                    self.print_("Wat doink?")
            else:
                if len(inputs) == 2:
                    break
                else:
                    self.print_("Your input was invalid. Please try again:")
        return inputs[0], inputs[1:]

    def _printCards(self):
        "Displays the cards this player is currently in possession of."
        self.game.print_(self.cards)
    
    def __str__(self):
        return self.name

    def print_(self, msg):
        self.game.print_(msg)
