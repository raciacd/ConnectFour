
import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from id3_decision_tree import ID3DecisionTree

# Load Iris data
iris = load_iris()
X = iris.data
y = iris.target

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1)

# Train the model
tree = ID3DecisionTree(max_depth=5, min_samples_split=10)
tree.fit(X_train, y_train)

# Evaluate
y_train_pred = tree.predict(X_train)
y_test_pred = tree.predict(X_test)

print(f"Training Accuracy: {accuracy_score(y_train, y_train_pred) * 100:.2f}%")
print(f"Test Accuracy: {accuracy_score(y_test, y_test_pred) * 100:.2f}%")

# Optional: print the tree
# tree.print_tree(feature_names=iris.feature_names)