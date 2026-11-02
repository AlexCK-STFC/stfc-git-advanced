import numpy as np

from peakfinder.normalise import normalise


def test_normalise_runs_from_zero_to_one():
    result = normalise([1, 3, 5])
    assert np.allclose(result, [0, 0.5, 1])


def test_normalise_keeps_shape():
    y = np.array([4.0, 2.0, 8.0, 6.0])
    assert normalise(y).shape == y.shape
