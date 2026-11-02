#!/usr/bin/env python3
"""Update the commit hashes quoted in the lesson after the example repo is rebuilt.

Any change to tools/ (even a name or a date) changes every commit hash, and the episodes
quote real hashes. Run this around a rebuild:

    git -C build/peakfinder log --all --format='%H|%at|%s' > /tmp/old_hashes.txt
    python tools/build_starter.py --force
    python tools/remap_hashes.py /tmp/old_hashes.txt

Commits are matched by author date and subject, which the build keeps fixed. Every hash-like
word in episodes/ and learners/ that is the start of an old commit is swapped for the same
length of the new one. Hashes that are not commits in the repo (the made-up ones in episodes
7 and 9, tree hashes) are left alone and listed, so you can check them.
"""
import glob
import re
import subprocess
import sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
if len(sys.argv) != 2:
    sys.exit(__doc__)


def commits(lines):
    pairs = [line.split("|", 2) for line in lines.splitlines() if line]
    return {(when, subject): sha for sha, when, subject in pairs}


old = commits(Path(sys.argv[1]).read_text())
new = commits(subprocess.run(
    ["git", "-C", str(root / "build" / "peakfinder"), "log", "--all", "--format=%H|%at|%s"],
    capture_output=True, text=True, check=True).stdout)

if old.keys() != new.keys():
    sys.exit("The old and new repos don't have the same commits (by date and subject), so they can't be matched.")

mapping = {old[key]: new[key] for key in old if old[key] != new[key]}
if not mapping:
    sys.exit("No hashes changed. Nothing to do.")

word = re.compile(r"(?<![0-9a-zA-Z])[0-9a-f]{7,40}(?![0-9a-zA-Z])")
unmatched = {}

for name in sorted(glob.glob(str(root / "episodes" / "*.md")) + glob.glob(str(root / "learners" / "*.md"))):
    text = Path(name).read_text()
    count = 0

    def swap(match):
        global count
        found = match.group(0)
        hits = [sha for sha in mapping if sha.startswith(found)]
        if len(hits) == 1:
            count += 1
            return mapping[hits[0]][: len(found)]
        if len(hits) > 1:
            print("ambiguous:", found, "in", name)
        elif re.search(r"[0-9]", found) and re.search(r"[a-f]", found):
            unmatched.setdefault(Path(name).name, set()).add(found)
        return found

    result = word.sub(swap, text)
    if result != text:
        Path(name).write_text(result)
        print(f"{Path(name).name}: {count} hash(es) updated")

print("\nHash-like words that are not commits in the repo (made up, or other objects). Check they are meant to be:")
for name, found in unmatched.items():
    print(" ", name, sorted(found))
