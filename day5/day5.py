#!/usr/bin/env python3

file = open('input.txt')
# file = open('test.txt')
data = file.read().splitlines()
file.close()

EMPTY_FIELD = '.'
import re

class CloudLine:
    max_value = 0

    def __init__(self, raw_string:str):
        self.values = [int(value) for value in re.split(',| -> ', raw_string)]
        # print(self.values)
        self.x1, self.y1, self.x2, self.y2 = self.values
        for i in self.values:
            if CloudLine.max_value < i:
                CloudLine.max_value = i

    @staticmethod
    def create_cloud_lines(data:list[str]) -> list:
        return [CloudLine(line) for line in data]

class Grid:
    def __init__(self, grid_size) -> None:
        self.grid = [[EMPTY_FIELD for i in range(grid_size+1)] for i in range(grid_size+1)]
        self.overlap_count = 0

    def __hit_position(self, x:int, y:int):
            if self.grid[y][x] == EMPTY_FIELD:
                self.grid[y][x] = 1
            else:
                self.overlap_count += self.grid[y][x] == 1
                self.grid[y][x] += 1

    def __draw_diagonal_line(self, line:CloudLine):
        if line.x1 == line.x2 or line.y1 == line.y2:
            return
        xmove = 1 if line.x2 > line.x1 else -1
        ymove = 1 if line.y2 > line.y1 else -1
        x, y = line.x1, line.y1
        while x != line.x2 + xmove:
            self.__hit_position(x,y)
            x, y = x+xmove, y+ymove


    def draw_line(self, line:CloudLine, consider_diagonal=False):
        if line.x1 == line.x2:
            min, max = sorted((line.y1, line.y2))
            for y in range(min, max + 1):
                self.__hit_position(line.x1,y)
        elif line.y1 == line.y2:
            min, max = sorted((line.x1, line.x2))
            for x in range(min, max + 1):
                self.__hit_position(x,line.y1)
        elif consider_diagonal:
            self.__draw_diagonal_line(line)


lines = CloudLine.create_cloud_lines(data)


def part1():
    grid1 = Grid(CloudLine.max_value)
    for line in lines:
        grid1.draw_line(line)
    # print(grid.grid)
    print('Part 1 overlaps: %d' % grid1.overlap_count)

def part2():
    grid2 = Grid(CloudLine.max_value)
    for line in lines:
        grid2.draw_line(line, True)
    # print(grid.grid)
    print('Part 2 overlaps: %d' % grid2.overlap_count)

part1()
part2()