import random
from ConnectState import ConnectState
import pickle
from id3_decision_tree import ID3DecisionTree #########

class RandomAI:
    def __init__(self, state: ConnectState):
        self.state = state

    def best_move(self):
        return random.choice(self.state.get_legal_moves())
    

######!!!!!!!! gera as informacoes pro conect state 

class DecisionTreeAI:
    def __init__(self, model_path="connect4_dt_model.pkl"):
        try:
            with open(model_path, 'rb') as f:
                self.model = pickle.load(f)
        except FileNotFoundError:
            raise Exception("Model not found. Train first with train_dt.py")

    def best_move(self, state):
        features = state.get_features()
        return int(self.model.predict([features])[0])
