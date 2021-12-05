#!/usr/bin/env python3

file = open('input.txt')
lines = file.readlines()
file.close()

def depth_pos_calculator():
    position_horizontal = 0
    depth = 0
    for line in lines:
        command_start = line[:2]
        if command_start == 'fo':
            position_horizontal += int(line[8:9])
        elif command_start == 'do':
            depth += int(line[5:6])
        elif command_start == 'up':
            depth -= int(line[3:4])
        else:
            print('not found')
        print('' + str(position_horizontal) + ' ' + str(depth))
    print(position_horizontal*depth)

def aim_calculator():
    position_horizontal = 0
    depth = 0
    aim = 0
    for line in lines:
        command_start = line[:2]
        if command_start == 'fo':
            value = int(line[8:9])
            depth += aim * value
            position_horizontal += value
        elif command_start == 'do':
            aim += int(line[5:6])
        elif command_start == 'up':
            aim -= int(line[3:4])
        else:
            print('not found')
    print('' + str(position_horizontal) + ' ' + str(depth))
    print(position_horizontal*depth)

# depth_pos_calculator()
aim_calculator()