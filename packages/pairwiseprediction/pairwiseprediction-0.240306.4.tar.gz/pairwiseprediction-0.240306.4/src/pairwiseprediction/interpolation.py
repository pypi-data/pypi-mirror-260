import numpy as np


def interpolate_for_classification(targets, conditions):
    """
    :param targets: Training set targets. Must be sorted.
    :param conditions:
        `1` means the resulting value should be greater than the corresponding target.
        `0` means the resulting value should be equal than the corresponding target. (`0` is not usually needed)
        `-1` means the resulting value should be lesser than the corresponding target.
    :return:

    >>> tgts = np.array([77,81,84,87,88,90,99,100,103,105,110,112,115,120])
    >>> conds = np.array([1,1,-1,1,1,-1,1,-1,-1,1,-1,-1,1,-1])
    >>> interpolate_for_classification(tgts, conds)
    94.25
    """
    first = 2 * targets[0] - targets[1]
    last = 2 * targets[-1] - targets[-2]
    targets = np.hstack([np.array([first]), targets, np.array([last])])
    conditions = np.hstack([np.array([1]), conditions, np.array([-1])])
    acc = np.cumsum(conditions)
    mx_mask = acc == np.max(acc)
    mx_idxs = np.flatnonzero(mx_mask)
    neighbors_before = targets[mx_idxs]
    neighbors_after = targets[mx_idxs + 1]
    candidates = (neighbors_before + neighbors_after) / 2
    return np.mean(candidates)


def interpolate_for_regression(targets, conditions):
    candidates = targets + conditions
    return np.mean(candidates)
