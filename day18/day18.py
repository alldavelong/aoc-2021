#!/usr/bin/env python3
import math
from abc import abstractmethod

file = open('input.txt')
# file = open('test.txt')
summands = file.read().splitlines()
file.close()


class SnailfishNumber:
    @classmethod
    def from_list_of_strings(cls, input_strings):
        numbers = [cls.from_string(string) for string in input_strings]
        tree = numbers[0]
        for i in range(1, len(numbers)):
            tree.add(numbers[i])
        return tree

    @classmethod
    def from_string(cls, input_string):
        """ Create a SnailfishNumber object from the printed string.

        Splits an input_string like '[[[3,3],2],[4,4]]' at the middle comma and returns the corresponding tree
        hierarchy of NumberPair and RegularNumber objects. The first and last characters (brackets) are skipped.
        """
        if not (input_string.__contains__('[') or input_string.__contains__(']') or input_string.__contains__(',')):
            return RegularNumber(int(input_string))
        open_brackets, search_index = 0, 1
        bracket_count_values = {'[': 1, ']': -1}
        while search_index < len(input_string) - 1:
            char = input_string[search_index]
            if char == ',' and open_brackets == 0:
                break
            if char in bracket_count_values.keys():
                open_brackets += bracket_count_values[char]
            search_index += 1
        return NumberPair(
            cls.from_string(input_string[1:search_index]),  # everything before the comma except starting '['
            cls.from_string(input_string[search_index + 1:-1])  # everything after the comma except ending ']'
        )

    @abstractmethod
    def add(self, other):
        """ Add the other number to the calling number. """

    @abstractmethod
    def calculate_magnitude(self):
        """ Returns the calculated magnitude of the SnailfishNumber and all children recursively"""

    @abstractmethod
    def to_string(self):
        """ Returns a string from the SnailfishNumber and all children recursively. """


class RegularNumber(SnailfishNumber):
    def __init__(self, value: int):
        self.value = value

    def add(self, other):
        self.value += other.value

    def calculate_magnitude(self):
        return self.value

    def to_string(self):
        return str(self.value)


class NumberPair(SnailfishNumber):
    def __init__(self, number1, number2):
        self.numbers = [number1, number2]

    def handle_explosion(self, nest_count=0, closest_left_neighbor=None, right_explosion_value=None, all_done=False):
        explosion_possible = True if nest_count + 1 == 4 else False  # True: pair "will consist of two regular numbers"

        for c, child in enumerate(self.numbers):
            if all_done:
                return closest_left_neighbor, right_explosion_value, all_done

            explosion_has_happened = right_explosion_value is not None

            if explosion_possible and not explosion_has_happened and not isinstance(child, RegularNumber):  # explodes
                if closest_left_neighbor is not None:
                    closest_left_neighbor.add(child.numbers[0])
                right_explosion_value = child.numbers[1]
                self.numbers[c] = RegularNumber(0)
                # closest right neighbor still needs to be found
                continue

            if isinstance(child, RegularNumber):
                if explosion_has_happened:
                    child.add(right_explosion_value)
                    return closest_left_neighbor, right_explosion_value, True
                else:
                    closest_left_neighbor = child
            else:
                closest_left_neighbor, right_explosion_value, all_done = child.handle_explosion(
                    nest_count + 1, closest_left_neighbor, right_explosion_value)

        return closest_left_neighbor, right_explosion_value, all_done

    def handle_splitting(self):
        for c, child in enumerate(self.numbers):
            if isinstance(child, RegularNumber):
                if child.value >= 10:
                    floor, ceil = math.floor(child.value/2), math.ceil(child.value/2)
                    self.numbers[c] = NumberPair(RegularNumber(floor), RegularNumber(ceil))
                    return True
            else:
                if child.handle_splitting():
                    return True
        return False

    def reduce(self):
        while True:
            if self.handle_explosion()[2]:
                continue
            if self.handle_splitting():
                continue
            break

    def add(self, other):
        self.numbers[0] = NumberPair(self.numbers[0], self.numbers[1])
        self.numbers[1] = other
        self.reduce()

    def calculate_magnitude(self):
        magnitude = 0
        for c, child in enumerate(self.numbers):
            magnitude += (3 if c == 0 else 2) * child.calculate_magnitude()
        return magnitude

    def to_string(self):
        return f"[{self.numbers[0].to_string()},{self.numbers[1].to_string()}]"


def test1():
    def test_explosion(input_strs, expected_solution):
        explosion = SnailfishNumber.from_list_of_strings(input_strs)
        explosion.handle_explosion()
        print("explosion:", explosion.to_string(), explosion.to_string() == expected_solution)

    def test_spliting(input_strs, expected_solution):
        split = SnailfishNumber.from_list_of_strings(input_strs)
        split.handle_splitting()
        print("splitting:", split.to_string(), split.to_string() == expected_solution)

    def test_list_adding(input_list, expected_solution):
        number = SnailfishNumber.from_list_of_strings(input_list)
        print("adding:", number.to_string(), number.to_string() == expected_solution, number.calculate_magnitude())

    test_explosion(['[[[[[9,8],1],2],3],4]'], '[[[[0,9],2],3],4]')
    test_explosion(['[7,[6,[5,[4,[3,2]]]]]'], '[7,[6,[5,[7,0]]]]')
    test_explosion(['[[6,[5,[4,[3,2]]]],1]'], '[[6,[5,[7,0]]],3]')
    test_explosion(['[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]'], '[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]')
    test_explosion(['[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]'], '[[3,[2,[8,0]]],[9,[5,[7,0]]]]')

    test_spliting(['[10,0]'], '[[5,5],0]')
    test_spliting(['[11,1]'], '[[5,6],1]')
    test_spliting(['[[3,6],12]'], '[[3,6],[6,6]]')

    num = SnailfishNumber.from_list_of_strings(['[[[[4,3],4],4],[7,[[8,4],9]]]', '[1,1]'])
    num.reduce()

    print("reduction:", num.to_string(), num.to_string() == '[[[[0,7],4],[[7,8],[6,0]]],[8,1]]')
    test_list_adding(['[1,1]', '[2,2]', '[3,3]', '[4,4]'], '[[[[1,1],[2,2]],[3,3]],[4,4]]')

    test_list_adding(['[1,1]', '[2,2]', '[3,3]', '[4,4]', '[5,5]', '[6,6]'], '[[[[5,0],[7,4]],[5,5]],[6,6]]')

    test_list_adding(summands, '[[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]')


def part1():
    number = SnailfishNumber.from_list_of_strings(summands)
    print("result:", number.to_string(), "- magnitude:", number.calculate_magnitude())


def part2():
    max_magnitude = 0
    for num1 in summands:
        for num2 in summands:
            if num1 == num2:
                continue
            magnitude = SnailfishNumber.from_list_of_strings([num1, num2]).calculate_magnitude()
            if magnitude > max_magnitude:
                max_magnitude = magnitude
    print("max magnitude:", max_magnitude)


# test1()
part1()
part2()
