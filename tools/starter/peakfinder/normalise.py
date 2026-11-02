import numpy as np


def normalise(y):
    """Scale y so that it runs from 0 to 1."""
    y = np.asarray(y, dtype=float)
    return (y - y.min()) / (y.max() - y.min())
