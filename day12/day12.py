#!/usr/bin/env python3

file = open("input.txt")
# file = open("test.txt")
cave_connections = file.read().splitlines()
file.close()

class Cave:
    def __init__(self, name: str) -> None:
        self.name = name
        self.connected_caves = []
        self.is_big = Cave.__is_big_cave(name)

    def __is_big_cave(name: str):
        return name.isupper()

    def add_connected_if_new(self, neighbour):
        if neighbour.name not in [c.name for c in self.connected_caves]:
            self.connected_caves.append(neighbour)

    @staticmethod
    def init_all_caves(cave_connections: list[str]) -> dict:
        all_caves = {}
        for connection in cave_connections:
            cave, neighbour = connection.split("-")
            existing = [all_caves[key].name for key in all_caves]
            if cave not in existing:
                all_caves[cave] = Cave(cave)
            if neighbour not in existing:
                all_caves[neighbour] = Cave(neighbour)
            all_caves[cave].add_connected_if_new(all_caves[neighbour])
            all_caves[neighbour].add_connected_if_new(all_caves[cave])
        # print([('"%s" connects to: %s' % (all_caves[key].name, [conn.name for conn in all_caves[key].connected_caves])) for key in all_caves])
        return all_caves

def find_all_paths(cave: Cave, current_path: list = [], allow_one_double_visit=False) -> list[list]:
    all_paths = []
    current_path.append(cave)

    for next_cave in cave.connected_caves:
        if next_cave.name == 'start':
            continue
        this_is_a_double_visit = next_cave in current_path and not next_cave.is_big
        if this_is_a_double_visit and not allow_one_double_visit:
            continue

        if next_cave.name == "end":
            # print([c.name for c in current_path + [next_cave]])
            all_paths.append(current_path + [next_cave])
        else:
            all_paths.extend(find_all_paths(next_cave, [x for x in current_path],allow_one_double_visit and not this_is_a_double_visit))
    return all_paths

all_caves = Cave.init_all_caves(cave_connections)

def part1():
    all_paths = find_all_paths(all_caves["start"])
    print('%d possible ways (visit small caves only once)' % len(all_paths))


def part2():
    all_paths = find_all_paths(all_caves["start"], allow_one_double_visit=True)
    print('%d possible ways when allowing one double visit' % len(all_paths))


part1()
part2()
