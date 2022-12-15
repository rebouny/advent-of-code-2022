#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author : Martin Schuh <development@rebouny.net>
Date   : 2022-12-14
Purpose: Solves day 14 from advent of code 2022.
"""

from typing import Final, Optional
from functools import reduce
from itertools import chain
from dataclasses import dataclass


TEST_DATA: Final = """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9"""


SAND_SOURCE: Final[tuple[int, int]] = (500, 0)


@dataclass
class Cave:
    """Represents a cave with path of rocks, flooded sand and an optional floor."""
    rocks: set[tuple[int, int]]
    rested: set[tuple[int, int]]

    sand: Optional[tuple[int, int]]
    bounding_box: tuple[tuple[int, int], tuple[int, int]]

    def __init__(self, data, floor=False):
        """Initializes cave with path of rocks. Additionally provide floor."""
        self.sand = None
        self.rocks = set()
        self.rested = set()
        self._initialize(data, floor)

    def _initialize(self, data, floor) -> None:
        """Initializes cave with paths of rocks"""
        for path in data:
            line_path = path[:]
            while line_path:
                if len(line_path) == 1:
                    self.rocks.add(line_path[0])
                else:  # p[0] is start tuple, p[1] is end tuple, then [0] == x, [1] == y
                    if line_path[0][0] == line_path[1][0]:  # no diff on x axis
                        for i in range(min(line_path[0][1], line_path[1][1]),
                                       max(line_path[0][1], line_path[1][1]) + 1):
                            self.rocks.add((line_path[0][0], i))
                    else:
                        # p[0][1] == [p[1][1]]
                        for i in range(min(line_path[0][0], line_path[1][0]),
                                       max(line_path[0][0], line_path[1][0]) + 1):
                            self.rocks.add((i, line_path[0][1]))
                line_path.pop(0)

        box = bounding_box(data)
        if floor:
            y_coord = box[1][1] + 2
            x_start = SAND_SOURCE[0] - y_coord
            x_end = SAND_SOURCE[0] + y_coord

            for i in range(x_start, x_end + 1):
                self.rocks.add((i, y_coord))
            self.box = ((x_start - 1, SAND_SOURCE[1]), (x_end + 1, y_coord + 1))
        else:
            self.box = box

    def inside_box(self) -> bool:
        """Checks if recently spawned sand element is flawing into abyss"""
        if self.sand is None:
            return True
        if self.box[0][0] <= self.sand[0] <= self.box[1][0] and\
           self.box[0][1] <= self.sand[1] <= self.box[1][1]:
            return True

        return False

    def step(self) -> bool:
        """Processes on cycle. Fails if no additional steps can be processed
        (either bounding box is exceeded or spawning source is blocked)"""
        if not self.sand:
            return self.spawn_sand()

        val = self.move()

        if not val:
            self.rested.add(self.sand)
            return self.spawn_sand()

        return self.inside_box()

    def spawn_sand(self) -> bool:
        """Spawns another piece of sand. Fails is spawning source is already filled"""
        if SAND_SOURCE in self.rested:
            return False

        self.sand = SAND_SOURCE
        return True

    def move(self) -> bool:
        """Moves piece of sand one unit further. Fails is item is 'rested'
        (= no space to move to available)"""
        if not self.sand:
            return False

        # check down
        sand = (self.sand[0], self.sand[1] + 1)
        if sand not in self.rocks and sand not in self.rested:
            self.sand = sand
            return True
        # check down and left
        sand = (self.sand[0] - 1, self.sand[1] + 1)
        if sand not in self.rocks and sand not in self.rested:
            self.sand = sand
            return True
        # check down and right free
        sand = (self.sand[0] + 1, self.sand[1] + 1)
        if sand not in self.rocks and sand not in self.rested:
            self.sand = sand
            return True

        return False

    def get_rested_size(self):
        """Returns amount of spawned sand elements that now fills up the cave"""
        return len(self.rested)


# --------------------------------------------------
def load_data(filename: str):
    """Loads input into single string"""
    with open(filename, 'rt', encoding='utf-8') as file:
        return file.read().rstrip()


def parse_data(data):
    """Parses input into paths"""
    return [[tuple(map(int, cmd.split(','))) for cmd in line.split(' -> ')]
            for line in data.split('\n')]


def bounding_box(paths):
    """Calculates bounding box"""
    x_min = reduce(min, map(lambda x: x[0], chain(*paths)))
    x_max = reduce(max, map(lambda x: x[0], chain(*paths)))
    y_min = reduce(min, map(lambda x: x[1], chain(*paths)))
    y_max = reduce(max, map(lambda x: x[1], chain(*paths)))

    return (min(x_min, SAND_SOURCE[0]), min(y_min, SAND_SOURCE[1])),\
           (max(x_max, SAND_SOURCE[0]), max(y_max, SAND_SOURCE[1]))


def part_01(data) -> int:
    """Solves part 01"""

    cave = Cave(data)

    while True:
        if not cave.step():
            break

    return cave.get_rested_size()


def part_02(data) -> int:
    """solves part 02"""
    cave = Cave(data, floor=True)

    while True:
        if not cave.step():
            break

    return cave.get_rested_size()


# --------------------------------------------------
def test_part_01():
    """Tests part 01"""
    data = parse_data(TEST_DATA)
    assert 24 == part_01(data)


def test_part_02():
    """Tests part 02"""
    data = parse_data(TEST_DATA)
    assert 93 == part_02(data)


def test_bounding_box():
    """Tests general calculation of bounding boxes"""
    data = parse_data(TEST_DATA)

    assert ((494, 0), (503, 9)) == bounding_box(data)


# --------------------------------------------------
def main() -> None:
    """Main wrapper."""
    data = parse_data(load_data('./input'))

    print(part_01(data))
    print(part_02(data))


if __name__ == '__main__':
    main()
