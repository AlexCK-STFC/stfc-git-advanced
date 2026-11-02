import numpy as np


def load_spectrum(path):
    """Read a csv file with a header row and return the x and y columns."""
    data = np.loadtxt(path, delimiter=",", skiprows=1)
    return data[:, 0], data[:, 1]
