class Player():
    def __init__(self, game, name, busCard, taxiCard, undergroundCard):
        self.name = name
        self.game = game

        self.position = self.game.getStartPosition()

        self.busCard = busCard
        self.taxiCard = taxiCard
        self.undergroundCard = undergroundCard

        self.history = []

    def update(self):
        pass
