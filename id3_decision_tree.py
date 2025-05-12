

import numpy as np
from collections import Counter

class ID3DecisionTree:
    def __init__(self, max_depth=None, min_samples_split=2):
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.tree = None

    def fit(self, X, y):
        X = np.array(X)
        y = np.array(y)
        self.feature_indices = list(range(X.shape[1]))
        self.tree = self._build_tree(X, y, depth=0)

    def _build_tree(self, X, y, depth):
        n_samples = X.shape[0]
        if (self.max_depth and depth >= self.max_depth) or \
           n_samples < self.min_samples_split or \
           len(np.unique(y)) == 1:
            return self._make_leaf_node(y)

        best_feature, best_threshold = self._find_best_split(X, y)
        if best_feature is None:
            return self._make_leaf_node(y)

        left_mask = X[:, best_feature] <= best_threshold
        right_mask = ~left_mask

        if np.sum(left_mask) == 0 or np.sum(right_mask) == 0:
            return self._make_leaf_node(y)

        left_subtree = self._build_tree(X[left_mask], y[left_mask], depth + 1)
        right_subtree = self._build_tree(X[right_mask], y[right_mask], depth + 1)

        return {
            'feature': best_feature,
            'threshold': best_threshold,
            'left': left_subtree,
            'right': right_subtree
        }

    def _find_best_split(self, X, y):
        best_gain = -1
        best_feature = None
        best_threshold = None
        for feature in self.feature_indices:
            thresholds = np.unique(X[:, feature])
            for threshold in thresholds:
                gain = self._information_gain(X, y, feature, threshold)
                if gain > best_gain:
                    best_gain = gain
                    best_feature = feature
                    best_threshold = threshold
        return best_feature, best_threshold

    def _information_gain(self, X, y, feature, threshold):
        parent_entropy = self._entropy(y)
        left_mask = X[:, feature] <= threshold
        right_mask = ~left_mask
        if sum(left_mask) == 0 or sum(right_mask) == 0:
            return 0
        n = len(y)
        n_left, n_right = sum(left_mask), sum(right_mask)
        e_left = self._entropy(y[left_mask])
        e_right = self._entropy(y[right_mask])
        child_entropy = (n_left / n) * e_left + (n_right / n) * e_right
        return parent_entropy - child_entropy

    def _entropy(self, y):
        counts = Counter(y)
        proportions = np.array(list(counts.values())) / len(y)
        return -np.sum(proportions * np.log2(proportions + 1e-10))

    def _make_leaf_node(self, y):
        counts = Counter(y)
        most_common = counts.most_common(1)[0][0]
        return {'class': most_common, 'count': len(y), 'distribution': dict(counts)}

    def predict(self, X):
        return np.array([self._predict_single(x) for x in X])

    def _predict_single(self, x, node=None):
        if node is None:
            node = self.tree
        if 'class' in node:
            return node['class']
        if x[node['feature']] <= node['threshold']:
            return self._predict_single(x, node['left'])
        else:
            return self._predict_single(x, node['right'])

    def print_tree(self, node=None, depth=0, feature_names=None):
        if node is None:
            node = self.tree
            print("\nDecision Tree:")
        prefix = "  " * depth
        if 'class' in node:
            dist = ", ".join(f"{k}:{v}" for k, v in node['distribution'].items())
            print(f"{prefix}Leaf: class={node['class']} (samples={node['count']}, dist={dist})")
        else:
            feature_name = feature_names[node['feature']] if feature_names else f"Feature_{node['feature']}"
            print(f"{prefix}If {feature_name} <= {node['threshold']}:")
            self.print_tree(node['left'], depth + 1, feature_names)
            print(f"{prefix}else:")
            self.print_tree(node['right'], depth + 1, feature_names)
            