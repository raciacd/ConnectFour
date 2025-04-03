from ConnectState import ConnectState #Game state and interface
#Import every search/play method
from mcts import MCTS
from random_ai import RandomAI

def get_human_move(state):
    while True:
        try:
            user_move = int(input("Enter a move: ")) - 1 #User chooses a column from 1 to 7, for better understanding
            if user_move in state.get_legal_moves():
                return user_move
            else:
                print("Illegal move")
        except ValueError:
            print("Please enter a valid number")

#Define all playable algorithms

def get_mcts_move(mcts):
    print("Thinking...")
    mcts.search(2)
    num_rollouts, run_time, num_states = mcts.statistics()
    print("Statistics: ", num_rollouts, "rollouts in", run_time, "seconds")
    print("States generated:", num_states)
    return mcts.best_move()

def get_random_move(random_ai):
    return random_ai.best_move()

def get_player_type(player_num): #Game settings, lets the user select the playing algorithms or the manual play
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
    #Each variable must be duplicated so we can keep track of the player
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

        #Keeps track of the table state for the MCTS, not needed for random since it does not compare states
        state.move(move)
        mcts1.move(move)
        mcts2.move(move)

        if state.game_over():
            state.print()
            outcome = state.get_outcome() #Returns value 1 to 3 from ConnectState, we don't need to check 1 or 2 since the execution order will provide us with the correct winner
            if outcome == 3: #Although we don't check 1 or 2, we need to check state 3 draw, otherwise there will be no remaing moves and the current player will be incorrectly declared winner
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
            if outcome == 3:
                print("Game ended in a draw!")
            else:
                print("Player 2 won!")
            break

if __name__ == "__main__":
    play()
