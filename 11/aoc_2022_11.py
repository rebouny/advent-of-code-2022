#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author : Martin Schuh <development@rebouny.net>
Date   : 2022-12-11
Purpose: Solves day 11 from advent of code 2022.

I got stuck on part two for quite some time and even a hint from my collegue didn't get me a clue
until I found this one

https://fasterthanli.me/series/advent-of-code-2022/part-11#math-check

Yeah, fully agree on that, lack of math skills may lead to frustration. Thank for the final tip,
this one my brain understood ;)
"""

from typing import Final
from dataclasses import dataclass
import operator
from functools import reduce


TEST_DATA: Final = """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1"""


@dataclass
class Monkey:
    """Monkey storage container"""
    identifier: int
    items: list[int]
    operation: tuple[str, str, str]
    test: int
    route_true: int
    route_false: int


OP_MAP: Final = {
    '+': operator.add,
    '*': operator.mul
}


# --------------------------------------------------
def load_data(filename: str):
    """Load input into one string"""
    with open(filename, 'rt', encoding='utf-8') as file:
        return file.read().rstrip()


def parse_data(data):
    """Splits up input by calling parser for monkeys"""
    return [parse_monkey(monkey) for monkey in data.split('\n\n')]


def parse_monkey(monkey):
    """Parses string into monkey object"""
    m_l = monkey.split('\n')

    return Monkey(
        identifier=int(m_l[0][7:-1]),
        items=list(map(int, m_l[1].split(':')[1].split(', '))),
        operation=m_l[2][19:].split(),
        test=int(m_l[3][21:]),
        route_true=int(m_l[4][29:]),
        route_false=int(m_l[5][30:])
    )


def calc_level(old, operation):
    """Calculates next worry level"""
    left = old if operation[0] == 'old' else int(operation[0])
    right = old if operation[2] == 'old' else int(operation[2])

    return OP_MAP[operation[1]](left, right)


def part_01(data) -> int:
    """Solves part 01"""
    rounds = 20

    business = {x.id: 0 for x in data}

    for _ in range(rounds):
        for monkey in data:
            for j in monkey.items:
                business[monkey.id] += 1
                level = calc_level(j, monkey.op) // 3

                if level % monkey.test == 0:
                    data[monkey.route_true].items.append(level)
                else:
                    data[monkey.route_false].items.append(level)
            monkey.items = []

    return reduce(operator.mul, map(lambda x: business[x],
                  sorted(business, key=lambda x: business[x], reverse=True)[:2]))


def part_02(data) -> int:
    """solves part 02"""
    rounds = 10000

    business = {x.id: 0 for x in data}

    mod_factor = reduce(operator.mul, map(lambda x: x.test, data))

    for _ in range(rounds):
        for monkey in data:
            for j in monkey.items:
                business[monkey.id] += 1

                level = calc_level(j, monkey.op) % mod_factor

                if level % monkey.test == 0:
                    data[monkey.route_true].items.append(level)
                else:
                    data[monkey.route_false].items.append(level)
            monkey.items = []

    return reduce(operator.mul, map(lambda x: business[x],
                  sorted(business, key=lambda x: business[x], reverse=True)[:2]))


# --------------------------------------------------
def test_part_01():
    """Tests part 01"""
    data = parse_data(TEST_DATA)
    assert 10605 == part_01(data)


def test_part_02():
    """Tests part 02"""
    data = parse_data(TEST_DATA)
    assert 2713310158 == part_02(data)


# --------------------------------------------------
def main() -> None:
    """Main wrapper."""
    data = parse_data(load_data('./input'))
    print(part_01(data))

    data = parse_data(load_data('./input'))
    print(part_02(data))


if __name__ == '__main__':
    main()
