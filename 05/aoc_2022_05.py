#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Solves fifth day of aoc 2022.
"""

# pylint: disable=invalid-name

from typing import Final, List
import re


TEST_DATA: Final = [
    "    [D]    ",
    "[N] [C]    ",
    "[Z] [M] [P]",
    " 1   2   3 ",
    "",
    "move 1 from 2 to 1",
    "move 3 from 1 to 3",
    "move 2 from 2 to 1",
    "move 1 from 1 to 2",
]


def load_data(filename: str):
    """Loads input file"""
    with open(filename, 'rt', encoding='utf-8') as file:
        return parse_data(list(map(lambda x: x.rstrip(), file.readlines())))


def parse_cmd(cmd: str):
    """parses a command into relvant"""
    m = re.match(r'move\ (\d+)\ from\ (\d+)\ to\ (\d+)', cmd)
    return tuple((int(m.group(1)), int(m.group(2)), int(m.group(3)))) if m else (None, None, None)


def parse_data(data: List[str]):
    """Loads input into stacks and list of commands stored as tuples"""

    idx = data.index('')

    stacks_data = data[0:idx]
    commands_data = data[idx+1:]

    num_stacks = int(stacks_data.pop().split()[-1])
    stacks = [[] for _ in range(num_stacks)]

    for s in stacks_data:
        for i in range(num_stacks):
            if s[i*4:i*4+3].strip():
                stacks[i].insert(0, s[i*4+1])

    commands = list(map(parse_cmd, commands_data))

    return stacks, commands


def part_01(stacks, commands) -> str:
    """Crane can only move one item at  time"""
    _ = [[stacks[t-1].append(stacks[f-1].pop()) for _ in range(a)] for a, f, t in commands]

    return ''.join([s[-1] for s in stacks])


def part_02(stacks, commands) -> str:
    """Crane can move multiple items at time"""
    for a, f, t in commands:
        stacks[t-1].extend(stacks[f-1][-a:])
        stacks[f-1] = stacks[f-1][0:-a]

    return ''.join([s[-1] if s else ' ' for s in stacks])


def test_parse_input():
    """Test load parsing data"""
    stacks, commands = parse_data(TEST_DATA)
    assert [['Z', 'N'], ['M', 'C', 'D'], ['P']] == stacks
    assert [(1, 2, 1), (3, 1, 3), (2, 2, 1), (1, 1, 2)] == commands


def test_part_01():
    """Tests part 01"""
    stacks, commands = parse_data(TEST_DATA)
    assert 'CMZ' == part_01(stacks, commands)


def test_part_02():
    """Tests part 02"""
    stacks, commands = parse_data(TEST_DATA)
    assert 'MCD' == part_02(stacks, commands)


def main() -> None:
    """Main wrapper."""
    print(part_01(*load_data('./input')))
    print(part_02(*load_data('./input')))


if __name__ == "__main__":
    main()
