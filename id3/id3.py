from sklearn.datasets import load_breast_cancer
import numpy as np
from pprint import pprint


def partition(set_):
    return {subset: (set_ == subset).nonzero()[0] for subset in np.unique(set_)}


def entropy(set_):
    res = 0
    val, counts = np.unique(set_, return_counts=True)
    freqs = counts.astype('float') / len(set_)
    for p in freqs:
        if p != 0.0:
            res -= p * np.log2(p)
    return res


def gain(y, subset):
    res = entropy(y)

    val, counts = np.unique(subset, return_counts=True)
    freqs = counts.astype('float') / len(subset)

    for p, v in zip(freqs, val):
        res -= p * entropy(y[subset == v])

    return res


def is_pure(set_):
    return np.all(set_ == set_[0])


def recursive_split(X, y):
    # If there could be no split, just return the original set
    if is_pure(y) or len(y) == 0:
        return y

    # We get attribute that gives the highest mutual information
    gains = np.array([gain(y, x_attr) for x_attr in X.T])
    selected_attr = np.argmax(gains)

    # If there's no gain at all, nothing has to be done, just return the original set
    if np.all(gains < 1e-6):
        return y

    # We split using the selected attribute
    sets = partition(X[:, selected_attr])

    res = {}
    for k, v in sets.items():
        y_subset = y.take(v, axis=0)
        x_subset = X.take(v, axis=0)

        res["x_%d = %d" % (selected_attr, k)] = recursive_split(x_subset, y_subset)

    return res


if __name__ == '__main__':
    X, y = load_breast_cancer(return_X_y=True)

    pprint(recursive_split(X, y))
