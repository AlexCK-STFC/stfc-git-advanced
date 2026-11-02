from peakfinder.peaks import find_peaks


def test_single_peak():
    x = [0, 1, 2, 3, 4]
    y = [0, 1, 5, 1, 0]
    assert find_peaks(x, y) == [(2, 5)]


def test_two_peaks():
    x = [0, 1, 2, 3, 4, 5, 6]
    y = [0, 3, 0, 1, 4, 1, 0]
    assert find_peaks(x, y) == [(1, 3), (4, 4)]


def test_flat_line_has_no_peaks():
    x = [0, 1, 2, 3]
    y = [2, 2, 2, 2]
    assert find_peaks(x, y) == []
