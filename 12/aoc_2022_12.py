#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author : Martin Schuh <development@rebouny.net>
Date   : 2022-12-12
Purpose: Solves day 12 from advent of code 2022.
"""

from typing import Final
import queue as q


TEST_DATA: Final = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""


START: Final = ord('S') - ord('a') + 1 
END: Final = ord('E') - ord ('a') + 1



# --------------------------------------------------
def load_data(filename: str):
    with open(filename, 'rt', encoding='utf-8') as file:
        return file.read().rstrip()


def parse_data(data):
    return [ [(ord(x)-ord('a')) + 1 for x in line] for line in data.split('\n')]


def get_path_coords(matrix):
    start = end = None

    rows = len(matrix)

    for i in range(rows):
        if START in matrix[i]:
            start = (i, matrix[i].index(START))
        if END in matrix[i]:
            end = (i, matrix[i].index(END))

    return (start, end)


def check_neighbour(matrix, i, j):
    possibles = list()
    height = matrix[i][j]
    rows = len(matrix)
    cols = len(matrix[0])
    
    if i>0 and matrix[i-1][j] - height <= 1:
        possibles.append((i-1, j))
    if i+1<rows and matrix[i+1][j] - height <= 1:
        possibles.append((i+1, j))
    if j>0 and matrix[i][j-1] - height <= 1:
        possibles.append((i, j-1))
    if j+1<cols and matrix[i][j+1] - height <= 1:
        possibles.append((i, j+1))

    return possibles


def build_matrix(data):
    adj_list = {}

    rows = len(data)
    cols = len(data[0])

    start, end = get_path_coords(data)
    if not (start and end):
        return -1

    data[start[0]][start[1]] = 0
    data[end[0]][end[1]] = 27


    for i in range(rows):
        for j in range(cols):
            adj_list[(i, j)] = check_neighbour(data, i, j)

    return adj_list, start, end


def depth_first_search_iterative(adj, start, end):
    stack, path = [start], []

    while stack:
        vertex = stack.pop()
        if vertex in path:
            continue
        if vertex == end:
            return path
        path.append(vertex)
        
        for neighbor in adj[vertex]:
            stack.append(neighbor)

    return path


def deepth_first_search_recursive(adj, start, end, visited):
    # adj ist die Adjazenzliste {knoten: [kanten]}
    # start ist der Knoten, um die Suche zu beginnen
    # suche ist der gesuchte Knoten
    if start == end:
        return True
    if adj[start]:
        for node in filter(lambda x: x not in visited, adj[start]):
            visited.append(node)
            if deepth_first_search_recursive(adj, node, end, visited):
                return True
    return False


def breadth_search(adj, start, end):
    # adj ist die Adjazenzliste {knoten: [kanten]}
    # start ist der Index des Knoten, in dem die Suche beginnt
    # suche ist der gesuchte Knoten
    queue = q.Queue()
    queue.put(start)
    visited = []
    found = False
    pathway = {}
    path = []
    while not found and queue.qsize() > 0:
        active_node = queue.get()
        visited.append(active_node)
        for another_node in adj[active_node]:
            if another_node in visited:
                continue
            pathway[another_node] = active_node
            if another_node == end:
                found = True
                break
            queue.put(another_node)

    if found:
        previous = end
        while (previous != start):
            path.insert(0, previous)
            previous = pathway[previous]
        return len(path)

    return -1


def dijkstra(vertices, edges, start, end):
    """Dijkstra implementation copied from
    https://de.wikibooks.org/wiki/Algorithmensammlung:_Graphentheorie:_Dijkstra-Algorithmus

    We need a list of vertices and tuples of source, destination vertex as well as the costs
    (constant 1).

    Returns the path (including stop element, therefore we reduce it by one)
    """
    vertex_properties = [ [i, float('inf'), None, False] for i in vertices if i != start ]
    vertex_properties += [ [start, 0, None, False] ]
    for i in range(len(vertex_properties)):
    	vertex_properties[i] += [i]
        
    while True:
        unvisited_vertex_iter = filter(lambda x: not x[3], vertex_properties)
        unvisited_vertex = list(unvisited_vertex_iter)
        if not unvisited_vertex:
            break

        sorted_list = sorted(unvisited_vertex, key=lambda i: i[1])
        active_vertex = sorted_list[0]
        vertex_properties[active_vertex[4]][3] = True
        
        if active_vertex[0] == end:
            break
        active_edges = list(filter(lambda x: x[0] == active_vertex[0], edges))
        for edge in active_edges:
            other_vertices_list=list(filter(lambda x: x[0] == edge[1], vertex_properties))
            other_vertex_id=other_vertices_list[0][4]
            weighted_sum = active_vertex[1]	+ edge[2]
            if weighted_sum < vertex_properties[other_vertex_id][1]:
                vertex_properties[other_vertex_id][1] = weighted_sum
                vertex_properties[other_vertex_id][2] = active_vertex[4]

    
    if active_vertex[0] == end:
        path = []
        path += [ active_vertex[0] ]
    	
        costs = active_vertex[1]
        while active_vertex[0] != start:
            active_vertex = vertex_properties[active_vertex[2]]
            path += [ active_vertex[0] ]

        path.reverse()
        return (path, costs)
    else:
    	raise "Kein Weg gefunden"

        

def part_01(data) -> int:
    """Solves part 01"""
    adj, start, end = build_matrix(data)

    vertices = []
    edges = []
    for key, targets in adj.items():
        vertices.append(key)
        for target in targets:
            edges.append((key, target, 1))


    #visited = []
    #return breadth_search(adj, start, end)
    #return deepth_first_search(adj, start, end, visited)
    #return len(depth_first_search_iterative(adj, start, end))
    path, costs = dijkstra(vertices, edges, start, end)
    return len(path) -1
    

def part_02(data) -> int:
    """solves part 02"""
    adj, start, end = build_matrix(data)

    vertices = []
    edges = []
    for key, targets in adj.items():
        vertices.append(key)
        for target in targets:
            edges.append((key, target, 1))

    path, _ = dijkstra(vertices, edges, start, end)
    
    path.pop()
    print(f'{path}')

    for vertex in reversed(path):
        if data[vertex[0]][vertex[1]] == 1:
            idx = path.index(vertex)
            print(f'idx={idx}')
            print(len(path[idx:]))
            
    
    return -1


# --------------------------------------------------
def test_part_01():
    """Tests part 01"""
    data = parse_data(TEST_DATA)
    assert 31 == part_01(data)


def test_part_02():
    """Tests part 02"""
    data = parse_data(TEST_DATA)
    assert 29 == part_02(data)


# --------------------------------------------------
def main() -> None:
    """Main wrapper."""
    #data = parse_data(load_data('./input'))
    data = parse_data(TEST_DATA)
    print(part_01(data))
    data = parse_data(TEST_DATA)
    print(part_02(data))
 

if __name__ == '__main__':
    main()
