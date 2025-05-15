import csv
import os
import time
from ConnectState import ConnectState
from mcts import MCTS, WeakMCTS
from random_ai import RandomAI

def flatten_board(board):
    return [cell for row in board for cell in row]

def generate_training_data(num_games, output_file, strong_time=1, weak_time=0.2):
    file_exists = os.path.isfile(output_file)

    with open(output_file, 'a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            # Escreve o cabeçalho apenas se o arquivo for novo
            writer.writerow([f'cell_{i}' for i in range(42)] + ['to_play', 'label'])

        for game_num in range(num_games):
            print(f"[{time.strftime('%H:%M:%S')}] Iniciando jogo {game_num + 1}...")
            state = ConnectState()

            # Alterna quem será o MCTS forte
            mcts_player = 1 if game_num % 2 == 0 else 2
            strong_mcts = MCTS(state)
            weak_mcts = WeakMCTS(state)
            # random_ai = RandomAI(state)

            while not state.game_over():
                current_player = state.to_play

                if current_player == mcts_player:
                    strong_mcts.search(strong_time)
                    move = strong_mcts.best_move()
                    board_flat = flatten_board(state.board)
                    writer.writerow(board_flat + [current_player, move])
                else:
                    weak_mcts.search(weak_time)
                    move = weak_mcts.best_move()

                # Aplica a jogada no jogo e sincroniza ambos os AIs
                state.move(move)
                strong_mcts.move(move)
                weak_mcts.move(move)

    print(f"Treinamento salvo em {output_file}")

#rodar indefinidamente por blocos
if __name__ == "__main__":
    while True:
        generate_training_data(num_games=100, output_file="training_data3.csv", strong_time=10, weak_time=2)