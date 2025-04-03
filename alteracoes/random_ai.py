import random
from ConnectState import ConnectState

class RandomAI:
    def __init__(self, state: ConnectState):
        self.state = state

    def best_move(self):
        return random.choice(self.state.get_legal_moves())