import numpy as np

class StateMachine:

    def __init__(self):
        self.GOING = 0
        self.CLOSE = 1
        self.STOPPED = 2
        self.state = self.GOING
