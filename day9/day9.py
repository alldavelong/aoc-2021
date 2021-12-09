#!/usr/bin/env python3

file = open('input.txt')
# file = open('test.txt')
lines = file.read().splitlines()
file.close()

def find_low_points(points:list[list]) -> list:
    low_points = []
    for y in range(len(points)):
        for x in range(len(points[0])):
            surrounding = []
            if x != 0: surrounding.append(points[y][x-1])
            if x != len(points[0])-1: surrounding.append(points[y][x+1])
            if y != 0: surrounding.append(points[y-1][x])
            if y != len(points)-1: surrounding.append(points[y+1][x])
            if points[y][x] < min(surrounding): low_points.append((x,y))
    return(low_points)

def part1(points:list[list], low_points:list[tuple]):
    print('risk level = %d' % sum(
        [points[coord[1]][coord[0]]+1 for coord in low_points]
        ))

def find_basin(points:list[list], low:tuple) -> list[tuple]:
    basin_tuples = [low]
    basin_index = 0
    while True:
        x,y = basin_tuples[basin_index][0], basin_tuples[basin_index][1]
        for offset in [(-1,0),(0,-1),(1,0),(0,1)]:
            x_add, y_add = offset
            if x+x_add < 0 or x+x_add >= len(points[0]) or y+y_add < 0 or y+y_add >= len(points): continue
            if points[y+y_add][x+x_add] > points[y][x]:
                current = (x+x_add,y+y_add)
                if current in basin_tuples or points[current[1]][current[0]] == 9: continue
                # print('adding: %s after %d of low %s' % (current, basin_index, basin_tuples[0]))
                basin_tuples.append(current)
        if len(basin_tuples) > basin_index + 1:
            basin_index += 1
        else: break
    return(basin_tuples)
                
def find_all_basin_sizes(points:list[list], low_points:list[tuple]) -> list[int]:
    basin_sizes = []
    for low in low_points:
        basin_tuples = find_basin(points, low)
        basin_sizes.append(len(basin_tuples))
    return(basin_sizes)


def part2(points:list[list], low_points:list[tuple]):
    basin_sizes = find_all_basin_sizes(points, low_points)
    biggest_3_basins = sorted(basin_sizes)[-3:]
    print('product of %s = %d' % (biggest_3_basins, biggest_3_basins[0]*biggest_3_basins[1]*biggest_3_basins[2]))

def main():
    points = [[int(char) for char in line] for line in lines]
    low_points = find_low_points(points)
    part1(points, low_points)
    part2(points, low_points)

main()