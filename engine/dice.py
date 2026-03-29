import random


def roll(sides: int) -> int:
    return random.randint(1, sides)


def roll_range(lo: int, hi: int) -> int:
    return random.randint(lo, hi)


def chance(p: float) -> bool:
    return random.random() < p
