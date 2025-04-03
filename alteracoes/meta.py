import math

class GameMeta:
    PLAYERS = {'none': 0, 'one': 1, 'two': 2} #0: vazio, 1: azul, 2: vermelho
    OUTCOMES = {'none': 0, 'one': 1, 'two': 2, 'draw': 3}
    INF = float('inf') #infinito
    ROWS = 6
    COLS = 7


class MCTSMeta:
    EXPLORATION = math.sqrt(2) #constante do UCB