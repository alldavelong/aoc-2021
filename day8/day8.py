#!/usr/bin/env python3

file = open('input.txt')
# file = open('test.txt')
entries = file.read().splitlines()
file.close()

import re

class Digit:
    def __init__(self, value:int, needed_signals:list[chr]) -> None:
        self.value = value
        self.needed_signals = needed_signals
        pass
    
    def number_of_needed_signals(self) -> int:
        return len(self.needed_signals)
    
def get_easy_digits(digits:list[Digit]):
    easy_count = [None]*10
    for digit in digits:
        number = digit.number_of_needed_signals()
        if easy_count[number] == None:
            easy_count[number] = digit
        elif easy_count[number] != 0:
            easy_count[number] = 0
    easy_digits = []
    for entry in easy_count:
        if entry != 0 and entry != None:
            easy_digits.append(entry)
    return easy_digits

def init_digits() -> list[Digit]:
    digits = {
        0: ['a', 'b', 'c',      'e', 'f', 'g'],
        1: [          'c',           'f'],
        2: ['a',      'c', 'd', 'e',      'g'],
        3: ['a',      'c', 'd',      'f', 'g'],
        4: [     'b', 'c', 'd',      'f'],
        5: ['a', 'b',      'd',      'f', 'g'],
        6: ['a', 'b',      'd', 'e', 'f', 'g'],
        7: ['a',      'c',           'f'],
        8: ['a', 'b', 'c', 'd', 'e', 'f', 'g'],
        9: ['a', 'b', 'c', 'd',      'f', 'g']
    }
    return [Digit(key, digits[key]) for key in digits]

def read_entry(entry:str) -> tuple:
    return [part.split() for part in re.split(' \| ', entry)]

def part1():
    digits = init_digits()
    easy_digits = get_easy_digits(digits)
    unique_count = 0

    for line in entries:
        signal_patterns, output_digits = read_entry(line)
        for digit in output_digits:
            if len(digit) in [len(digit.needed_signals) for digit in easy_digits]:
                # print(digit)
                unique_count += 1
    print('number of found easy digits: %d' % unique_count)

part1()
# no solution found for part2