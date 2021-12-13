#!/usr/bin/env python3

file = open('input.txt')
# file = open('test.txt')
coordinates, fold_instructions = file.read().split('\n\n')
file.close()

list_of_dots = [
    (int(line.split(',')[0]), int(line.split(',')[1]))
    for line in coordinates.splitlines()
    ]
fold_instructions = [
    (instruction.split()[-1].split('=')[0], int(instruction.split()[-1].split('=')[1]))
    for instruction in fold_instructions.splitlines()
    ]

def fold_paper(paper:list[tuple], fold_along_axis:chr, fold_index:int):
    changing_coordinate_index = fold_along_axis == 'y' # 1 if 'y', 0 if 'x'
    folded_paper = []
    for coordinate in paper:
        to_check = coordinate[changing_coordinate_index]
        if to_check == fold_index:
            continue
        if to_check < fold_index:
            to_append = coordinate # in unchanged half
        else:
            static_value = coordinate[not changing_coordinate_index]
            changed_value = fold_index - (to_check - fold_index)
            to_append = (
                (static_value, changed_value)
                if changing_coordinate_index == 1
                else (changed_value, static_value)
                )
        if to_append not in folded_paper: folded_paper.append(to_append)
    return folded_paper

def draw_paper(paper:list[tuple]):
    max_x, max_y = 0, 0
    for coord in paper:
        cx, cy = coord[0], coord[1]
        if cx > max_x: max_x = cx
        if cy > max_y: max_y = cy
    
    dot_matrix = [['.'] * (max_x + 1) for i in range(max_y + 1)]
    for x in range(max_x + 1):
        for y in range(max_y + 1):
            if (x,y) in paper:
                dot_matrix[y][x] = '#'
    return dot_matrix

def part1():
    folded_paper = fold_paper(list_of_dots, fold_instructions[0][0], fold_instructions[0][1])
    print('number of dots after first fold: %d' % len(folded_paper))

def part2():
    folded_paper = list_of_dots
    for instruction in fold_instructions:
            folded_paper = fold_paper(folded_paper, instruction[0], instruction[1])
    print('\nEight letter code to activate system:')
    for line in draw_paper(folded_paper): # draws the solution to the console
        print(''.join([char for char in line]))

part1()
part2()