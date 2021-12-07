#!/usr/bin/env python3

import statistics
import math

file = open('input.txt')
# file = open('test.txt')
numbers = [int(num) for num in file.read().split(',')]
file.close()

def part1():
    closest_center = statistics.median(numbers)
    cost = sum([abs(num - closest_center) for num in numbers])
    print('constant cost to optimal center %d = %d' % (closest_center, cost))


def calc_increasing_cost(center:int, nums:list[int]):
    return sum([sum(range(1,abs(num - center)+1)) for num in nums])

def part2():
    closest_center = sum(numbers) / len(numbers)
    center_floor, center_ceil = math.floor(closest_center), math.ceil(closest_center)
    cost = {}
    cost[center_floor] = calc_increasing_cost(center_floor, numbers)
    cost[center_ceil] = calc_increasing_cost(center_ceil, numbers)
    better_center = center_floor if cost[center_floor] < cost[center_ceil] else center_ceil

    print('increasing cost to optimal center %d = %d' % (better_center, cost[better_center]))



part1()
part2()