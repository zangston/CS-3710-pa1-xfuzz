# Utilities for retrieving wordlists used in testing.

from pathlib import Path

wordlist_path = Path(__file__).parent.resolve()


def path_common():
    return (wordlist_path / "common.txt").relative_to(Path.cwd())


def get_common():
    with open(path_common(), "r") as f:
        return f.read().splitlines()
