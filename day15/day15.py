#!/usr/bin/env python3

file = open('input.txt')
# file = open('test.txt')
GRID = [[int(x) for x in y] for y in file.read().splitlines()]
file.close()

import math

class GridNode:
    def __init__(self, risk:int, coords:tuple) -> None:
        self.risk = risk
        self.coords = coords
        self.distance = math.inf
        self.neighbours = []
        self.visited = False
        self.previous = None

    def __lt__(self, other):
        return self.distance < other.distance
    
    def add_neighbours(self, neighbours):
        for neighbour in neighbours:
            self.neighbours.append(neighbour)

    @staticmethod
    def init_node_list_from_grid(grid:list[list]) -> list:
        grid_nodes = [line.copy() for line in grid]
        node_list = []
        for x in range(len(grid_nodes[0])):
            for y in range(len(grid_nodes)):
                if type(grid_nodes[y][x]) == int:
                    grid_nodes[y][x] = GridNode(grid_nodes[y][x], (x, y))
                neighbours = []
                for i in [(-1,0), (0,-1), (1,0), (0,1)]:
                    dx, dy = i[0], i[1]
                    if x+dx < 0 or x+dx >= len(grid_nodes[0]) or y+dy < 0 or y+dy >= len(grid_nodes):
                        continue
                    if type(grid_nodes[y+dy][x+dx]) == int:
                        grid_nodes[y+dy][x+dx] = GridNode(grid_nodes[y+dy][x+dx], (x+dx, y+dy))
                    neighbours.append(grid_nodes[y+dy][x+dx])
                grid_nodes[y][x].add_neighbours(tuple(neighbours))
                node_list.append(grid_nodes[y][x])
        return node_list

def dijkstra(nodes:list[GridNode]):
    nodes[0].distance = 0
    queue = [nodes[0]]
    count = 0
    total_positions = len(nodes)
    while len(queue):
        count += 1
        if count % 1000 == 0: print('checked %d%% (%d of %d)' % (count/total_positions*100, count, total_positions), end='\r')
        current = queue.pop(0)
        for neighbour in current.neighbours:
            if neighbour.visited:
                continue
            new_distance = current.distance + neighbour.risk
            if new_distance < neighbour.distance:
                neighbour.distance = new_distance
                neighbour.previous = current
                if neighbour not in queue:
                    queue.append(neighbour)
                    # queue.sort(key=lambda x: x.distance) # this is much faster than queue.sort(), but less pretty
                    queue.sort() # uses __lt__() of the object
        current.visited = True
    print('\nDijkstra finished')

def part1():
    node_list = GridNode.init_node_list_from_grid(GRID)
    dijkstra(node_list)
    print('path risk: %d' % node_list[-1:][0].distance)

def make_increased_grid_copy(grid:list[list], increment=1) -> list[list]:
    increased_grid = [line.copy() for line in grid]
    for x in range(len(increased_grid[0])):
        for y in range(len(increased_grid)):
            new_value = increased_grid[y][x] + increment
            if new_value > 9:
                new_value = new_value - 9
            increased_grid[y][x] = new_value
    return increased_grid

def part2():
    bigger_grid = [line.copy() for line in GRID]

    for i in range(4):
        increased_grid = make_increased_grid_copy(GRID, i+1)
        for line_index in range(len(bigger_grid)):
            bigger_grid[line_index].extend(increased_grid[line_index])
    five_bigger_grids_in_a_row = [line.copy() for line in bigger_grid]
    for i in range(4):
        increased_grid = make_increased_grid_copy(five_bigger_grids_in_a_row, i+1)
        bigger_grid.extend(increased_grid)
    
    # for line in bigger_grid:
    #     print(''.join([str(s) for s in line]))

    node_list = GridNode.init_node_list_from_grid(bigger_grid)
    dijkstra(node_list)
    print('path risk: %d' % node_list[-1:][0].distance)

part1()
part2()