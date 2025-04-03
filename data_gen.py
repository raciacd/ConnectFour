import csv
from ConnectState import ConnectState
from mcts import MCTS

def flatten_board(board):
    return [cell for row in board for cell in row]

def generate_training_data(num_games, output_file):
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        # Header: 42 cells + to_play + label
        writer.writerow([f'cell_{i}' for i in range(42)] + ['to_play', 'label'])

        for game_num in range(num_games):
            print(f"Generating game {game_num + 1}...")
            state = ConnectState()
            mcts = MCTS(state)

            while not state.game_over():
                mcts.search(1)  # 1 second per move
                move = mcts.best_move()

                if move == -1:
                    print("MCTS returned -1 — game must be over or no moves left.")
                    break

                # Extract current state and decision
                board_flat = flatten_board(state.board)
                to_play = state.to_play
                label = move

                writer.writerow(board_flat + [to_play, label])

                # Apply move to real game and sync MCTS
                state.move(move)
                mcts.move(move)

    print(f"Training data saved to {output_file}")

generate_training_data(5, "test_data.csv")