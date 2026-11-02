import matplotlib.pyplot as plt
from matplotlib.figure import Figure


def draw(ax, x, y, peaks):
    """Draw the spectrum on ax with a red dot on each peak."""
    ax.plot(x, y)
    ax.plot([p[0] for p in peaks], [p[1] for p in peaks], "ro")
    ax.set_xlabel("x")
    ax.set_ylabel("intensity")


def plot_spectrum(x, y, peaks, filename=None):
    """Show the plot in a window, or save it if a filename is given."""
    if filename:
        # Figure doesn't need a display, so this works on any machine
        fig = Figure()
        draw(fig.subplots(), x, y, peaks)
        fig.savefig(filename)
    else:
        fig, ax = plt.subplots()
        draw(ax, x, y, peaks)
        plt.show()
