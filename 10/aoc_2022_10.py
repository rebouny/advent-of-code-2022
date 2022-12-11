#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author : Martin Schuh <development@rebouny.net>
Date   : 2022-12-11
Purpose: Solves day 10 from advent of code 2022.
"""

from typing import Final
from functools import reduce
import operator


TEST_DATA: Final = """addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop"""


TEST_DATA_02: Final = """##..##..##..##..##..##..##..##..##..##..
###...###...###...###...###...###...###.
####....####....####....####....####....
#####.....#####.....#####.....#####.....
######......######......######......####
#######.......#######.......#######....."""


# --------------------------------------------------
def load_data(filename: str):
    """Loads data into large string"""
    with open(filename, 'rt', encoding='utf-8') as file:
        return file.read().rstrip()


def parse_data(data):
    """Parsed commands. addx commands are treated like noop + real add"""
    cmds = []
    for line in data.split('\n'):
        cmds.append(0)
        if line != 'noop':
            cmds.append(int(line[5:]))

    return cmds


def part_01(data) -> int:
    """Solves part 01"""
    strengths = [1]

    for cmd in data:
        strengths.append(strengths[-1] + cmd)

    return reduce(operator.add, (map(lambda i: i * strengths[i-1], [20, 60, 100, 140, 180, 220])))


def part_02(data) -> str:
    """solves part 02"""
    sprite = [1]

    for cmd in data:
        sprite.append(sprite[-1] + cmd)

    crt = ["#" if sprite[i]-1 <= i % 40 <= sprite[i]+1 else "." for i in range(240)]

    return '\n'.join([
        reduce(lambda a, b: a+str(b), crt[i*40:(i+1)*40]) for i in range(6)
    ])


# --------------------------------------------------
def test_part_01():
    """Tests part 01"""
    data = parse_data(TEST_DATA)
    assert 13140 == part_01(data)


def test_part_02():
    """Tests part 02"""
    data = parse_data(TEST_DATA)
    assert TEST_DATA_02 == part_02(data)


# --------------------------------------------------
def main() -> None:
    """Main wrapper."""
    data = parse_data(load_data('./input'))

    print(part_01(data))
    print(part_02(data))


if __name__ == '__main__':
    main()
