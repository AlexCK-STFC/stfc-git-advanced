import matplotlib

matplotlib.use("Agg")

from peakfinder.plot import plot_spectrum


def test_plot_is_saved_to_file(tmp_path):
    x = [0, 1, 2, 3, 4]
    y = [0, 1, 5, 1, 0]
    filename = tmp_path / "spectrum.png"
    plot_spectrum(x, y, [(2, 5)], filename=filename)
    assert filename.exists()
