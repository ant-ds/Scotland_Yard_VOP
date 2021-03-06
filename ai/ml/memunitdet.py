

class MemUnitDet():
    """
    Class to hold information for 1 training unit
    """
    def __init__(self):
        # current state
        self.currDetState = None

        # action
        self.action = (None, None)

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
        print(f'Possible action: {self.nextPossActions}')


class MemUnitMrX():
    def __init__(self):
        # currents state
        self.currMrXState = None

        # action
        self.action = (None, None)

        # reward
        self.reward = 0

        # next state
        self.nextMrXState = None

        # actions possible in next state
        self.nextPossActions = []
    
    def display(self):
        print('Displaying MemUnitDet')
        self.currMrXState.display()
        print(f'Action: {self.action}')
        print(f'Reward: {self.reward}')
        self.nextMrXState.display()
        print(f'Possible Action: {self.nextPossActions}')