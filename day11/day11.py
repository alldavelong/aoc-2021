#!/usr/bin/env python3

file = open("input.txt")
# file = open("test.txt")
lines = file.read().splitlines()
file.close()


class OctopusEnergyGrid:
    def __init__(self, grid: list[list]) -> None:
        self.grid = grid
        self.will_flash = []
        self.have_flashed = []
        self.flash_count = 0

    def print(self):
        for line in self.grid:
            print("".join(str(num) + ", " for num in line))

    def energy_step(self, number_of_steps=1, go_until_simultaneous_flash=False) -> int:
        step_no = 1
        while True:
            # print("rep %d:" % (step_no))
            for y in range(len(self.grid)):
                for x in range(len(self.grid[0])):
                    self.__increase((x, y))
            self.__flash()
            for coords in self.have_flashed:
                self.grid[coords[1]][coords[0]] = 0
            # self.print()
            if (
                go_until_simultaneous_flash
                and len(self.have_flashed) == len(self.grid) * len(self.grid[0])
                ): break
            elif (
                not go_until_simultaneous_flash
                and step_no >= number_of_steps
                ): break
            self.have_flashed = []
            step_no += 1
        return step_no

    def __increase(self, coords: tuple):
        x, y = coords[0], coords[1]
        self.grid[y][x] += 1
        if self.grid[y][x] > 9:
            if coords not in self.have_flashed and coords not in self.will_flash:
                self.will_flash.append((x, y))

    def __flash(self):
        while len(self.will_flash) > 0:
            self.flash_count += 1
            coords = self.will_flash.pop(0)
            self.__increase_surrounding(coords)
            self.have_flashed.append(coords)

    def __increase_surrounding(self, coords: tuple):
        x, y = coords[0], coords[1]
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                if (
                    (dy == 0 and dx == 0)
                    or dx + x < 0
                    or dx + x >= len(self.grid[0])
                    or dy + y < 0
                    or dy + y >= len(self.grid)
                ):
                    continue
                else:
                    self.__increase((x + dx, y + dy))


def part1():
    grid = OctopusEnergyGrid([[int(char) for char in line] for line in lines])
    grid.energy_step(100)
    print("%d flashes so far" % grid.flash_count)


def part2():
    grid = OctopusEnergyGrid([[int(char) for char in line] for line in lines])
    print('%d steps until simultaneous flash' % grid.energy_step(go_until_simultaneous_flash=True))


part1()
part2()
