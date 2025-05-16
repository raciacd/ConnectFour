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
    strong_wins = 0
    losses = 0
    draws = 0

    with open(output_file, 'a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            # Escreve o cabeçalho apenas se o arquivo for novo
            writer.writerow([f'cell_{i}' for i in range(42)] + ['to_play'] + [f'height_{i}' for i in range(7)] + ['label'])

        for game_num in range(num_games):
            print(f"[{time.strftime('%H:%M:%S')}] Iniciando jogo {game_num + 1}...")
            state = ConnectState()

            # Alterna quem será o MCTS forte
            mcts_player = 1 if game_num % 2 == 0 else 2
            strong_mcts = MCTS(state)
            # weak_mcts = WeakMCTS(state)
            random_ai = RandomAI(state)

            while not state.game_over():
                current_player = state.to_play

                if current_player == mcts_player:
                    strong_mcts.search(strong_time)
                    move = strong_mcts.best_move()
                    board_flat = flatten_board(state.board)
                    writer.writerow(board_flat + [current_player, move])
                else:
                    # weak_mcts.search(weak_time)
                    # move = weak_mcts.best_move()
                    move = random_ai.best_move()

                # Aplica a jogada no jogo e sincroniza ambos os AIs
                state.move(move)
                strong_mcts.move(move)
                # weak_mcts.move(move)

            # Verifica se o strong venceu
            outcome = state.get_outcome()
            if outcome == 3:
                draws += 1
            elif (mcts_player == 1 and outcome == 1) or (mcts_player == 2 and outcome == 2):
                strong_wins += 1
            else:
                losses += 1  # <- agora precisa declarar losses antes também

    total_games = num_games
    losses = total_games - strong_wins - draws
    winrate = (strong_wins / total_games) * 100
    drawrate = (draws / total_games) * 100
    lossrate = (losses / total_games) * 100

    result_text = (
        f"Strong MCTS Stats (último bloco de {total_games} jogos):\n"
        f"- Vitórias: {strong_wins} ({winrate:.2f}%)\n"
        f"- Empates: {draws} ({drawrate:.2f}%)\n"
        f"- Derrotas: {losses} ({lossrate:.2f}%)\n"
    )

    # Salva os resultados em um arquivo de texto separado
    stats_filename = f"{os.path.splitext(output_file)[0]}_results.txt"
    with open(stats_filename, 'a') as f:
        f.write(result_text)

    print(f"Treinamento salvo em {output_file}")
    print(result_text.strip())
    print(f"Resumo salvo em {stats_filename}")

#rodar indefinidamente por blocos
if __name__ == "__main__":
    while True:
        generate_training_data(num_games=100, output_file="training_data6.csv", strong_time=2, weak_time=0.5)