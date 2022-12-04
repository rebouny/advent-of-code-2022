#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Solves fourth day of aoc 2022.

Treats elf assignment as set initialized from range.
"""

from typing import Final
from functools import reduce


# TEST_DATA: Final = [
#     ['2-4','6-8'],
#     ['2-3','4-5'],
#     ['5-7','7-9'],
#     ['2-8','3-7'],
#     ['6-6','4-6'],
#     ['2-6','4-8']
# ]

def split_elf(pair):
    return (tuple(map(int, pair[0].split('-'))),
            tuple(map(int, pair[1].split('-'))))


def load_data(filename: str):
    with open(filename, 'rt', encoding='utf-8') as file:
        pairs = [line.rstrip().split(',') for line in file.readlines()]

        return [split_elf(pair) for pair in pairs]
 

def elf_set(elf):
    return set(range(elf[0], elf[1] + 1))


def is_contained(left, right):
    return elf_set(left).issubset(elf_set(right)) or elf_set(right).issubset(elf_set(left))


def overlaps(left, right):
    return len(elf_set(left).intersection(elf_set(right))) > 0


def part_01(data) -> int:
    """Sums up contained pairs of elves"""
    return [is_contained(left, right) for left, right in data].count(True)


def part_02(data) -> int:
    """Sums up overlapping pairs of elves"""
    return [overlaps(left, right) for left, right in data].count(True)


# def test_part_01():
#     """Tests part 01"""
#     assert 157 == part_01(TEST_DATA)


# def test_part_02():
#     """Tests part 02"""
#     assert 70 == part_02(TEST_DATA)


def main() -> None:
    """Main wrapper."""
    data = load_data('./input')

    print(part_01(data))
    print(part_02(data))


if __name__ == "__main__":
    main()
