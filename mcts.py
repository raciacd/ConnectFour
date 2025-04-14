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
        self.num_states_generated = 0

    def select_node(self) -> tuple:
        # Selects a node from the tree, descending by choosing the children with the highest UCT value
        node = self.root
        state = deepcopy(self.root_state)

        while len(node.children) != 0:
            # Selects the child(ren) with the highest UCT value and chooses deterministically or randomly in case of a tie
            children = node.children.values()
            max_value = max(children, key=lambda n: n.value()).value()
            max_nodes = [n for n in children if n.value() == max_value]
            node = max_nodes[0] if len(max_nodes) == 1 else random.choice(max_nodes)
            state.move(node.move)
            self.num_states_generated += 1

            # If the selected node has not been visited yet, end the selection
            if node.N == 0:
                return node, state

        # If there are no visited children, expand the node and select one of the newly created nodes
        if self.expand(node, state):
            node = random.choice(list(node.children.values()))
            state.move(node.move)
            self.num_states_generated += 1

        return node, state

    def expand(self, parent: Node, state: ConnectState) -> bool:
        # Expands a node by adding all possible child nodes from legal moves
        if state.game_over():
            return False

        children = [Node(move, parent) for move in state.get_legal_moves()]
        parent.add_children(children)
        return True

    def roll_out(self, state: ConnectState) -> int:
        # Performs a rollout (simulated game with random moves) until the game ends
        while not state.game_over():
            legal_moves = state.get_legal_moves()
            state.move(random.choice(legal_moves))
            self.num_states_generated += 1

        return state.get_outcome()

    def back_propagate(self, node: Node, turn: int, outcome: int) -> None:
        # Backpropagates the result of the rollout through the tree, alternating the reward for each layer
        reward = 0 if outcome == turn else 1

        while node is not None:
            node.N += 1
            node.Q += reward
            node = node.parent
            if outcome == GameMeta.OUTCOMES['draw']:
                reward = 0
            else:
                reward = 1 - reward

    def search(self, time_limit: int):
        # Performs rollouts within the time limit (in CPU seconds)
        start_time = time.process_time()
        num_rollouts = 0
        self.num_states_generated = 0

        while time.process_time() - start_time < time_limit:
            node, state = self.select_node()
            outcome = self.roll_out(state)
            self.back_propagate(node, state.to_play, outcome)
            num_rollouts += 1

        self.run_time = time.process_time() - start_time
        self.num_rollouts = num_rollouts

    def best_move(self):
        # If it is the 1st move of player one (empty board), return the middle column
        if (self.root_state.to_play == GameMeta.PLAYERS['one'] and 
            all(cell == 0 for row in self.root_state.board for cell in row)):
            return GameMeta.COLS // 2

        # If the game is over, return -1 (no valid move)
        if self.root_state.game_over():
            return -1

        # Selects the node with the highest number of visits among the root's children
        max_value = max(self.root.children.values(), key=lambda n: n.N).N
        max_nodes = [n for n in self.root.children.values() if n.N == max_value]
        best_child = random.choice(max_nodes)
        return best_child.move

    def move(self, move):
        # Updates the search tree with the performed move
        if move in self.root.children:
            self.root_state.move(move)
            self.root = self.root.children[move]
            return

        self.root_state.move(move)
        self.root = Node(None, None)

    def statistics(self) -> tuple:
        # Returns statistics: number of rollouts, total execution time, and generated states
        return self.num_rollouts, self.run_time, self.num_states_generated
