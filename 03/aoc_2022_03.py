#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Solves third day of aoc 2022.
"""

from typing import List, Final
import re
from functools import reduce
import operator


TEST_INPUT: Final = [
    'vJrwpWtwJgWrhcsFMMfFFhFp',
    'jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL',
    'PmmdzqPrVvPwwTWBwg',
    'wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn',
    'ttgJtRGJQctTZtZT',
    'CrZsJsPPZsGzwwsLwLmpwMDw'
]


def load_rucksacks(filename: str) -> List[str]:
    """Load elves cargo"""
    with open(filename, 'rt', encoding='utf-8') as file:
        return [line.rstrip() for line in file.readlines()]


def priority(char: str):
    """Returns priority of char"""
    return 1 + ord(char) - ord('a') if re.match('[a-z]', char)\
        else 26 + 1 + ord(char) - ord('A')


def badge(item: List[str]) -> str:
    """Returns badge of group of elves"""
    return list(set(filter(lambda x: x in item[1] and x in item[2], item[0])))[0]


def common(bag: str) -> str:
    """Find common char in bag"""
    return list(set(filter(lambda x: x in bag[:len(bag)//2], bag[len(bag)//2:])))[0]


def part_01(bags: List[str]) -> int:
    """Looks up first part of score tuple"""
    return reduce(operator.add, map(priority, map(common, bags)))


def part_02(bags: List[str]) -> int:
    """Split rucksacks into badges of three and get priotity of common char"""
    return reduce(operator.add,
                  map(priority, map(badge, [bags[i:i+3] for i in range(0, len(bags), 3)])))


def test_part_01():
    """Tests part 01"""
    assert 157 == part_01(TEST_INPUT)


def test_part_02():
    """Tests part 02"""
    assert 70 == part_02(TEST_INPUT)


def main() -> None:
    """Main wrapper."""
    bags = load_rucksacks('./input')

    print(part_01(bags))
    print(part_02(bags))


if __name__ == "__main__":
    main()
