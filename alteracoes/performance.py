import time
from ConnectState import ConnectState
from mcts import MCTS

def test_performance():
    state = ConnectState()
    mcts = MCTS(state)
    
    max_time = 2.0
    simulations = 0
    
    start_time = time.time()
    
    while True:
        mcts.search(0.001)
        simulations += 1
        
        if time.time() - start_time > max_time:
            break
    
    total_time = time.time() - start_time
    
    print(f"Simulations performed in {max_time} seconds: {simulations}")
    print(f"Total elapsed time: {total_time:.4f} seconds")
    print(f"Simulations per second: {simulations / total_time:.2f}")

if __name__ == "__main__":
    test_performance()