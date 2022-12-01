#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Solves first day of aoc 2022.
"""

from functools import reduce
import operator
from typing import List


def load_input(filename: str) -> List[List[int]]:
    """Loads and parses elves and their cargo"""
    with open(filename, 'rt', encoding='utf-8') as file:
        return list(
            map(lambda x: list(map(int, x.rstrip().split('\n'))),
                file.read().split('\n\n'))
                )


def part_01(elves: List[List[int]]) -> None:
    """Heaviest cargo"""
    print(reduce(max, map(sum, elves)))


def part_02(elves: List[List[int]]) -> None:
    """Three most heavy cargos"""
    print(reduce(operator.add, sorted(map(sum, elves))[-3:]))


def main() -> None:
    """Main wrapper."""
    elves = load_input('./input')

    part_01(elves)
    part_02(elves)


if __name__ == "__main__":
    main()
