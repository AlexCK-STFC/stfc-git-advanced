import numpy as np


def find_peaks(x, y):
    """Return a list of (position, height) for each local maximum in y."""
    x = np.asarray(x)
    y = np.asarray(y)
    peaks = []
    for i in range(1, len(y) - 1):
        if y[i] > y[i - 1] and y[i] > y[i + 1]:
            peaks.append((x[i], y[i]))
    return peaks
