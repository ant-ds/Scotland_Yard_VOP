

class MemUnitDet():
    """
    Class to hold information for 1 training unit
    """
    def __init__(self):
        # current state
        self.currDetState = None

        # action
        self.action = []

        # reward
        self.reward = 0

        # next state
        self.nextDetState = None

        # actions possible in next state
        self.nextPossActions = []
    
    def display(self):
        print('Displaying MemUnitDet')
        self.currDetState.display()
        print(f'Action: {self.action}')
        print(f'Reward: {self.reward}')
        self.nextDetState.display()
        print(f'Action: {self.nextPossActions}')