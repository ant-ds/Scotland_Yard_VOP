from game.detective import Detective

class ExampleAIImplementationDetective(Detective):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    # Should return a tuple (destination:int, transportation:string)
    def decide(self):
        return 153, 'taxi'
