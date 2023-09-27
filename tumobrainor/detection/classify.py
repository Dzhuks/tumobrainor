from pathlib import Path
from random import randint


def classify(filepath: Path) -> int:
    return randint(0, 3)
