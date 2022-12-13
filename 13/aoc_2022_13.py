#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author : Martin Schuh <development@rebouny.net>
Date   : 2022-12-13
Purpose: Solves day 13 from advent of code 2022.

Function compare_items is rather complex. I tried to factor out some return statements so pylint
scores well but sonarlint still doesn't like the amount of conditions.
"""

from typing import Final
from dataclasses import dataclass
from functools import reduce, cmp_to_key
import operator
import json

TEST_DATA: Final = """[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]"""


@dataclass
class PacketPair:
    """Container for a pair of packets"""
    index: int
    left: list
    right: list


def check_ordered(pair: PacketPair):
    """Recursivly compares a pait of packts.
    If left ist 'smaller' or both are identical return true
    """
    return compare_items(pair.left, pair.right) < 1#!= 1


def compare_items(left, right) -> int:
    """Comparses items/lists:
    Returns
    <0 if left is smaller
     0 if both are equal (continue checking)
    >0 if right is smaller (error case)
    """
    if not left:
        return 0 if not right else -1
    if not right:
        return 1

    if isinstance(left, int) and isinstance(right, int):
        return left - right

    left = [left] if isinstance(left, int) else left
    right = [right] if isinstance(right, int) else right

    left_len = len(left)
    right_len = len(right)

    for i in range(max(left_len, right_len)):
        if i >= left_len or i >= right_len:
            return -1 if i >= left_len else 1

        val = compare_items(left[i], right[i])
        if val != 0:
            return val

    return 0


def parse_pair(data: str, index) -> PacketPair:
    """Converts data to pairs of packets"""
    left, right = data.split('\n')

    return PacketPair(
        index=index,
        left=json.loads(left),
        right=json.loads(right)
    )


# --------------------------------------------------
def load_data(filename: str):
    """Loads data into single string"""
    with open(filename, 'rt', encoding='utf-8') as file:
        return file.read().rstrip()


def parse_data(data) -> list[PacketPair]:
    """Parses data into list of pairs"""
    return [parse_pair(x, i) for i, x in enumerate(data.split('\n\n'), start=1)]


def part_01(pairs) -> int:
    """Solves part 01"""

    return reduce(operator.add, [pair.index if check_ordered(pair) else 0 for pair in pairs])


def part_02(pairs) -> int:
    """solves part 02"""

    flat_pairs = [pair.right for pair in pairs] + [pair.left for pair in pairs] + [[[2]], [[6]]]

    sorted_list = sorted(flat_pairs, key=cmp_to_key(compare_items))

    return reduce(operator.mul, [sorted_list.index([[2]]) + 1, sorted_list.index([[6]]) + 1])


# --------------------------------------------------
def test_part_01():
    """Tests part 01"""
    pairs = parse_data(TEST_DATA)

    assert 13 == part_01(pairs)


def test_part_02():
    """Tests part 02"""
    data = parse_data(TEST_DATA)
    assert 140 == part_02(data)


# --------------------------------------------------
def main() -> None:
    """Main wrapper."""
    data = parse_data(load_data('./input'))

    print(part_01(data))
    print(part_02(data))


if __name__ == '__main__':
    main()
