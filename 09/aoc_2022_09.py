#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author : Martin Schuh <development@rebouny.net>
Date   : 2022-12-09
Purpose: Solves day 09 from advent of code 2022. Python 3.9+
"""

from typing import Final


TEST_DATA_01: Final = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2"""

TEST_DATA_02: Final = """R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20"""


MOVEMENTS: Final[dict[tuple[int, int], tuple[int,int]]] = {
    (-2, 1): (-1, 1), (-2, 0): (-1, 0), (-2, -1): (-1, -1),  # Left
    (-1, 2): (-1, 1), (0, 2): (0, 1), (1, 2): (1, 1),  # Up
    (2, 1): (1, 1), (2, 0): (1, 0), (2, -1): (1, -1),  # Right
    (-1, -2): (-1, -1), (0, -2): (0, -1), (1, -2): (1, -1),  # Down
    (2, 2): (1, 1), (2, -2): (1, -1), (-2, -2): (-1, -1), (-2, 2): (-1, 1)  # 2x2 cases
}


# --------------------------------------------------
def load_data(filename: str):
    """Load input."""
    with open(filename, 'rt', encoding='utf-8') as file:
        return file.read().rstrip()


def parse_data(data):
    """Splits input into commands"""
    return [(cmd[0], int(cmd[2:])) for cmd in data.split('\n')]


def move_t(pos_h: tuple[int, int], pos_t: tuple[int, int]):
    """Return modification to deal to pos_t"""
    if abs(pos_h[0] - pos_t[0]) < 2 and abs(pos_h[1] - pos_t[1]) < 2:
        return (0, 0)

    return MOVEMENTS[(pos_h[0] - pos_t[0], pos_h[1] - pos_t[1])]


def move_h(pos_h: tuple[int, int], direction: str) -> tuple[int, int]:
    """Moves 'head'. In quotes because tail elements can operate as 'head', too
    (relativly to their 'followers')"""
    if direction == 'R':
        return (pos_h[0] + 1, pos_h[1])
    if direction == 'L':
        return (pos_h[0] - 1, pos_h[1])
    if direction == 'U':
        return (pos_h[0], pos_h[1] + 1)
    # D
    return (pos_h[0], pos_h[1] - 1)


def part_01(data: list[tuple[str, int]]) -> int:
    """Solves part 01"""
    pos_h = (0, 0)
    pos_t = (0, 0)

    visited_t = set()
    visited_t.add((0, 0))
    for cmd, num in data:
        for _ in range(num):
            pos_h = move_h(pos_h, cmd)
            movement = move_t(pos_h, pos_t)
            if movement != (0, 0):
                pos_t = (pos_t[0] + movement[0], pos_t[1] + movement[1])
                visited_t.add(pos_t)

    return len(visited_t)


def part_02(data) -> int:
    """solves part 02"""
    pos_h = (0, 0)

    visited = [set() for _ in range(9)]
    pos_t = [(int(0), int(0)) for _ in range(9)]
    for i in range(9):
        visited[i].add(pos_t[i])

    for cmd, num in data:
        for _ in range(num):
            pos_h = move_h(pos_h, cmd)
            for i, pos in enumerate(pos_t):
                movement = move_t(pos_h if i == 0 else pos_t[i-1], pos)
                if movement == (0, 0):
                    break  # inner for loop, knots that follow don't need to be moved

                pos_t[i] = (pos[0] + movement[0], pos[1] + movement[1])
                visited[i].add(pos_t[i])

    return len(visited[-1])


# --------------------------------------------------
def test_part_01():
    """Tests part 01"""
    data = parse_data(TEST_DATA_01)
    assert 13 == part_01(data)


def test_part_02():
    """Tests part 02"""
    data = parse_data(TEST_DATA_02)
    assert 36 == part_02(data)


# --------------------------------------------------
def main() -> None:
    """Main wrapper."""
    data = parse_data(load_data('./input'))

    print(part_01(data))
    print(part_02(data))


if __name__ == '__main__':
    main()
