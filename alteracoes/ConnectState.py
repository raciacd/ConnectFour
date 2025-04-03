from copy import deepcopy
import numpy as np
from meta import GameMeta

class ConnectState:
    def __init__(self):
        self.board = np.zeros((GameMeta.ROWS, GameMeta.COLS), dtype=np.int8)
        self.to_play = GameMeta.PLAYERS['one']
        self.height = np.full(GameMeta.COLS, GameMeta.ROWS - 1, dtype=np.int8)
        self.last_played = np.array([-1, -1], dtype=np.int8)

    def get_board(self):
        return self.board.copy()

    def move(self, col):
        self.board[self.height[col], col] = self.to_play
        self.last_played = np.array([self.height[col], col], dtype=np.int8)
        self.height[col] -= 1
        self.to_play = GameMeta.PLAYERS['two'] if self.to_play == GameMeta.PLAYERS['one'] else GameMeta.PLAYERS['one']

    def get_legal_moves(self):
        return np.where(self.board[0] == 0)[0].tolist()

    def check_win(self):
        if self.last_played[0] >= 0 and self.check_win_from(self.last_played[0], self.last_played[1]):
            return self.board[self.last_played[0], self.last_played[1]]
        return 0

    def copy(self):
        new_state = ConnectState()
        new_state.board = self.board.copy()
        new_state.to_play = self.to_play
        new_state.height = self.height.copy()
        new_state.last_played = self.last_played.copy()
        return new_state

    def check_win_from(self, row, col):
        player = self.board[row, col]
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for dr, dc in directions:
            count = 1
            for step in (1, -1):
                r, c = row + dr * step, col + dc * step
                while 0 <= r < GameMeta.ROWS and 0 <= c < GameMeta.COLS and self.board[r, c] == player:
                    count += 1
                    if count >= 4:
                        return True
                    r += dr * step
                    c += dc * step
        return False

    def game_over(self):
        return self.check_win() or len(self.get_legal_moves()) == 0

    def get_outcome(self):
        if len(self.get_legal_moves()) == 0 and self.check_win() == 0:
            return GameMeta.OUTCOMES['draw']
        return GameMeta.OUTCOMES['one'] if self.check_win() == GameMeta.PLAYERS['one'] else GameMeta.OUTCOMES['two']

    def print(self):
        print('=============================')
        for row in range(GameMeta.ROWS):
            for col in range(GameMeta.COLS):
                print('|{} '.format('🔵' if self.board[row, col] == 1 else '🔴' if self.board[row, col] == 2 else '  '), end='')
            print('|')
        print('=============================')
        print('  1 | 2 | 3 | 4 | 5 | 6 | 7  ')