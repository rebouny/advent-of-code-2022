#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Solves second day of aoc 2022.

Uses precalculated map of scores for both parts as the
amount of possible values is limited.

"""

from typing import Final
from functools import reduce
import operator

SCORES: Final = {
    ('A', 'X'): (4, 3),
    ('A', 'Y'): (8, 4),
    ('A', 'Z'): (3, 8),
    ('B', 'X'): (1, 1),
    ('B', 'Y'): (5, 5),
    ('B', 'Z'): (9, 9),
    ('C', 'X'): (7, 2),
    ('C', 'Y'): (2, 6),
    ('C', 'Z'): (6, 7)
}


def load_input(filename: str):
    """Loads input"""
    with open(filename, 'rt', encoding='utf-8') as file:
        return [tuple(line.rstrip().split()) for line in file.readlines()]


def part_01(games) -> int:
    """Looks up first part of score tuple"""
    return reduce(operator.add, map(lambda x: SCORES[x][0], games))


def part_02(games) -> int:
    """Looks up second part of score tuple"""
    return reduce(operator.add, map(lambda x: SCORES[x][1], games))


def test_part_01():
    """Tests part 01"""
    games = [('A', 'Y'), ('B', 'X'), ('C', 'Z')]

    assert 15 == part_01(games)


def test_part_02():
    """Tests part 02"""
    games = [('A', 'Y'), ('B', 'X'), ('C', 'Z')]

    assert 12 == part_02(games)


def main() -> None:
    """Main wrapper."""
    games = load_input('./input')

    print(part_01(games))
    print(part_02(games))


if __name__ == "__main__":
    main()
