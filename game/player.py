class Player():
    def __init__(self, game, name, busCard, taxiCard, undergroundCard):
        self.name = name
        self.game = game

        self.position = self.game.board.giveStartPosition()

        """self.busCard = busCard
        self.taxiCard = taxiCard
        self.undergroundCard = undergroundCard"""
        
        self.cards = [busCard, taxiCard, undergroundCard]
        self._cardTypes = ['bus', 'taxi', 'underground']

        self.history = []

    def update(self):
        dest, transport = self.decide()
        self.move(dest, transport)
    
    def decide(self):
        """
        Decide which position to move to next.
        Returns a tuple of (destination, transportation used to get there)
        Basic interactive implementation, should be overwritten by superclasses.
        """
        dest, transport = input("What is your destination and how do you get there?  ").split()
        
        try:
            transport = int(transport)
        except ValueError:
            transport = self._cardTypes.index(transport)  # keep track of the index instead of the human readable string

        assert(0 <= transport < len(self._cardTypes))  # TODO: assert destination is valid, maybe though board API?

        print(f"{self} chose to move from {self.position} to {dest} by {self._cardTypes[transport]}")

        return dest, transport

    
    def move(self, destination, transport):
        """
        Very simple implementation, no checks on possibility of move.
        """
        self.position = destination
        self.cards[transport] -= 1

        self._printCards()
    
    def _printCards(self):
        text = f"{self} now holds the following cards: "
        for i, card in enumerate(self._cardTypes):
            text += f"{(card, self.cards[i])}"
        print(text)
    
    def __str__(self):
        return self.name

        
