from copy import deepcopy
import numpy as np
from meta import GameMeta


class ConnectState:
    def __init__(self):
        self.board = [[0] * GameMeta.COLS for _ in range(GameMeta.ROWS)]
        self.to_play = GameMeta.PLAYERS['one']
        self.height = [GameMeta.ROWS - 1] * GameMeta.COLS
        self.last_played = []

    def get_board(self):
        return deepcopy(self.board)

    def move(self, col):
        self.board[self.height[col]][col] = self.to_play
        self.last_played = [self.height[col], col]
        self.height[col] -= 1
        self.to_play = GameMeta.PLAYERS['two'] if self.to_play == GameMeta.PLAYERS['one'] else GameMeta.PLAYERS['one']

    def get_legal_moves(self):
        return [col for col in range(GameMeta.COLS) if self.board[0][col] == 0]

    def check_win(self):
        if len(self.last_played) > 0 and self.check_win_from(self.last_played[0], self.last_played[1]):
            return self.board[self.last_played[0]][self.last_played[1]]
        return 0

    '''def check_win_from(self, row, col):
        player = self.board[row][col]
        """
        Last played action is at (row, col)
        Check surrounding 7x7 grid for a win
        """

        consecutive = 1
        # Check horizontal
        tmprow = row
        while tmprow + 1 < GameMeta.ROWS and self.board[tmprow + 1][col] == player:
            consecutive += 1
            tmprow += 1
        tmprow = row
        while tmprow - 1 >= 0 and self.board[tmprow - 1][col] == player:
            consecutive += 1
            tmprow -= 1

        if consecutive >= 4:
            return True

        # Check vertical
        consecutive = 1
        tmpcol = col
        while tmpcol + 1 < GameMeta.COLS and self.board[row][tmpcol + 1] == player:
            consecutive += 1
            tmpcol += 1
        tmpcol = col
        while tmpcol - 1 >= 0 and self.board[row][tmpcol - 1] == player:
            consecutive += 1
            tmpcol -= 1

        if consecutive >= 4:
            return True

        # Check diagonal
        consecutive = 1
        tmprow = row
        tmpcol = col
        while tmprow + 1 < GameMeta.ROWS and tmpcol + 1 < GameMeta.COLS and self.board[tmprow + 1][tmpcol + 1] == player:
            consecutive += 1
            tmprow += 1
            tmpcol += 1
        tmprow = row
        tmpcol = col
        while tmprow - 1 >= 0 and tmpcol - 1 >= 0 and self.board[tmprow - 1][tmpcol - 1] == player:
            consecutive += 1
            tmprow -= 1
            tmpcol -= 1

        if consecutive >= 4:
            return True

        # Check anti-diagonal
        consecutive = 1
        tmprow = row
        tmpcol = col
        while tmprow + 1 < GameMeta.ROWS and tmpcol - 1 >= 0 and self.board[tmprow + 1][tmpcol - 1] == player:
            consecutive += 1
            tmprow += 1
            tmpcol -= 1
        tmprow = row
        tmpcol = col
        while tmprow - 1 >= 0 and tmpcol + 1 < GameMeta.COLS and self.board[tmprow - 1][tmpcol + 1] == player:
            consecutive += 1
            tmprow -= 1
            tmpcol += 1

        if consecutive >= 4:
            return True

        return False'''

    def check_win_from(self, row, col):
        player = self.board[row][col]
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]  #Tuples (dr, dc) for navigating the matrix. Moves a row, column, upwards diagonal and downwards diagonal.

        for dr, dc in directions:
            count = 1 #Starts the count with the piece placed

            # Checks direction dr, dc
            r, c = row + dr, col + dc
            while 0 <= r < GameMeta.ROWS and 0 <= c < GameMeta.COLS and self.board[r][c] == player: #Verifies if the current spot is occupied by the same player who just played. Stops if the spot is empty or occupied by the enemy piece
                count += 1
                r += dr
                c += dc

            # Checks opposite direction (goes backwards)
            r, c = row - dr, col - dc
            while 0 <= r < GameMeta.ROWS and 0 <= c < GameMeta.COLS and self.board[r][c] == player:
                count += 1
                r -= dr
                c -= dc

            if count >= 4: #Condition for win, 4 or more pieces in a row. Can be easily changed to modify the game
                return True

        return False

    def game_over(self):
        return self.check_win() or len(self.get_legal_moves()) == 0

    def get_outcome(self):
        if len(self.get_legal_moves()) == 0 and self.check_win() == 0:
            return GameMeta.OUTCOMES['draw']

        return GameMeta.OUTCOMES['one'] if self.check_win() == GameMeta.PLAYERS['one'] else GameMeta.OUTCOMES['two']

    def print(self):
        #Draws the board
        print('=============================')

        for row in range(GameMeta.ROWS):
            for col in range(GameMeta.COLS):
                print('|{} '.format('🔵' if self.board[row][col] == 1 else '🔴' if self.board[row][col] == 2 else '  '), end='') #Checks every spot for a player chip and displays the correct board
            print('|')
        
        print('=============================')
        print('  1 | 2 | 3 | 4 | 5 | 6 | 7  ')