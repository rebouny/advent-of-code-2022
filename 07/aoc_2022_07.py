#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author : Martin Schuh <development@rebouny.net>
Date   : 2022-12-07
Purpose: Solves day 07 from advent of code 2022.
"""

from typing import Final, List
from dataclasses import dataclass
from functools import reduce
import operator


TOTAL: Final = 70000000
MIN_REQ: Final = 30000000

TEST_DATA: Final = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
"""


@dataclass
class Node:
    """Base node class"""
    name: str


@dataclass
class Root(Node):
    """Node that has children"""
    children: list

    def get_size(self):
        """Returns size of contained elements"""
        return reduce(operator.add, map(lambda x: x.get_size(), self.children))

    def has_child(self, name: str):
        """Looks up certain property"""
        return name in list(map(lambda x: x.name, self.children))

    def get_child(self, name: str):
        """Retrieves certain property"""
        return list(filter(lambda x: x.name == name, self.children))[0]


@dataclass
class Dir(Root):
    """Node that has children and a parent"""
    parent: Node


@dataclass
class File(Node):
    """Node that has file size"""
    size: int

    def get_size(self):
        """Return stored file size"""
        return self.size


# --------------------------------------------------
def load_data(filename: str):
    """Loads complete input into multiline string"""
    with open(filename, 'rt', encoding='utf-8') as file:
        return file.read()


def parse_data(data: str):
    """Splits loaded data into commands"""
    return list(map(lambda x: x.rstrip(), data.split('\n')))


def part_01(data) -> int:
    """Solves part 01"""
    root = build_tree(parse_data(data))

    items = []
    find_dirs(root, items)

    filtered = list(filter(lambda x: x.get_size() <= 100000, items))

    return reduce(operator.add, map(lambda x: x.get_size(), filtered))


def part_02(data) -> int:
    """solves part 02"""
    root = build_tree(parse_data(data))

    items = []
    find_dirs(root, items)

    used = root.get_size()
    needed = MIN_REQ - (TOTAL - used)

    return sorted(filter(lambda x: x.get_size() > needed, items),
                  key=lambda x: x.get_size()
                  )[0].get_size()


def build_tree(lines: List[str]):
    """Parses list of commands into tree structure"""
    cur = root = Root(name='/', children=[])

    for line in lines:
        if not line or line == '$ ls':
            continue
        if line[0:4] == '$ cd':
            path = line[5:]
            if path == '/':
                cur = root
            elif path == '..' and 'parent' in cur.__dict__:
                cur = cur.__dict__['parent']
            elif cur.has_child(path):
                cur = cur.get_child(path)
            continue

        info, name = line.split()
        cur.children.append(Dir(name=name, parent=cur, children=[]) if info == 'dir'
                            else File(name=name, size=int(info)))

    return root


def find_dirs(node, items):
    """Recursivly collects Dirs in tree"""
    items.append(node)
    for child in filter(lambda x: not isinstance(x, File), node.children):
        find_dirs(child, items)


# --------------------------------------------------
def test_part_01():
    """Tests part 01"""
    assert 95437 == part_01(TEST_DATA)


def test_part_02():
    """Tests part 02"""
    assert 24933642 == part_02(TEST_DATA)


# --------------------------------------------------
def main() -> None:
    """Main wrapper."""
    data = load_data('./input')

    print(part_01(data))
    print(part_02(data))


if __name__ == '__main__':
    main()
