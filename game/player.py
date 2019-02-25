class Player():
    def __init__(self, game, name, busCard, taxiCard, undergroundCard):
        self.name = name
        self.game = game

        self.position = self.game.board.giveStartPosition()
        
        self.cards = {
            'bus': busCard,
            'taxi': taxiCard,
            'underground': undergroundCard,
        }

        self.history = []  # TODO: implement tracking of movement: why and in what format?

    def update(self):
        print("-------------------------------------")
        print(f"{self}'s turn")
        print(f"Current position: {self.position}")

        dest, transport = self.decide()
        status, issue = self.move(dest, transport)
        while not status:
            print(f"That move was invalid: {issue}")
            dest, transport = self.decide()
            status, issue = self.move(dest, transport)
        
        self._printCards()
        print(f"{self} ended his turn on position {self.position}")

    def decide(self):
        """
        Decide which position to move to next.
        Returns a tuple of (destination, transportation used to get there)
        Basic interactive implementation, should be overwritten by superclasses.
        """

        options = self.game.board.getOptions(self.position)
        print(f"Your options are:: {options}")

        dest, transport = self._getInput()

        try:
            dest = int(dest)
        except ValueError:
            raise ValueError(f"Destination recieved was not a valid destination")

        assert(transport in self.cards.keys())

        print(f"{self} chose to move from {self.position} to {dest} by {transport}")

        return dest, transport

    def move(self, destination, transport):
        """
        Very simple implementation, no checks on possibility of move.
        """
        return self.game.board.movePlayer(self, destination, transport)        
    
    def _getInput(self):
        return input("What is your destination and how do you get there?  ").split()
    
    def _printCards(self):
        """text = f"{self} now holds the following cards: "
        for i, card in enumerate(self._cardTypes):
            text += f"{(card, self.cards[i])}"
        print(text)"""
        print(self.cards)
    
    def __str__(self):
        return self.name
