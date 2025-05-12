import numpy as np
from id3_decision_tree import ID3DecisionTree
from ConnectState import ConnectState
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

def load_training_data(filename):
    data = np.loadtxt(filename, delimiter=',', skiprows=1)
    X = data[:, :-2]  #os 42 estados 
    y = data[:, -1]   #ultima coluna movida
    return X, y

def train_model():
    # Load data
    X, y = load_training_data("test_data.csv")

    
    # Split data (80% train, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
    
    # Train model
    dt = ID3DecisionTree(max_depth=10)
    dt.fit(X_train, y_train)
    
    # Evaluate
    train_pred = dt.predict(X_train)
    test_pred = dt.predict(X_test)
    
    train_acc = accuracy_score(y_train, train_pred)
    test_acc = accuracy_score(y_test, test_pred)
    
    print(f"\nTraining Accuracy: {train_acc:.2%}")
    print(f"Test Accuracy: {test_acc:.2%}")
    
    # Save model
    import pickle
    with open("connect4_dt_model.pkl", 'wb') as f:
        pickle.dump(dt, f)
    
    print("Model saved to connect4_dt_model.pkl")

if __name__ == "__main__":
    train_model()