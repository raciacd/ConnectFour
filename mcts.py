import random
import time
import math
from datetime import datetime

from ConnectState import ConnectState
from meta import GameMeta, MCTSMeta


class Node:
    def __init__(self, move, parent):
        self.move = move
        self.parent = parent
        self.N = 0
        self.Q = 0
        self.children = {}
        self.outcome = GameMeta.PLAYERS['none']

    def value(self, explore: float = MCTSMeta.EXPLORATION):
        if self.N == 0:
            return 0 if explore == 0 else GameMeta.INF
        else:
            return self.Q / self.N + explore * math.sqrt(math.log(self.parent.N) / self.N)


class MCTS:
    def __init__(self, state=ConnectState()):
        self.root_state = state.clone()
        self.root = Node(None, None)
        self.run_time = 0
        self.node_count = 0
        self.num_rollouts = 0
        self.num_states_generated = 0

    def select_node(self):
        node = self.root
        state = self.root_state.clone()

        while node.children:
            children = node.children.values()
            max_value = max(children, key=lambda n: n.value()).value()
            max_nodes = [n for n in children if n.value() == max_value]
            node = max_nodes[0] if len(max_nodes) == 1 else random.choice(max_nodes)
            state.move(node.move)
            self.num_states_generated += 1

            if node.N == 0:
                return node, state

        legal_moves = state.get_legal_moves()
        if not legal_moves or state.game_over():
            return node, state

        move = random.choice(legal_moves)
        child = Node(move, node)
        node.children[move] = child
        state.move(move)
        self.num_states_generated += 1
        return child, state

    def roll_out(self, state: ConnectState, max_depth=20):
        depth = 0
        while not state.game_over() and depth < max_depth:
            legal_moves = state.get_legal_moves()
            best_move = None

            # 1. Jogada de vitória imediata
            for move in legal_moves:
                sim = state.clone()
                sim.move(move)
                if sim.check_win() == state.to_play:
                    best_move = move
                    break

            if best_move is None:
                # 2. Bloquear vitória do adversário
                opponent = GameMeta.PLAYERS['two'] if state.to_play == GameMeta.PLAYERS['one'] else GameMeta.PLAYERS['one']
                for move in legal_moves:
                    sim = state.clone()
                    sim.to_play = opponent
                    sim.move(move)
                    if sim.check_win() == opponent:
                        best_move = move
                        break
            
            if best_move is None:
                scored_moves = []
                for move in legal_moves:
                    sim = state.clone()
                    sim.move(move)
                    score = self._count_consecutive(sim, move, state.to_play)
                    scored_moves.append((score, move))

                if scored_moves:
                    scored_moves.sort(reverse=True)
                    _, best_move = scored_moves[0]

            if best_move is None:
                # 4. Prioridade ao centro
                center = GameMeta.COLS // 2
                if center in legal_moves:
                    best_move = center
                else:
                    # 5. Jogada mais próxima do centro
                    best_move = sorted(legal_moves, key=lambda x: abs(x - center))[0]
            
            if best_move not in legal_moves:
                # Fallback de emergência
                best_move = random.choice(legal_moves)

            state.move(best_move)
            self.num_states_generated += 1
            depth += 1

        return state.get_outcome()

    def search(self, time_limit: int):
        legal_moves = self.root_state.get_legal_moves()
        current_player = self.root_state.to_play
        opponent = GameMeta.PLAYERS['two'] if current_player == GameMeta.PLAYERS['one'] else GameMeta.PLAYERS['one']

        for move in legal_moves:
            simulated = self.root_state.clone()
            simulated.move(move)
            if simulated.check_win() == current_player:
                self.root.children[move] = Node(move, self.root)
                self.root.children[move].N = 1_000_000
                self.num_rollouts = 0
                self.run_time = 0
                self.num_states_generated = 0
                return

        for move in legal_moves:
            simulated = self.root_state.clone()
            simulated.to_play = opponent
            simulated.move(move)
            if simulated.check_win() == opponent:
                self.root.children[move] = Node(move, self.root)
                self.root.children[move].N = 500_000
                self.num_rollouts = 0
                self.run_time = 0
                self.num_states_generated = 0
                return

        start_time = time.process_time()
        last_time_check = time.time()
        rollouts_this_second = 0
        total_rollouts = 0
        self.num_states_generated = 0

        print("Iniciando MCTS com estatísticas ao vivo...")

        while time.process_time() - start_time < time_limit:
            node, state = self.select_node()
            outcome = self.roll_out(state)

            # Estratégica retropropagação
            reward = 1 if outcome == self.root_state.to_play else 0
            if outcome == GameMeta.OUTCOMES['draw']:
                reward = 0.5
            temp = node
            while temp:
                temp.N += 1
                temp.Q += reward
                reward = 1 - reward if outcome != GameMeta.OUTCOMES['draw'] else 0.5
                temp = temp.parent

            rollouts_this_second += 1
            total_rollouts += 1

            now = time.time()
            if now - last_time_check >= 1:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Iterações por segundo: {rollouts_this_second}")
                rollouts_this_second = 0
                last_time_check = now

        self.run_time = time.process_time() - start_time
        self.num_rollouts = total_rollouts

    def best_move(self):
        if (self.root_state.to_play == GameMeta.PLAYERS['one'] and 
            all(cell == 0 for row in self.root_state.board for cell in row)):
            return GameMeta.COLS // 2

        if self.root_state.game_over():
            return -1

        max_value = max(self.root.children.values(), key=lambda n: n.N).N
        max_nodes = [n for n in self.root.children.values() if n.N == max_value]
        best_child = random.choice(max_nodes)
        return best_child.move

    def move(self, move):
        if move in self.root.children:
            self.root_state.move(move)
            self.root = self.root.children[move]
        else:
            self.root_state.move(move)
            self.root = Node(None, None)

    def statistics(self) -> tuple:
        return self.num_rollouts, self.run_time, self.num_states_generated
    
    def _count_consecutive(self, state, col, player):
        row = state.last_played[0]
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        score = 0

        for dr, dc in directions:
            count = 1
            for step in range(1, 3):
                r, c = row + dr * step, col + dc * step
                if 0 <= r < GameMeta.ROWS and 0 <= c < GameMeta.COLS and state.board[r][c] == player:
                    count += 1
                else:
                    break
            if count == 2:
                score += 10
            elif count == 3:
                score += 50

        return score


# Adicionar este método à classe ConnectState:
def connectstate_clone(self):
    new_state = ConnectState()
    new_state.board = [row[:] for row in self.board]
    new_state.to_play = self.to_play
    new_state.height = self.height[:]
    new_state.last_played = self.last_played[:]
    return new_state

ConnectState.clone = connectstate_clone
