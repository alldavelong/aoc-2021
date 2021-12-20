#!/usr/bin/env python3

file = open('input.txt')
# file = open('test.txt')
input = file.read().split('\n\n')
file.close()

enhancement_pattern = [1 if char == '#' else 0 for char in input[0]]
starting_input = input[1].splitlines()

class Image:
    def __init__(self, starting_light_pixels:dict[int, set[int]], padding_size:int):
        self.light_pixels = starting_light_pixels
        self.min_x, self.min_y = 0, 0
        self.max_x = self.__init_max_x()
        self.max_y = len(self.light_pixels) - 1
        self.PADDING, self.SIZE_INCREMENT = padding_size, 2
        self.outer_min_x = self.min_x - self.PADDING
        self.outer_min_y = self.min_y - self.PADDING
        self.outer_max_x = self.max_x + self.PADDING
        self.outer_max_y = self.max_y + self.PADDING
        self.__init_outer_rows()

    def __init_max_x(self):
        return max(max([[x for x in self.light_pixels[y]] for y in self.light_pixels.keys()]))

    def __init_outer_rows(self):
        for y in range(self.outer_min_y, self.min_y):
            self.light_pixels[y] = set()
        for y in range(self.max_y + 1, self.outer_max_y + 1):
            self.light_pixels[y] = set()

    def __increase_inner_range(self):
        self.min_x -= self.SIZE_INCREMENT
        self.min_y -= self.SIZE_INCREMENT
        self.max_x += self.SIZE_INCREMENT
        self.max_y += self.SIZE_INCREMENT

    def calculate_new_pixel_value(self, target_grid:dict[int, set[int]], x:int, y:int, enhancement_table:list) -> int:
        surrounding_binary = 0b0
        for dy in range(-1,2):
            for dx in range(-1,2):
                surrounding_binary = surrounding_binary << 1
                if (
                    x+dx < self.outer_min_x
                    or y+dy < self.outer_min_y
                    or x+dx > self.outer_max_x
                    or y+dy > self.outer_max_y
                ): continue
                surrounding_binary += x+dx in self.light_pixels[y+dy]
        if enhancement_table[surrounding_binary]:
            target_grid[y].add(x)
        else:
            target_grid[y].discard(x)

    def enhance(self):
        self.__increase_inner_range()
        new_light_pixels = {}
        for y in range(self.outer_min_y, self.outer_max_y + 1):
            new_light_pixels[y] = set()
            for x in range(self.outer_min_x, self.outer_max_x + 1):
                self.calculate_new_pixel_value(new_light_pixels, x, y, enhancement_pattern)
        self.light_pixels = new_light_pixels

    def print(self):
        for y in range(self.min_y, self.max_y + 1):
            print(''.join([
                '#' if x in self.light_pixels[y] else '.'
                 for x in range(self.min_x, self.max_x + 1)
                ]))

    def count_lit_pixels(self) -> int:
        count = 0
        for y in range(self.min_y, self.max_y + 1):
            for x in range(self.min_x, self.max_x + 1):
                count += x in self.light_pixels[y]
        return count

    @staticmethod
    def get_light_pixels_from_grid(grid:list[str]) -> dict[int, set[int]]:
        """returns a list (one entry per row) of lists (each containing the light pixels' x indices in that row) """
        light_pixels = {}
        for y, row in enumerate(grid):
            line_y = set()
            for x, pixel in enumerate(row):
                if pixel == '#':
                    line_y.add(x)
            light_pixels[y] = line_y
        return light_pixels

def part1():
    starting_light_pixels = Image.get_light_pixels_from_grid(starting_input)
    image = Image(starting_light_pixels, 20)
    image.print()
    for i in range(2):
        image.enhance()
    print("")
    image.print()
    print('lit pixels after 2 reps: %d' % image.count_lit_pixels())

def part2():
    starting_light_pixels = Image.get_light_pixels_from_grid(starting_input)
    image = Image(starting_light_pixels, 200)
    image.print()
    for i in range(50):
        image.enhance()
    print("")
    # image.print()
    print('lit pixels after 50 reps: %d' % image.count_lit_pixels())

part1()
part2()