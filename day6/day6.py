#!/usr/bin/env python3

file = open('input.txt')
# file = open('test.txt')
numbers = [int(num) for num in file.read().split(',')]
file.close()

class Lanternfish:
    RESET_VALUE = 6
    def __init__(self, value=8):
        self.value = value

    @staticmethod
    def evolve(all_fish):
        new_fish = []
        for fish in all_fish:
            if fish.value == 0:
                new_fish.append(Lanternfish())
                fish.value = Lanternfish.RESET_VALUE
            else:
                fish.value -= 1
        all_fish.extend(new_fish)

    @staticmethod
    def printfish(all_fish):
        print('list:')
        print([fish.value for fish in all_fish])

def part1():
    fish = []
    for num in numbers:
        fish.append(Lanternfish(num))
    Lanternfish.printfish(fish)
    for i in range(80):
        Lanternfish.evolve(fish)
    print('number of fish: %d' % len(fish))

def calc_evolve(times:list):
    num_of_new = times[0]
    for i in range(len(times)-1):
        times[i] = times[i+1]
    times[6] += num_of_new
    times[8] = num_of_new

def part2():
    time_til_spawn = [0]*9
    # each list index contains number of fish with time until next spawn = 0 to 8 
    for num in numbers:
        time_til_spawn[num] += 1
    for i in range(256):
        calc_evolve(time_til_spawn)
    print('number of fish: %d' % sum(time_til_spawn))

#part1()
part2()
