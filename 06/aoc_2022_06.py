#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author : Martin Schuh <development@rebouny.net>
Date   : 2022-12-05
Purpose: Solves day 06 from advent of code 2022.
"""

from typing import Final


TEST_DATA_PART_01: Final = [
    ("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 7),
    ("bvwbjplbgvbhsrlpgdmjqwftvncz", 5),
    ("nppdvjthqldpwncqszvftbrmjlhg", 6),
    ("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 10),
    ("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 11)
]

TEST_DATA_PART_02: Final = [
    ("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 19),
    ("bvwbjplbgvbhsrlpgdmjqwftvncz", 23),
    ("nppdvjthqldpwncqszvftbrmjlhg", 23),
    ("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 29),
    ("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 26)
]


# --------------------------------------------------
def load_data(filename: str):
    """Loads complete input into a string"""
    with open(filename, 'rt', encoding='utf-8') as file:
        return file.read().rstrip()


def solve(data: str, packet_size: int) -> int:
    """Solves both parts"""
    return list(map(lambda x: len(set(data[x-packet_size:x])) == packet_size,
                    range(packet_size, len(data) + 1)
                    )
                ).index(True) + packet_size


def solve_conventionally(data: str, packet_size: int) -> int:
    """Solves by 'conventional' way"""
    for i in range(packet_size, len(data) + 1):
        if len(set(data[i-packet_size:i])) == packet_size:
            return i
    return -1


# --------------------------------------------------
def test_part_01():
    """Tests part 01"""
    data = TEST_DATA_PART_01

    for test in data:
        assert test[1] == solve(test[0], 4)


def test_part_02():
    """Tests part 02"""
    data = TEST_DATA_PART_02

    for test in data:
        assert test[1] == solve(test[0], 14)


# --------------------------------------------------
def main() -> None:
    """Main wrapper."""
    data = load_data('./input')
    print(solve(data, 4))
    print(solve(data, 14))


if __name__ == '__main__':
    main()
