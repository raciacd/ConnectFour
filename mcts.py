import random
import time
import math
from copy import deepcopy

from ConnectState import ConnectState
from meta import GameMeta, MCTSMeta


class Node: #Represents a node in the tree
    def __init__(self, move, parent):
        self.move = move #Move that generated this node
        self.parent = parent
        self.N = 0 #Number of times the node was visited
        self.Q = 0 #Number of wins reached from this node
        self.children = {} #Represents the next possible moves
        self.outcome = GameMeta.PLAYERS['none'] #Game state

    def add_children(self, children: dict) -> None: #Adds multiple nodes to the current one
        for child in children:
            self.children[child.move] = child

    def value(self, explore: float = MCTSMeta.EXPLORATION): #Applies the Upper Confidence bounds applied to Trees to evaluate the node
        if self.N == 0:
            return 0 if explore == 0 else GameMeta.INF
        else:
            return self.Q / self.N + explore * math.sqrt(math.log(self.parent.N) / self.N)


class MCTS: #Initialize MCTS with the current game state (creates the root)
    def __init__(self, state=ConnectState()):
        self.root_state = deepcopy(state) #Copies the game state so we don't modify the original game
        self.root = Node(None, None)
        self.run_time = 0
        self.node_count = 0
        self.num_rollouts = 0

    def select_node(self) -> tuple: #Selects a node so it can traverse it until finding a new node or leaf
        node = self.root
        state = deepcopy(self.root_state)

        while len(node.children) != 0: #Looks for highest value children in the visited nodes
            children = node.children.values()
            max_value = max(children, key=lambda n: n.value()).value()
            max_nodes = [n for n in children if n.value() == max_value]

            node = random.choice(max_nodes)
            state.move(node.move)

            if node.N == 0:
                return node, state

        if self.expand(node, state):
            node = random.choice(list(node.children.values())) #Picks a newly expanded node
            state.move(node.move)

        return node, state

    def expand(self, parent: Node, state: ConnectState) -> bool: #Adds children based on all possible moves
        if state.game_over():
            return False

        children = [Node(move, parent) for move in state.get_legal_moves()]
        parent.add_children(children)

        return True

    def roll_out(self, state: ConnectState) -> int: #Plays the game with random moves until reaching an end result
        while not state.game_over():
            state.move(random.choice(state.get_legal_moves()))

        return state.get_outcome()

    def back_propagate(self, node: Node, turn: int, outcome: int) -> None: #Propagates back to the root and adds points as rewards for victories

        #For the current player, not the next player
        reward = 0 if outcome == turn else 1

        while node is not None:
            node.N += 1
            node.Q += reward
            node = node.parent
            if outcome == GameMeta.OUTCOMES['draw']:
                reward = 0
            else:
                reward = 1 - reward

    def search(self, time_limit: int): #Define a time limit for playing the simulations of the game (in cpu seconds to avoid machine interference).
        #Can be change to time.time() to choose real time
        start_time = time.process_time()

        num_rollouts = 0
        while time.process_time() - start_time < time_limit:
            node, state = self.select_node()
            outcome = self.roll_out(state)
            self.back_propagate(node, state.to_play, outcome)
            num_rollouts += 1

        run_time = time.process_time() - start_time
        self.run_time = run_time
        self.num_rollouts = num_rollouts

    def best_move(self): #Chooses the node with most visits (during the UCT simulations)
        if self.root_state.game_over():
            return -1

        max_value = max(self.root.children.values(), key=lambda n: n.N).N
        max_nodes = [n for n in self.root.children.values() if n.N == max_value]
        best_child = random.choice(max_nodes)

        return best_child.move

    def move(self, move): #Updates the tree with new moves
        if move in self.root.children:
            self.root_state.move(move)
            self.root = self.root.children[move]
            return

        self.root_state.move(move)
        self.root = Node(None, None)

    def statistics(self) -> tuple: #Returns the number of simulations and time elapsed
        return self.num_rollouts, self.run_time
