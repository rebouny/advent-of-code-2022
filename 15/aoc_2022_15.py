#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author : Martin Schuh <development@rebouny.net>
Date   : 2022-12-15
Purpose: Solves day 15 from advent of code 2022.
"""

from typing import Final, Optional
from dataclasses import dataclass
import re
from pytest import fixture

RE_LINE: Final = re.compile(r'Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)')

TEST_DATA: Final = """Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3"""


@dataclass
class Sensor:
    """Stores a sensor and its beacon"""
    sensor_x: int
    sensor_y: int
    beacon_x: int
    beacon_y: int

    def __init__(self, s_x, s_y, b_x, b_y):
        """Initialization, calculates radius and bounding box as well"""
        self.sensor_x = s_x
        self.sensor_y = s_y
        self.beacon_x = b_x
        self.beacon_y = b_y
        self.radius = abs(s_x - b_x) + abs(s_y - b_y)
        self.box = self._init_bounding_box()  # we cache the box

    def _init_bounding_box(self):
        """Calculates bounding box, even if it's a square"""
        return (
            (self.sensor_x - self.radius, self.sensor_y - self.radius),
            (self.sensor_x + self.radius, self.sensor_y + self.radius)
        )

    def intersects(self, y_line: int):
        """CHeck of a given line intersects the bounding box (= intersects this object)"""
        return self.box[0][1] <= y_line <= self.box[1][1]

    def __str__(self):
        """Just for lazy debuggings sake"""
        return f's:({self.sensor_x},{self.sensor_y}),r={self.radius}'


def line_intersection(sensor: Sensor, y_line: int) -> list[tuple[int, int]]:
    """Returns list of forbidden coords"""
    dx_line = sensor.radius - abs(sensor.sensor_y - y_line)

    return [(x, y_line) for x in range(sensor.sensor_x - dx_line, 
                                       sensor.sensor_x + dx_line + 1)]


# --------------------------------------------------
def load_data(filename: str):
    """Loads whole file into string"""
    with open(filename, 'rt', encoding='utf-8') as file:
        return file.read().rstrip()


def parse_data(data: str) -> list[Sensor]:
    """Parses data into scanner objects"""
    sensors = []
    for line in data.split('\n'):
        match = RE_LINE.match(line)
        if (match):
            sensors.append(Sensor(*list(map(int, match.groups()))))

    return sensors


# def dump_grid(sensors):
#     g = [['.' for _ in range(26)] for _ in range(26) ]
#     rows = len(g)
#     cols = len(g[0])

#     #mark outside playground
#     for i in range(rows):
#         for j in range(cols):
#             if i > 20 or j > 20:
#                 g[i][j] = '/'

    
#     for s in sensors:
#         g[s.sensor_y][s.sensor_x] = 'S'
#         #g[s.beacon_y][s.beacon_x] = 'B'
#         mark_sensor(g, s)


#     for i in range(rows):
#         for j in range(cols):
#             print(f'{g[i][j]}', end='')
#         print()


# def mark_sensor(g, sensor: Sensor):
#     box = sensor.box

#     for i in range(box[0][1], box[1][1] + 1):
#         for j in range(box[0][0], box[1][0] + 1):
#             if 0 <= i <= 20 and 0 <= j <= 20:
#                 if (abs(i - sensor.sensor_y) + abs(j - sensor.sensor_x)) <= sensor.radius:
#                     if g[i][j] == '.':
#                         g[i][j] = '#'


def part_01(data, line) -> int:
    """Solves part 01"""

    forbidden = set()

    for sensor in data:
        if sensor.intersects(line):
            forbidden.update(line_intersection(sensor, line))

    beacons = set(map(lambda x: (x.beacon_x, x.beacon_y), filter(lambda x: x.beacon_y == line, data)))
    
    return len(forbidden) - len(beacons)
    

# def check_outside_sensor_range(sensors: list[Sensor], points: list[tuple[int, int]]) -> list[tuple[int, int]]:
#     outside = set()
#     for p in points:
#         for s in sensors:
#             distance = abs(s.sensor_x - p[0]) + abs(s.sensor_y - p[1])
#             if distance <= s.radius:
#                 continue
#             outside.add(p)

#     return list(outside)


def part_02(sensors: list[Sensor]):
    """Was meant to solve part 2, unfortunately..."""

    candidates = set()
    for s in sensors:
        for c in sensors:
            if s.sensor_x == c.sensor_x and s.sensor_y == c.sensor_y:
                continue
            distance = (abs(s.sensor_x - c.sensor_x) + abs(s.sensor_y - c.sensor_y)) - (s.radius + c.radius)
            if distance == 2:
                print(s, c)
                candidates.update(get_unreachable(s, c, sensors))

    print(candidates)
    for c in candidates:
        if 0 <= c[0] <= 4000000 and 0 <= c[1] <= 4000000:
            return c[0] * 4000000 + c[1]

    return -1


def get_unreachable(l: Sensor, r: Sensor, sensors) -> set[tuple[int, int]]:
    """Find unreachable points. So far - not very successful"""
    
    # contains edge points not caught by any sensors, len should be lte 1
    ep = set()
    
    #print(f'y: ({abs(min(l.sensor_y, r.sensor_y) - (max(l.sensor_y, r.sensor_y) + 1))}) x: ({abs(min(l.sensor_x, r.sensor_x) - (max(l.sensor_x, r.sensor_x) + 1))})')

    # y_half = (max(l.sensor_y, r.sensor_y) - min(l.sensor_y, r.sensor_y)) // 2
    # y_start = min(l.sensor_y, r.sensor_y) + y_half
    # x_half = (max(l.sensor_x, r.sensor_x) - min(l.sensor_x, r.sensor_x)) // 2
    # x_start = min(l.sensor_x, r.sensor_x) * x_half
    # percentage = l.radius / (l.radius + r.radius)
    # head_x = 1 if r.sensor_x >= l.sensor_x else -1
    # head_y = 1 if r.sensor_y >= l.sensor_y else -1

    # x_start = l.sensor_x + int(abs(l.sensor_x - r.sensor_x) * percentage) * head_x
    # y_start = l.sensor_y + int(abs(l.sensor_y - r.sensor_y) * percentage) * head_y

    # if (r.sensor_x - l.sensor_x) < 0 or (r.sensor_y - l.sensor_y):
    #     print((r.sensor_x, r.sensor_y), (l.sensor_x, l.sensor_y))

    # for y in range(min(l.sensor_y, r.sensor_y), max(l.sensor_y, r.sensor_y) + 1):
    #     for x in range(min(l.sensor_x, r.sensor_x), max(l.sensor_x, r.sensor_x) + 1):
    #diff = 1

    # for y in range(y_start - (diff * head_y), y_start + (diff + 1) * head_y, head_y):
    #     for x in range(x_start - (diff * head_y), x_start + (diff + 1) * head_x, head_x):
    #for point in calc_edge_points(l, r):

    # check smallest possible bounding box spun up by those edge points 
    p_0, p_1 = calc_edge_points(l, r)
    for y in range(min(p_0[1], p_1[1]), max(p_0[1], p_1[1]) + 1):
        for x in range(min(p_0[0], p_1[0]), max(p_0[0], p_1[0]) + 1):
            found = False
            print(f'checking ({x},{y})')
            for sensor in sensors:
                distance = abs(sensor.sensor_x - x) + abs(sensor.sensor_y - y)
                #distance = abs(sensor.sensor_x) - point[0] + abs(sensor.sensor_y - point[1])
                if distance <= sensor.radius:
                    print(f'\tp({x},{y}) with distance {distance} in s({sensor.sensor_x},{sensor.sensor_y}):r({sensor.radius})')
                    found = True
                    break
            
            # we did not break while scanning for sensors, so point is unreachable
            if not found and (0 <= x <= 4000000 and 0 <= y <= 4000000):
                ep.add((x, y))
        # if not found and (0 <= point[0] <= 4000000 and 0 <= point[1] <= 4000000):
        #     ep.add(point)

    return ep


# def part_02_not_working(sensors: list[Sensor]):

#     undetected = loop(4000000 + 1, 4000000 + 1, sensors)

#     if undetected:
#         print(undetected)
#         return undetected[0] * 4000000 + undetected[1]

#     return -1


# def loop(rows: int, cols: int, sensors: list[Sensor]) -> Optional[tuple[int, int]]:
#     for y in range(rows):
#         for x in range(cols):
#             caught = False
#             for s in sensors:
#                 if (abs(x - s.sensor_x) + abs(y - s.sensor_y)) <= s.radius:
#                     caught = True
#                     break
#             if not caught:
#                 return (x, y)
#     return None


# --------------------------------------------------
def __test_part_01():
    """Tests part 01"""
    data = parse_data(TEST_DATA)
    line = 10
    assert 26 == part_01(data, line)


def __test_part_02():
    """Tests part 02"""
    data = parse_data(TEST_DATA)
    assert 56000011 == part_02(data)


@fixture
def load_edge_position_data_1():
    data = parse_data("""Sensor at x=2926899, y=3191882: closest beacon is at x=2734551, y=2960647\nSensor at x=3486366, y=3717867: closest beacon is at x=3724687, y=3294321""")
    yield data

@fixture
def load_edge_position_data_2():
    data = parse_data("""Sensor at x=3358586, y=3171857: closest beacon is at x=3152133, y=2932891\nSensor at x=2736967, y=3632098: closest beacon is at x=2514367, y=3218259""")
    yield data

@fixture
def load_edge_position_data_3():
    data = parse_data("""Sensor at x=3486366, y=3717867: closest beacon is at x=3724687, y=3294321\nSensor at x=2926899, y=3191882: closest beacon is at x=2734551, y=2960647""")
    yield data

@fixture
def load_edge_position_data_4():
    data = parse_data("""Sensor at x=2736967, y=3632098: closest beacon is at x=2514367, y=3218259\nSensor at x=3358586, y=3171857: closest beacon is at x=3152133, y=2932891""")
    yield data


def test_edge_positions(load_edge_position_data_1):
    data = load_edge_position_data_1

    distance = abs(data[0].sensor_x - data[1].sensor_x) + abs(data[0].sensor_y - data[1].sensor_y)
    assert 2 == (distance - (data[0].radius + data[1].radius))


def test_edge_calculation_1(load_edge_position_data_1):
    sensors = load_edge_position_data_1

    edge_points = calc_edge_points(sensors[0], sensors[1])
    assert len(edge_points) == 2
    assert edge_points[0] == (3145223,3397141)
    assert edge_points[1] == (3145224,3397142)

def test_edge_calculation_2(load_edge_position_data_2):
    sensors = load_edge_position_data_2

    edge_points = calc_edge_points(sensors[0], sensors[1])
    assert len(edge_points) == 2
    assert edge_points[0] == (3102656,3361346)
    assert edge_points[1] == (3102654,3361346)

def test_edge_calculation_3(load_edge_position_data_3):
    sensors = load_edge_position_data_3

    edge_points = calc_edge_points(sensors[0], sensors[1])
    assert len(edge_points) == 2
    assert edge_points[0] == (3145224,3397142)
    assert edge_points[1] == (3145223,3397141)


def test_edge_calculation_4(load_edge_position_data_4):
    sensors = load_edge_position_data_4

    edge_points = calc_edge_points(sensors[0], sensors[1])
    assert len(edge_points) == 2
    assert edge_points[0] == (3102654,3361346)
    assert edge_points[1] == (3102656,3361346)

def calc_edge_points(left: Sensor, right: Sensor) -> tuple[tuple[int, int],tuple[int,int]]:
    dx = abs(left.sensor_x - right.sensor_x)
    dy = abs(left.sensor_y - right.sensor_y)
    head_x = 1 if right.sensor_x - left.sensor_x >= 0 else -1
    head_y = 1 if right.sensor_y - left.sensor_y >= 0 else -1
    distance = dx + dy
    delta = distance - left.radius - right.radius

    off_0_x = round(left.radius / distance * dx) * head_x
    off_0_y = round(left.radius / distance * dy) * head_y
    p_new_0 = (left.sensor_x + off_0_x, left.sensor_y + off_0_y)

    off_1_x = round(right.radius / distance * dx) * head_x * -1
    off_1_y = round(right.radius / distance * dy) * head_y * -1
    p_new_1 = (right.sensor_x + off_1_x, right.sensor_y + off_1_y)

    dx_new = abs(p_new_0[0] - p_new_1[0])
    dy_new = abs(p_new_0[1] - p_new_1[1])
    distance_new = dx_new + dy_new

    # print(f's:({left.sensor_x},{left.sensor_y}), r={left.radius}')
    # print(f's:({right.sensor_x},{right.sensor_y}), r={right.radius}')
    # print(f'dx={dx} dy={dy} head_x={head_x} head_y={head_y} dist={distance} delta={delta}')
    # print(f'left offset x={off_0_x}, y={off_0_y}')
    # print(f'edge left: ({p_new_0[0]},{p_new_0[1]})')
    # print(f'right offset x={off_1_x}, y={off_1_y}')
    # print(f'edge right: ({p_new_1[0]},{p_new_1[1]})')


    #print(f'new_distance {distance_new}')
    return (p_new_0, p_new_1)


    


# --------------------------------------------------
def main() -> None:
    """Main wrapper."""
    data = parse_data(load_data('./input'))
    #data = parse_data(TEST_DATA)
    #print(part_01(data, 10))
    
    # print(part_01(data, 2000000))

    print(part_02(data))
    

if __name__ == '__main__':
    main()
