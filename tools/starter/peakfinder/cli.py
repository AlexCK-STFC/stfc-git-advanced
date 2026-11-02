import argparse
import sys

from peakfinder.io import load_spectrum
from peakfinder.normalise import normalise
from peakfinder.peaks import find_peaks


def main():
    parser = argparse.ArgumentParser(description="Find peaks in a spectrum")
    parser.add_argument("filename", help="csv file with x and y columns")
    parser.add_argument("--normalise", action="store_true",
                        help="scale the spectrum between 0 and 1 first")
    args = parser.parse_args()

    x, y = load_spectrum(args.filename)
    if args.normalise:
        y = normalise(y)

    peaks = find_peaks(x, y)
    for position, height in peaks:
        print(f"{position:.2f} {height:.3f}")


if __name__ == "__main__":
    main()
