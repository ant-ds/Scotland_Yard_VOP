from game.misterx import MisterX

class ExampleAIImplementationMisterX(Misterx):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    # Should return a tuple (destination:int, transportation:string)
    def decide(self):
        return 153, 'taxi'
