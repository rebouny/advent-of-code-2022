#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Solves fourth day of aoc 2022.

Treats elf assignment as set initialized from range.
"""

from typing import Final
from functools import reduce
import operator


TEST_DATA: Final = [
    ((2, 4), (6, 8)),
    ((2, 3), (4, 5)),
    ((5, 7), (7, 9)),
    ((2, 8), (3, 7)),
    ((6, 6), (4, 6)),
    ((2, 6), (4, 8))
]


def split_elf(pair):
    """Load helper: """
    return (tuple(map(int, pair[0].split('-'))),
            tuple(map(int, pair[1].split('-'))))


def load_data(filename: str):
    """Loads input into list of tuples of tuples of ints"""
    with open(filename, 'rt', encoding='utf-8') as file:
        return list(map(split_elf, map(lambda x: x.rstrip().split(','), file.readlines())))


def elf_set(elf):
    """Returns elves assignment as a set of ints"""
    return set(range(elf[0], elf[1] + 1))


def is_contained(left, right):
    """True if ones assignment is completely contained in the others"""
    return elf_set(left).issubset(elf_set(right)) or elf_set(right).issubset(elf_set(left))


def overlaps(left, right) -> bool:
    """True is two elves assignments have something in common"""
    return len(elf_set(left).intersection(elf_set(right))) > 0


def part_01(data) -> int:
    """Sums up contained pairs of elves"""
    return reduce(operator.add, map(lambda x: is_contained(x[0], x[1]), data))


def part_02(data) -> int:
    """Sums up overlapping pairs of elves"""
    return reduce(operator.add, map(lambda x: overlaps(x[0], x[1]), data))


def test_part_01():
    """Tests part 01"""
    assert 2 == part_01(TEST_DATA)


def test_part_02():
    """Tests part 02"""
    assert 4 == part_02(TEST_DATA)


def main() -> None:
    """Main wrapper."""
    data = load_data('./input')

    print(part_01(data))
    print(part_02(data))


if __name__ == "__main__":
    main()
