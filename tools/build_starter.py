#!/usr/bin/env python3
"""Build the peakfinder repo used in the course.

    python tools/build_starter.py [output_dir] [--force]

The output (default build/peakfinder) is a normal git repo. Fixed names and
dates are used for every commit, so running this twice gives the same hashes.

Branches and tags that get created:

    main                              6 commits, tagged v0.1.0
    background-subtraction            messy branch for episode 06
    solution/background-subtraction   the same work, cleaned up
    colleague/normalise-modes         colleague's work, contains a bug, v0.2.0 tag
    solution/fix-normalise            fix for the bug (episodes 10 and 13)
    solution/feature-*                example features for episode 07

At the end the script checks the things the lesson relies on (tests pass or
fail where we expect, the colleague's branch conflicts with the features, etc).
"""
import os
import shutil
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
STARTER = HERE / "starter"

args = [a for a in sys.argv[1:] if not a.startswith("--")]
FORCE = "--force" in sys.argv
OUT = Path(args[0]).resolve() if args else HERE.parent / "build" / "peakfinder"
VENV = OUT.parent / ".venv-build"

YOU = ("Sam Scientist", "sam.scientist@example.org")
COLLEAGUE = ("Robin Researcher", "robin.researcher@example.org")

clock = datetime(2025, 1, 6, 9, 0)


# ---------------------------------------------------------------- helpers

def git(*cmd, cwd=None, check=True):
    result = subprocess.run(
        ["git", *cmd], cwd=cwd or OUT, text=True, capture_output=True
    )
    if check and result.returncode != 0:
        sys.exit(f"git {' '.join(cmd)} failed:\n{result.stdout}{result.stderr}")
    return result.stdout.strip()


def set_author(who):
    name, email = who
    os.environ["GIT_AUTHOR_NAME"] = os.environ["GIT_COMMITTER_NAME"] = name
    os.environ["GIT_AUTHOR_EMAIL"] = os.environ["GIT_COMMITTER_EMAIL"] = email


def set_clock(year, month, day, hour=9):
    global clock
    clock = datetime(year, month, day, hour, 0)


def commit(message, body=None):
    """Commit everything that has changed, one hour after the last commit."""
    global clock
    clock += timedelta(hours=1)
    stamp = clock.strftime("%Y-%m-%dT%H:%M:%S+00:00")
    os.environ["GIT_AUTHOR_DATE"] = os.environ["GIT_COMMITTER_DATE"] = stamp
    git("add", "-A")
    full = message if body is None else f"{message}\n\n{body}"
    git("commit", "-q", "-m", full)
    return git("rev-parse", "HEAD")


def replace(path, old, new):
    """Replace text in a file. Fails loudly if the old text is not there."""
    file = OUT / path
    text = file.read_text()
    if old not in text:
        sys.exit(f"could not find text to replace in {path}:\n{old}")
    file.write_text(text.replace(old, new, 1))


def append(path, text):
    with open(OUT / path, "a") as f:
        f.write(text)


def write(path, text):
    file = OUT / path
    file.parent.mkdir(parents=True, exist_ok=True)
    file.write_text(text)


def copy_from_starter(paths):
    for p in paths:
        target = OUT / p
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(STARTER / p, target)


def branch(name, start="main"):
    git("switch", "-q", "-c", name, start)


# ---------------------------------------------------------------- main branch

def build_main():
    set_author(YOU)
    set_clock(2025, 1, 6)
    git("init", "-q", "-b", "main")
    git("config", "commit.gpgsign", "false")

    copy_from_starter([
        "pyproject.toml", "README.md", ".gitignore", "requirements.txt",
        "peakfinder/__init__.py",
    ])
    commit("Add project metadata and README")

    copy_from_starter(["peakfinder/peaks.py", "tests/test_peaks.py"])
    commit("Add find_peaks", "Finds local maxima by comparing each point to its neighbours.")

    copy_from_starter(["peakfinder/normalise.py", "tests/test_normalise.py"])
    commit("Add normalise")

    copy_from_starter(["peakfinder/io.py", "data/example_spectrum.csv"])
    commit("Add loading of csv spectra")

    copy_from_starter(["peakfinder/cli.py"])
    commit("Add command line interface")

    # plotting arrives late, once people wanted to see the spectrum
    copy_from_starter(["peakfinder/plot.py", "tests/test_plot.py"])
    replace("peakfinder/cli.py",
            "from peakfinder.peaks import find_peaks\n",
            "from peakfinder.peaks import find_peaks\nfrom peakfinder.plot import plot_spectrum\n")
    replace("peakfinder/cli.py",
            '                        help="scale the spectrum between 0 and 1 first")\n',
            '                        help="scale the spectrum between 0 and 1 first")\n'
            '    parser.add_argument("--plot", action="store_true",\n'
            '                        help="show a plot of the spectrum and its peaks")\n'
            '    parser.add_argument("--save-plot", metavar="FILE",\n'
            '                        help="save the plot to FILE instead of showing it")\n')
    replace("peakfinder/cli.py",
            '        print(f"{position:.2f} {height:.3f}")\n',
            '        print(f"{position:.2f} {height:.3f}")\n\n'
            '    if args.save_plot:\n'
            '        plot_spectrum(x, y, peaks, filename=args.save_plot)\n'
            '    elif args.plot:\n'
            '        plot_spectrum(x, y, peaks)\n')
    replace("README.md",
            "Add `--normalise` to scale the spectrum between 0 and 1 first.\n",
            "Add `--normalise` to scale the spectrum between 0 and 1 first.\n\n"
            "Add `--plot` to see the spectrum with the peaks marked, or\n"
            "`--save-plot spectrum.png` to save the plot instead.\n")
    commit("Add plotting of the spectrum and its peaks")

    git("tag", "-a", "v0.1.0", "-m", "First release")


# ---------------------------------------------------------------- episode 06

def build_messy_branch():
    """Ten commits, the way a real week of work looks."""
    set_author(YOU)
    set_clock(2025, 2, 3)
    branch("background-subtraction")

    # 1
    write("peakfinder/background.py", '''\
"""Substract a smooth background from a spectrum."""
import numpy as np


def subtract_background(y, window=25):
    """Subtract a rolling minimum background from the spectrum y."""
    y = np.asarray(y, dtype=float)
    return y
''')
    commit("add background module")

    # 2
    replace("peakfinder/background.py",
            "    y = np.asarray(y, dtype=float)\n    return y\n",
            '''\
    print("window", window)
    y = np.asarray(y, dtype=float)
    half = window // 2
    background = np.zeros(len(y))
    for i in range(len(y)):
        start = i - half
        stop = i + half + 1
        background[i] = y[start:stop].min()
    return y - background
''')
    commit("wip")

    # 3: three unrelated changes in one commit (split it in the lesson)
    replace("peakfinder/normalise.py",
            "    return (y - y.min()) / (y.max() - y.min())\n",
            '''\
    span = y.max() - y.min()
    if span == 0:
        return np.zeros(len(y))
    return (y - y.min()) / span
''')
    append("tests/test_normalise.py", '''

def test_normalise_constant_spectrum():
    assert np.allclose(normalise([4, 4, 4]), 0)
''')
    replace("peakfinder/io.py",
            "def load_spectrum(path):\n    \"\"\"Read a csv file with a header row and return the x and y columns.\"\"\"\n"
            "    data = np.loadtxt(path, delimiter=\",\", skiprows=1)\n",
            "def load_spectrum(path, skiprows=1):\n    \"\"\"Read a csv file and return the x and y columns.\"\"\"\n"
            "    data = np.loadtxt(path, delimiter=\",\", skiprows=skiprows)\n")
    replace("peakfinder/peaks.py",
            "    y = np.asarray(y)\n",
            '    y = np.asarray(y)\n    if len(x) != len(y):\n        raise ValueError("x and y must have the same length")\n')
    replace("tests/test_peaks.py",
            "from peakfinder.peaks import find_peaks\n",
            "import pytest\n\nfrom peakfinder.peaks import find_peaks\n")
    append("tests/test_peaks.py", '''

def test_different_lengths_raise_an_error():
    with pytest.raises(ValueError):
        find_peaks([0, 1, 2], [0, 1])
''')
    commit("tidy up")

    # 4
    replace("peakfinder/background.py",
            "        start = i - half\n        stop = i + half + 1\n",
            "        start = max(0, i - half)\n        stop = min(len(y), i + half + 1)\n")
    commit("fix")

    # 5
    write("tests/test_background.py", '''\
import numpy as np

from peakfinder.background import subtract_background


def test_flat_spectrum_goes_to_zero():
    y = np.full(50, 3.0)
    assert np.allclose(subtract_background(y), 0)


def test_removes_constant_offset():
    y = np.array([0, 0, 5, 0, 0, 0, 0, 0], dtype=float) + 10
    result = subtract_background(y, window=3)
    assert np.allclose(result, [0, 0, 5, 0, 0, 0, 0, 0])
''')
    commit("add tests")

    # 6
    replace("peakfinder/background.py", '    print("window", window)\n', "")
    commit("remove print")

    # 7
    replace("peakfinder/cli.py",
            "from peakfinder.io import",
            "from peakfinder.background import subtract_background\nfrom peakfinder.io import")
    replace("peakfinder/cli.py",
            '                        help="scale the spectrum between 0 and 1 first")\n',
            '                        help="scale the spectrum between 0 and 1 first")\n'
            '    parser.add_argument("--subtract-background", action="store_true",\n'
            '                        help="remove a rolling minimum background first")\n')
    replace("peakfinder/cli.py",
            "    if args.normalise:\n",
            "    if args.subtract_background:\n        y = subtract_background(y)\n    if args.normalise:\n")
    commit("cli stuff")

    # 8
    replace("peakfinder/background.py", "Substract", "Subtract")
    commit("fix typo")

    # 9: an experiment that went nowhere
    write("scratch_smoothing.py", '''\
import numpy as np

# trying a moving average instead
def smooth(y, n=5):
    return np.convolve(y, np.ones(n) / n, mode="same")
''')
    commit("try smoothing")

    # 10
    replace("README.md",
            "Add `--normalise` to scale the spectrum between 0 and 1 first.\n",
            "Add `--normalise` to scale the spectrum between 0 and 1 first.\n\n"
            "Add `--subtract-background` to remove a rolling minimum background first.\n")
    commit("readme")


def build_messy_solution():
    """The same work as small commits. Files are taken from the messy tip."""
    set_author(YOU)
    set_clock(2025, 2, 10)
    branch("solution/background-subtraction")

    steps = [
        (["peakfinder/normalise.py", "tests/test_normalise.py"],
         "Handle constant spectra in normalise",
         "A flat spectrum has max equal to min, so we were dividing by zero.\nReturn zeros instead."),
        (["peakfinder/io.py"],
         "Let load_spectrum skip a variable number of header rows", None),
        (["peakfinder/peaks.py", "tests/test_peaks.py"],
         "Check x and y are the same length in find_peaks", None),
        (["peakfinder/background.py"],
         "Add rolling minimum background subtraction",
         "Takes the minimum in a window around each point as the background."),
        (["tests/test_background.py"],
         "Add tests for background subtraction", None),
        (["peakfinder/cli.py"],
         "Add --subtract-background option to the CLI", None),
        (["README.md"],
         "Document --subtract-background in the README", None),
    ]
    for paths, message, body in steps:
        git("checkout", "background-subtraction", "--", *paths)
        commit(message, body)


# ---------------------------------------------------------------- colleague

def build_colleague():
    set_author(COLLEAGUE)
    set_clock(2025, 2, 4)
    branch("colleague/normalise-modes")

    replace("README.md", "spectrums", "spectra")
    commit("Fix typo in README")

    # the bug: the range mode divides by max, then subtracts min
    write("peakfinder/normalise.py", '''\
import numpy as np


def normalise(y, mode="range"):
    """Scale y. mode is 'range' (0 to 1), 'max' (divide by max) or 'area'."""
    y = np.asarray(y, dtype=float)
    if mode == "range":
        return (y - y.min()) / y.max() - y.min()
    if mode == "max":
        return y / y.max()
    if mode == "area":
        return y / y.sum()
    raise ValueError(f"unknown mode: {mode}")
''')
    append("tests/test_normalise.py", '''

def test_normalise_max_mode():
    assert np.allclose(normalise([1, 2, 4], mode="max"), [0.25, 0.5, 1])


def test_normalise_area_mode():
    assert np.allclose(normalise([1, 1, 2], mode="area"), [0.25, 0.25, 0.5])
''')
    commit("Add mode option to normalise",
           "Adds 'max' and 'area' modes alongside the default 'range'.")

    replace("peakfinder/cli.py", "import sys\n", "")
    commit("Remove unused import from cli")

    replace("peakfinder/__init__.py", "0.1.0", "0.2.0")
    replace("pyproject.toml", 'version = "0.1.0"', 'version = "0.2.0"')
    commit("Bump version to 0.2.0")
    git("tag", "-a", "v0.2.0", "-m", "Second release")

    replace("peakfinder/peaks.py",
            'import numpy as np\n\n\ndef find_peaks(x, y):\n'
            '    """Return a list of (position, height) for each local maximum in y."""\n',
            'from typing import NamedTuple\n\nimport numpy as np\n\n\n'
            'class Peak(NamedTuple):\n    position: float\n    height: float\n\n\n'
            'def find_peaks(x, y):\n'
            '    """Return a list of Peak tuples, one for each local maximum in y."""\n')
    replace("peakfinder/peaks.py",
            "peaks.append((x[i], y[i]))", "peaks.append(Peak(x[i], y[i]))")
    replace("tests/test_peaks.py",
            "from peakfinder.peaks import find_peaks\n",
            "from peakfinder.peaks import Peak, find_peaks\n")
    replace("tests/test_peaks.py", "== [(2, 5)]", "== [Peak(2, 5)]")
    replace("tests/test_peaks.py", "== [(1, 3), (4, 4)]", "== [Peak(1, 3), Peak(4, 4)]")
    replace("peakfinder/cli.py",
            '    for position, height in peaks:\n'
            '        print(f"{position:.2f} {height:.3f}")\n',
            '    for peak in peaks:\n'
            '        print(f"{peak.position:.2f} {peak.height:.3f}")\n')
    replace("peakfinder/plot.py",
            'ax.plot([p[0] for p in peaks], [p[1] for p in peaks], "ro")',
            'ax.plot([p.position for p in peaks], [p.height for p in peaks], "ro")')
    replace("tests/test_plot.py",
            "from peakfinder.plot import plot_spectrum\n",
            "from peakfinder.peaks import Peak\nfrom peakfinder.plot import plot_spectrum\n")
    replace("tests/test_plot.py", "[(2, 5)]", "[Peak(2, 5)]")
    commit("Return Peak tuples from find_peaks",
           "Peaks now have names (peak.position, peak.height), but they still unpack\n"
           "like a tuple, so code that already uses them keeps working.")

    replace("README.md", "## Tests\n",
            "## Python use\n\n"
            "    from peakfinder.peaks import find_peaks\n"
            "    for peak in find_peaks(x, y):\n"
            "        print(peak.position, peak.height)\n\n"
            "## Tests\n")
    commit("Document Peak in the README")


def build_fix():
    set_author(YOU)
    set_clock(2025, 2, 11)
    branch("solution/fix-normalise", "colleague/normalise-modes")
    replace("peakfinder/normalise.py",
            "return (y - y.min()) / y.max() - y.min()",
            "return (y - y.min()) / (y.max() - y.min())")
    commit("Fix 'range' mode of normalise for spectra that don't start at zero",
           "The subtraction of the minimum was outside the division, so the\n"
           "result was only right when the minimum was zero.")


# ---------------------------------------------------------------- episode 07

PROMINENCE = '''

def prominence(y, i):
    """Height of the peak at i above the higher of the valleys either side."""
    left_min = y[i]
    for j in range(i - 1, -1, -1):
        if y[j] > y[i]:
            break
        left_min = min(left_min, y[j])
    right_min = y[i]
    for j in range(i + 1, len(y)):
        if y[j] > y[i]:
            break
        right_min = min(right_min, y[j])
    return y[i] - max(left_min, right_min)
'''

PEAK_WIDTH = '''

def peak_width(x, y, i):
    """Width of the peak at i where it falls to half its height."""
    half = y[i] / 2
    left = i
    while left > 0 and y[left] > half:
        left -= 1
    right = i
    while right < len(y) - 1 and y[right] > half:
        right += 1
    return x[right] - x[left]
'''


def build_features():
    """Example features. Learners write their own, these are for checking."""
    set_author(YOU)

    set_clock(2025, 2, 6)
    branch("solution/feature-min-height")
    replace("peakfinder/peaks.py", "def find_peaks(x, y):", "def find_peaks(x, y, min_height=None):")
    replace("peakfinder/peaks.py",
            "            peaks.append((x[i], y[i]))",
            "            if min_height is None or y[i] >= min_height:\n"
            "                peaks.append((x[i], y[i]))")
    commit("Add min_height option to find_peaks")
    append("tests/test_peaks.py", '''

def test_min_height_ignores_small_peaks():
    x = [0, 1, 2, 3, 4, 5, 6]
    y = [0, 3, 0, 1, 4, 1, 0]
    assert find_peaks(x, y, min_height=3.5) == [(4, 4)]
''')
    commit("Test min_height")

    set_clock(2025, 2, 6)
    branch("solution/feature-prominence")
    append("peakfinder/peaks.py", PROMINENCE)
    commit("Add prominence function")
    replace("peakfinder/peaks.py", "def find_peaks(x, y):", "def find_peaks(x, y, min_prominence=0):")
    replace("peakfinder/peaks.py",
            "            peaks.append((x[i], y[i]))",
            "            if prominence(y, i) >= min_prominence:\n"
            "                peaks.append((x[i], y[i]))")
    commit("Add min_prominence option to find_peaks")
    append("tests/test_peaks.py", '''

def test_min_prominence_ignores_bumps_on_a_slope():
    x = list(range(8))
    y = [0, 5, 4, 4.5, 4, 3, 1, 0]
    assert find_peaks(x, y, min_prominence=1) == [(1, 5)]
''')
    commit("Test min_prominence")

    set_clock(2025, 2, 6)
    branch("solution/feature-widths")
    append("peakfinder/peaks.py", PEAK_WIDTH)
    commit("Add peak_width function")
    replace("peakfinder/peaks.py", "def find_peaks(x, y):", "def find_peaks(x, y, with_widths=False):")
    replace("peakfinder/peaks.py",
            "            peaks.append((x[i], y[i]))",
            "            if with_widths:\n"
            "                peaks.append((x[i], y[i], peak_width(x, y, i)))\n"
            "            else:\n"
            "                peaks.append((x[i], y[i]))")
    commit("Add with_widths option to find_peaks")
    append("tests/test_peaks.py", '''

def test_peak_widths():
    x = [0, 1, 2, 3, 4, 5, 6]
    y = [0, 1, 4, 8, 4, 1, 0]
    assert find_peaks(x, y, with_widths=True) == [(3, 8, 2)]
''')
    commit("Test peak widths")


# ---------------------------------------------------------------- episode 05

def build_untangle():
    """One commit that mixes a feature, a fix and a leftover debug print."""
    set_author(YOU)
    set_clock(2025, 2, 12)
    branch("untangle")

    # the feature: --title for the plot
    replace("peakfinder/cli.py",
            '                        help="save the plot to FILE instead of showing it")\n',
            '                        help="save the plot to FILE instead of showing it")\n'
            '    parser.add_argument("--title", help="title for the plot")\n')
    replace("peakfinder/cli.py",
            "plot_spectrum(x, y, peaks, filename=args.save_plot)",
            "plot_spectrum(x, y, peaks, filename=args.save_plot, title=args.title)")
    replace("peakfinder/cli.py",
            "        plot_spectrum(x, y, peaks)\n",
            "        plot_spectrum(x, y, peaks, title=args.title)\n")
    replace("peakfinder/plot.py", "def draw(ax, x, y, peaks):", "def draw(ax, x, y, peaks, title=None):")
    replace("peakfinder/plot.py",
            '    ax.set_ylabel("intensity")\n',
            '    ax.set_ylabel("intensity")\n    if title:\n        ax.set_title(title)\n')
    replace("peakfinder/plot.py", "def plot_spectrum(x, y, peaks, filename=None):",
            "def plot_spectrum(x, y, peaks, filename=None, title=None):")
    replace("peakfinder/plot.py", "draw(fig.subplots(), x, y, peaks)", "draw(fig.subplots(), x, y, peaks, title)")
    replace("peakfinder/plot.py", "draw(ax, x, y, peaks)\n        plt.show()", "draw(ax, x, y, peaks, title)\n        plt.show()")

    # a separate fix: peak markers were hidden behind the line
    replace("peakfinder/plot.py", '"ro")', '"ro", zorder=3)')

    # a debug print that should never be committed
    replace("peakfinder/cli.py",
            "    x, y = load_spectrum(args.filename)\n",
            '    x, y = load_spectrum(args.filename)\n    print("DEBUG", len(x), len(y))\n')
    commit("plot stuff")


# ---------------------------------------------------------------- checks

def make_test_env():
    """A throwaway virtual environment with numpy and pytest."""
    python = VENV / "bin" / "python"
    if VENV.exists() and not python.exists():
        # a leftover environment whose python has gone (for example after a container rebuild)
        shutil.rmtree(VENV)
    if not VENV.exists():
        subprocess.run(["uv", "venv", "-q", str(VENV)], check=True)
    subprocess.run(["uv", "pip", "install", "-q", "--python", str(VENV),
                    "-r", str(STARTER / "requirements.txt")], check=True)
    return python


def tests_pass(python, rev):
    """Check out rev in a temporary worktree and run pytest there."""
    tmp = OUT.parent / "check-worktree"
    git("worktree", "add", "-q", "--detach", str(tmp), rev)
    try:
        result = subprocess.run([str(python), "-m", "pytest", "-q", "-p", "no:cacheprovider"],
                                cwd=tmp, capture_output=True, text=True)
        return result.returncode == 0
    finally:
        git("worktree", "remove", "--force", str(tmp))


def rebase_conflicts(branch_name, onto):
    """Try rebasing branch_name onto another branch. True if it conflicts."""
    tmp = OUT.parent / "check-worktree"
    git("worktree", "add", "-q", "-b", "tmp/check", str(tmp), branch_name)
    try:
        result = subprocess.run(["git", "rebase", onto], cwd=tmp, capture_output=True, text=True)
        conflicted = result.returncode != 0
        if conflicted:
            git("rebase", "--abort", cwd=tmp)
        return conflicted
    finally:
        git("worktree", "remove", "--force", str(tmp))
        git("branch", "-q", "-D", "tmp/check")


def check(ok, text):
    print(("  ok    " if ok else "  FAIL  ") + text)
    if not ok:
        check.failed = True


check.failed = False


def run_checks():
    print("Checking the repo...")
    python = make_test_env()

    check(tests_pass(python, "v0.1.0"), "tests pass at v0.1.0")

    clean = git("rev-list", "--reverse", "main..solution/background-subtraction").split()
    check(all(tests_pass(python, c) for c in clean),
          f"tests pass at all {len(clean)} commits of the clean background branch")
    check(git("diff", "--name-only", "background-subtraction", "solution/background-subtraction")
          == "scratch_smoothing.py",
          "clean branch matches the messy one, except the scratch file")

    theirs = git("rev-list", "--reverse", "main..colleague/normalise-modes").split()
    results = [tests_pass(python, c) for c in theirs]
    check(results == [True, False, False, False, False, False],
          f"colleague's commits: pass/fail is {results}, so bisect finds commit 2")
    bad = git("log", "-1", "--format=%s", theirs[1])
    check(bad == "Add mode option to normalise", f"first bad commit is '{bad}'")

    check(tests_pass(python, "solution/fix-normalise"), "tests pass after the fix")

    for name in ["feature-min-height", "feature-prominence", "feature-widths"]:
        check(tests_pass(python, f"solution/{name}"), f"{name}: tests pass on its own")
    for name in ["feature-prominence", "feature-widths"]:
        check(rebase_conflicts(f"solution/{name}", "colleague/normalise-modes"),
              f"{name}: rebasing onto the colleague's branch conflicts")
    print("  info  feature-min-height conflicts with colleague:",
          rebase_conflicts("solution/feature-min-height", "colleague/normalise-modes"))

    tmp = OUT.parent / "check-worktree"
    git("worktree", "add", "-q", "--detach", str(tmp), "v0.2.0")
    try:
        picked = subprocess.run(["git", "cherry-pick", "-x", "solution/fix-normalise"],
                                cwd=tmp, capture_output=True, text=True).returncode == 0
        passed = subprocess.run([str(python), "-m", "pytest", "-q", "-p", "no:cacheprovider"],
                                cwd=tmp, capture_output=True).returncode == 0
    finally:
        git("worktree", "remove", "--force", str(tmp))
    check(picked and passed, "fix cherry-picks cleanly onto v0.2.0 and tests pass")


def main():
    if OUT.exists():
        if not FORCE:
            sys.exit(f"{OUT} already exists. Use --force to rebuild it.")
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)

    build_main()
    build_messy_branch()
    git("switch", "-q", "main")
    build_messy_solution()
    git("switch", "-q", "main")
    build_colleague()
    build_fix()
    git("switch", "-q", "main")
    build_features()
    git("switch", "-q", "main")
    build_untangle()
    git("switch", "-q", "main")

    print(f"Built {OUT}")
    print(git("branch", "--format", "  %(refname:short)"))
    print(git("tag", "--format", "  tag %(refname:short)"))
    run_checks()
    sys.exit(1 if check.failed else 0)


if __name__ == "__main__":
    main()
