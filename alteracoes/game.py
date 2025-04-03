from ConnectState import ConnectState
from mcts import MCTS
from random_ai import RandomAI
from meta import GameMeta

def get_human_move(state):
    while True:
        try:
            user_move = int(input("Enter a move: ")) - 1
            if user_move in state.get_legal_moves():
                return user_move
            else:
                print("Illegal move")
        except ValueError:
            print("Please enter a valid number")

def get_mcts_move(mcts):
    print("Thinking...")
    mcts.search(0.5)
    num_rollouts, run_time = mcts.statistics()
    print(f"Statistics: {num_rollouts} rollouts in {run_time:.2f} seconds")
    return mcts.best_move()

def get_random_move(random_ai):
    return random_ai.best_move()

def get_player_type(player_num):
    while True:
        try:
            choice = int(input(f"Select Player {player_num} type: \n1 = Human\n2 = MCTS\n3 = Random\n"))
            if choice in [1, 2, 3]:
                return choice
            else:
                print("Please enter 1, 2, or 3.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def play():
    state = ConnectState()
    mcts1 = MCTS(state)
    mcts2 = MCTS(state)
    random_ai1 = RandomAI(state)
    random_ai2 = RandomAI(state)
    
    player1_type = get_player_type(1)
    player2_type = get_player_type(2)

    while not state.game_over():
        print("Current state:")
        state.print()

        if player1_type == 1:
            move = get_human_move(state)
        elif player1_type == 2:
            move = get_mcts_move(mcts1)
        else:
            move = get_random_move(random_ai1)

        state.move(move)
        mcts1.move(move)
        mcts2.move(move)

        if state.game_over():
            state.print()
            outcome = state.get_outcome()
            if outcome == GameMeta.OUTCOMES['draw']:
                print("Game ended in a draw!")
            else:
                print("Player 1 won!")
            break

        print("Current state:")
        state.print()

        if player2_type == 1:
            move = get_human_move(state)
        elif player2_type == 2:
            move = get_mcts_move(mcts2)
        else:
            move = get_random_move(random_ai2)

        state.move(move)
        mcts1.move(move)
        mcts2.move(move)

        if state.game_over():
            state.print()
            outcome = state.get_outcome()
            if outcome == GameMeta.OUTCOMES['draw']:
                print("Game ended in a draw!")
            else:
                print("Player 2 won!")
            break

if __name__ == "__main__":
    play()
