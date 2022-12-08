#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author : Martin Schuh <development@rebouny.net>
Date   : 2022-12-08
Purpose: Solves day 08 from advent of code 2022.
"""

from typing import Final
from functools import reduce
import operator


TEST_DATA: Final = """30373
25512
65332
33549
35390"""


# --------------------------------------------------
def load_data(filename: str):
    """Loads input"""
    with open(filename, 'rt', encoding='utf-8') as file:
        return file.read().rstrip()


def parse_data(data):
    """Parses input data in matrix"""
    matrix = [list(x) for x in data.split('\n')]
    return len(matrix), len(matrix[0]), matrix


def is_invisible(patch, transposed, row, col) -> bool:
    """Test is given point is invisible"""
    return all([
                any(map(lambda x: x >= patch[row][col], patch[row][:col])),
                any(map(lambda x: x >= patch[row][col], patch[row][col + 1:])),
                any(map(lambda x: x >= transposed[col][row], transposed[col][:row])),
                any(map(lambda x: x >= transposed[col][row], transposed[col][row + 1:]))
               ])


def scenic_row(patch, row, items, height):
    """calculates scenic value when peeking inside a row"""
    for i in items:
        yield 1
        if height <= patch[row][i]:
            break


def scenic_col(patch, col, items, height):
    """calculates scenic value when peeking inside a col.
    I guess this second function can be left off when using
    transposed matrix, but I'm too lazy now for calculating
    adepted indicies"""
    for j in items:
        yield 1
        if height <= patch[j][col]:
            break


def scenic(patch, row, col) -> int:
    """Calculates scenic value for given point"""
    height = patch[row][col]

    return reduce(operator.mul,
                  [
                      sum(scenic_row(patch, row, range(col-1, -1, -1), height)),
                      sum(scenic_row(patch, row, range(col + 1, len(patch[0])), height)),
                      sum(scenic_col(patch, col, range(row - 1, -1, -1), height)),
                      sum(scenic_col(patch, col, range(row + 1, len(patch)), height))
                  ])


def part_01(patch, rows, cols) -> int:
    """Solves part 01"""
    transposed = list(map(list, zip(*patch)))

    # https://stackoverflow.com/questions/20820476/using-generator-instead-of-nested-loops
    count = sum((1 if is_invisible(patch, transposed, i, j) else 0
                for j in range(1, cols-1) for i in range(1, rows-1)))

    return cols * rows - count


def part_02(patch, rows, cols) -> int:
    """solves part 02"""

    return max((scenic(patch, i, j) for j in range(cols) for i in range(rows)))


# --------------------------------------------------
def test_part_01():
    """Tests part 01"""
    rows, cols, data = parse_data(TEST_DATA)
    assert 21 == part_01(data, rows, cols)


def test_part_02():
    """Tests part 02"""
    _, _, data = parse_data(TEST_DATA)

    assert 4 == scenic(data, 1, 2)
    assert 8 == scenic(data, 3, 2)


# --------------------------------------------------
def main() -> None:
    """Main wrapper."""
    rows, cols, data = parse_data(load_data('./input'))

    print(part_01(data, rows, cols))
    print(part_02(data, rows, cols))


if __name__ == '__main__':
    main()


# --------------------------------------------------
# obsolete code, just for presentation purpose
# --------------------------------------------------
def initialize(patch):
    """Initializes visibility matrix"""
    row_len = len(patch)
    col_len = len(patch[0])

    matrix = [[False] * col_len] * row_len

    matrix[0] = [True] * col_len
    for i in range(1, row_len - 2):
        matrix[i][0] = True
        matrix[i][col_len - 1] = True
    matrix[row_len - 1] = [True] * col_len

    return row_len, col_len, matrix


# def debug_tree(patch, transposed, row, col):

#     left = patch[row][:col]
#     right = patch[row][col + 1:]

#     top = transposed[col][:row]
#     bottom = transposed[col][row + 1:]

#     #print (f'{patch[row][col]}: {left} {right} / {top} {bottom}')

#     v_left = any(map(lambda x: x >= patch[row][col], patch[row][:col]))
#     v_right = any(map(lambda x: x >= patch[row][col], patch[row][col + 1:]))
#     v_top = any(map(lambda x: x >= transposed[col][row], transposed[col][:row]))
#     v_bottom = any(map(lambda x: x >= transposed[col][row], transposed[col][row + 1:]))

#     invisible = all([v_left, v_right, v_top, v_bottom])

#     print(f'{patch[row][col]} -> {invisible}: {v_left} {v_right} / {v_top} {v_bottom}')
#     #print (invisible)
#     # print(any(map(lambda x: x >= patch[row][col], patch[row][:col])))
#     # print(any(map(lambda x: x >= patch[row][col], patch[row][col + 1:])))

#     # print(any(map(lambda x: x >= transposed[col][row], transposed[col][:row])))
#     # print(any(map(lambda x: x >= transposed[col][row], transposed[col][row + 1:])))


#     # check row
#     # print(any(map(lambda x: x >= patch[row][col], patch[row][:col])))
#     # print(any(map(lambda x: x >= patch[row][col], patch[row][col + 1:])))

#     # print(any(map(lambda x: x >= transposed[col][row], transposed[col][:row])))
#     # print(any(map(lambda x: x >= transposed[col][row], transposed[col][row + 1:])))

#     # if any(map(lambda x: x >= patch[row][col], patch[row][:col]))\
#     #     and any(map(lambda x: x >= patch[row][col], patch[row][col + 1:]))\
#     #     and any(map(lambda x: x >= transposed[col][row], transposed[col][row + 1:]))\
#     #     and any(map(lambda x: x >= transposed[col][row], transposed[col][row + 1:])):
#     #     return False
#     # return True


# #rows, cols, visibility = initialize(patch)
# #debug_tree(patch, transposed, i, j)
# #visibility[i][j] = not invisible
# #print(f'p[{i}][{j}] = {patch[i][j]}: {visibility[i][j]}')

# #print(f'p[{i}][{j}] = {patch[i][j]}: {invisible} / {visibility[i][j]}')
