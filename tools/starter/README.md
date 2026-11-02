# peakfinder

Find peaks in spectrums.

## Install

    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt

## Usage

    python -m peakfinder.cli data/example_spectrum.csv

Add `--normalise` to scale the spectrum between 0 and 1 first.

## Tests

    pytest
